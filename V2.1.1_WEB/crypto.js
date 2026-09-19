/**
 * PassKey V2.0 WebPWA
 * 与PC Python源码完全互通，XOR批量文件加密
 * 文件名完全自由自定义，不依赖固定文件名
 */

// XOR字节加解密
function xorCryptBytes(uint8Data, keyBytes) {
    const out = new Uint8Array(uint8Data.length);
    const kLen = keyBytes.length;
    for (let i = 0; i < uint8Data.length; i++) {
        out[i] = uint8Data[i] ^ keyBytes[i % kLen];
    }
    return out;
}

// 包装密钥：原始16字节密钥 → JSON字符串（key.txt内容）
function passwordWrapKey(rawKeyBytes, password) {
    const rawB64 = btoa(String.fromCharCode(...rawKeyBytes));
    if (!password) {
        return JSON.stringify({ no_password: true, raw_b64: rawB64 }, null, 2);
    }
    let wrappedChars = [];
    for (let idx = 0; idx < rawB64.length; idx++) {
        const ch = rawB64[idx];
        const pCh = password[idx % password.length];
        const code = ch.charCodeAt(0) ^ pCh.charCodeAt(0);
        wrappedChars.push(String.fromCharCode(code));
    }
    const wrapped = wrappedChars.join("");
    return JSON.stringify({ no_password: false, wrapped: wrapped }, null, 2);
}

// 解开密钥JSON，返回Uint8Array原始密钥；失败返回null
function passwordUnwrapKey(wrappedJsonStr, password) {
    try {
        const obj = JSON.parse(wrappedJsonStr);
        if (obj.no_password === true) {
            const binStr = atob(obj.raw_b64);
            return Uint8Array.from([...binStr].map(c => c.charCodeAt(0)));
        }
        const wrapped = obj.wrapped;
        let rawB64Chars = [];
        for (let idx = 0; idx < wrapped.length; idx++) {
            const ch = wrapped[idx];
            const pCh = password[idx % password.length];
            const code = ch.charCodeAt(0) ^ pCh.charCodeAt(0);
            rawB64Chars.push(String.fromCharCode(code));
        }
        const rawB64 = rawB64Chars.join("");
        const binStr = atob(rawB64);
        return Uint8Array.from([...binStr].map(c => c.charCodeAt(0)));
    } catch (e) {
        console.error("密钥解析错误", e);
        return null;
    }
}

/**
 * 批量加密文件列表
 * @param {File[]} fileList 待加密文件数组
 * @param {string} password 口令，空字符串=无密码
 * @param {boolean} useFixedKey true=随机16字节，false=固定测试密钥 PassKeyV2FixedKey1
 * @returns {Promise<{cipherPackageText:string, protectedKeyText:string}>}
 */
async function batchEncryptFiles(fileList, password, useFixedKey = true) {
    let globalKey;
    if (useFixedKey) {
        globalKey = crypto.getRandomValues(new Uint8Array(16));
    } else {
        const fixedText = "PassKeyV2FixedKey1";
        globalKey = new TextEncoder().encode(fixedText);
    }

    const pkgData = {
        version: "V2.0",
        files: []
    };

    for (const file of fileList) {
        const buf = await file.arrayBuffer();
        const fileBytes = new Uint8Array(buf);
        const encryptedBytes = xorCryptBytes(fileBytes, globalKey);
        // 转hex
        let hexStr = "";
        for (const b of encryptedBytes) {
            hexStr += b.toString(16).padStart(2, "0");
        }
        pkgData.files.push({
            orig_name: file.name,
            cipher_hex: hexStr
        });
    }

    const cipherPackageText = JSON.stringify(pkgData, null, 2);
    const protectedKeyText = passwordWrapKey(globalKey, password);
    return { cipherPackageText, protectedKeyText };
}

/**
 * 批量解密
 * @param {string} cipherPackageText 密文包JSON文本
 * @param {string} keyJsonText 密钥JSON文本
 * @param {string} password 用户口令
 * @returns {Promise<Array<{name:string,data:Uint8Array}>>} 返回文件数组
 */
async function batchDecryptFiles(cipherPackageText, keyJsonText, password) {
    const masterKey = passwordUnwrapKey(keyJsonText, password);
    if (!masterKey) throw new Error("密钥或口令错误");

    const pkg = JSON.parse(cipherPackageText);
    if (pkg.version !== "V2.0") throw new Error("不是V2.0密文包，不兼容旧版本！");

    const resultFiles = [];
    for (const item of pkg.files) {
        const hexStr = item.cipher_hex;
        const origName = item.orig_name;
        // hex转字节
        const bytes = [];
        for (let i = 0; i < hexStr.length; i += 2) {
            bytes.push(parseInt(hexStr.substring(i, i + 2), 16));
        }
        const cipherBytes = new Uint8Array(bytes);
        const plainBytes = xorCryptBytes(cipherBytes, masterKey);
        resultFiles.push({ name: origName, data: plainBytes });
    }
    return resultFiles;
}

// 下载文本文件（支持自定义文件名）
function downloadTextFile(content, defaultName) {
    let saveName = prompt("自定义保存文件名（默认：" + defaultName + "）", defaultName);
    if (saveName === null) return;
    if (!saveName.endsWith(".txt")) saveName += ".txt";
    const blob = new Blob([content], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = saveName;
    a.click();
    URL.revokeObjectURL(a.href);
}

// 下载二进制文件
function downloadBinaryFile(uint8Data, filename) {
    const blob = new Blob([uint8Data]);
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
}