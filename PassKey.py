# -*- coding: utf-8 -*-
"""
PassKey‑Password V2.0
简易批量文件加密解密工具 Windows Only
⚠️ V2.0 不兼容 V1.0 ~ V1.1.1‑beta 的旧密文、旧密钥！
Author: WiseWang1013 https://github.com/WiseWang1013
仅学习用途，禁止恶意加密、勒索行为
"""
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import random
import json
import binascii
import base64
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import threading

# ===================== 加密核心（V2.0：全部文件统一二进制XOR，不再区分文本/二进制后缀方案） =====================
def xor_crypt_bytes(data: bytes, key: bytes) -> bytes:
    """通用字节异或加密，输入字节，输出字节"""
    k_len = len(key)
    return bytes(b ^ key[i % k_len] for i, b in enumerate(data))


def password_wrap_key(raw_key_bytes: bytes, password: str) -> str:
    """用口令保护原始随机密钥；允许password为空字符串(无密码模式)
    返回base64保护后的密钥字符串，存到密钥文档
    """
    raw_b64 = base64.b64encode(raw_key_bytes).decode("utf‑8")
    if not password:
        return json.dumps({"no_password": True, "raw_b64": raw_b64}, ensure_ascii=False)
    # 口令异或保护
    out_chars = []
    for idx, ch in enumerate(raw_b64):
        out_chars.append(chr(ord(ch) ^ ord(password[idx % len(password)])))
    wrapped = "".join(out_chars)
    return json.dumps({"no_password": False, "wrapped": wrapped}, ensure_ascii=False)


def password_unwrap_key(wrapped_json_str: str, password: str) -> bytes | None:
    """从受保护密钥json，还原出原始加密密钥；失败返回None"""
    try:
        obj = json.loads(wrapped_json_str)
    except Exception:
        return None
    if obj.get("no_password") is True:
        return base64.b64decode(obj["raw_b64"])
    wrapped = obj["wrapped"]
    out_chars = []
    for idx, ch in enumerate(wrapped):
        out_chars.append(chr(ord(ch) ^ ord(password[idx % len(password)])))
    raw_b64 = "".join(out_chars)
    return base64.b64decode(raw_b64)


def encrypt_single_file(file_bytes: bytes, password: str, mode_auto: bool, progress_cb=None) -> tuple[str, str]:
    """
    加密单个文件
    :param file_bytes: 原始文件字节
    :param password: 用户口令，可以为空字符串
    :param mode_auto: True=自动随机16字节密钥；False=固定密钥(内部固定测试密钥，界面给用户选择)
    :param progress_cb: 进度回调0‑100
    :return: (cipher_hex, protected_key_json_str)
    """
    total = len(file_bytes)
    if mode_auto:
        crypt_key = random.randbytes(16)
    else:
        # 用户选择自定义固定加密密钥模式
        crypt_key = b"PassKeyV2FixedKey1"

    chunk_size = 8192
    cipher_buffer = bytearray()
    for offset in range(0, total, chunk_size):
        chunk = file_bytes[offset:offset + chunk_size]
        enc_chunk = xor_crypt_bytes(chunk, crypt_key)
        cipher_buffer.extend(enc_chunk)
        if progress_cb and total > 0:
            progress_cb(offset / total * 100)
    if progress_cb:
        progress_cb(100)
    cipher_hex = binascii.hexlify(cipher_buffer).decode("ascii")
    protected_key = password_wrap_key(crypt_key, password)
    return cipher_hex, protected_key


def decrypt_single_file(cipher_hex: str, protected_key_json: str, password: str, progress_cb=None) -> bytes | None:
    """解密单个文件，返回原始bytes，出错返回None"""
    crypt_key = password_unwrap_key(protected_key_json, password)
    if crypt_key is None:
        return None
    try:
        cipher_bytes = binascii.unhexlify(cipher_hex)
    except Exception:
        return None
    total = len(cipher_bytes)
    chunk_size = 8192
    out_buffer = bytearray()
    for offset in range(0, total, chunk_size):
        chunk = cipher_bytes[offset:offset + chunk_size]
        dec_chunk = xor_crypt_bytes(chunk, crypt_key)
        out_buffer.extend(dec_chunk)
        if progress_cb and total > 0:
            progress_cb(offset / total * 100)
    if progress_cb:
        progress_cb(100)
    return bytes(out_buffer)

# ===================== GUI 界面：纯白简约布局，按钮全部左侧，右侧预览 =====================
class PassKeyV2GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PassKey‑Password V2.0 批量文件加密解密工具 | Windows")
        self.root.geometry("1100x720")
        self.root.minsize(950, 620)
        # V2.0 纯白主题
        BG_MAIN = "#ffffff"
        BG_LEFT = "#f3f4f6"
        self.root.configure(bg=BG_MAIN)

        # 工作状态标记
        self.is_working = False
        self.file_list: list[str] = []  # 批量待加密文件路径列表
        self.last_cipher_hex = ""
        self.last_protected_key = ""
        self.last_decrypted_bytes: bytes | None = None
        self.last_dec_ext: str = ""

        # ----------------布局划分：左侧控制面板，右侧预览区----------------
        main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#dddddd", sashwidth=4)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 左侧面板：所有按钮放这里
        frame_left = tk.Frame(main_pane, bg=BG_LEFT, width=240)
        main_pane.add(frame_left, minsize=220)

        # 右侧预览面板
        frame_right = tk.Frame(main_pane, bg="#ffffff")
        main_pane.add(frame_right, minsize=600)

        # --------左侧控件--------
        row_idx = 0
        tk.Label(frame_left, text="操作面板", font=("Microsoft YaHei",12,"bold"), bg=BG_LEFT).grid(row=row_idx, column=0, pady=(12,6))
        row_idx +=1

        tk.Button(frame_left, text="📂 多选待加密文件", command=self.select_multi_files, width=22, bg="#4088dd", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="🔒 批量加密全部文件", command=self.start_batch_encrypt_thread, width=22, bg="#27ae60", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="🔓 批量解密(密文+密钥)", command=self.start_batch_decrypt_thread, width=22, bg="#9b59b6", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="💾 导出密文包", command=self.export_cipher_package, width=22, bg="#e67e22", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="🔑 导出统一密钥", command=self.export_global_key, width=22, bg="#e67e22", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="📤 批量导出解密文件", command=self.batch_save_decrypted, width=22, bg="#27ae60", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="🗑 清空全部", command=self.ui_clear_all, width=22, bg="#e74c3c", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=3)
        row_idx +=1

        tk.Button(frame_left, text="📖 使用说明 / 协议", command=self.show_license_dialog, width=22, bg="#606870", fg="white", relief="flat", font=("Microsoft YaHei",10)).grid(row=row_idx, column=0, pady=(12,4))
        row_idx +=1

        # 加密模式单选
        self.enc_mode_var = tk.BooleanVar(value=True)
        frame_radio = tk.Frame(frame_left, bg=BG_LEFT)
        frame_radio.grid(row=row_idx, column=0, pady=(10,4))
        ttk.Radiobutton(frame_radio, text="随机密钥(推荐)", variable=self.enc_mode_var, value=True).pack(anchor="w")
        ttk.Radiobutton(frame_radio, text="固定测试密钥", variable=self.enc_mode_var, value=False).pack(anchor="w")
        row_idx +=1

        # 文件列表显示框（左侧）
        tk.Label(frame_left, text="已选择文件列表", bg=BG_LEFT, font=("Microsoft YaHei", 10)).grid(row=row_idx, column=0, pady=(8,2))
        row_idx +=1
        self.listbox_files = tk.Listbox(frame_left, width=28, height=12, font=("Consolas",9))
        self.listbox_files.grid(row=row_idx, column=0, padx=6, pady=2)

        # --------右侧：预览文本框--------
        tk.Label(frame_right, text="预览信息", font=("Microsoft YaHei",12,"bold"), bg="#ffffff").pack(anchor="w", padx=10, pady=(8,2))
        self.text_preview = tk.Text(frame_right, font=("Consolas", 10), wrap="word", bg="#fafafa")
        self.text_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        self.text_preview.drop_target_register(DND_FILES)
        self.text_preview.dnd_bind('<<Drop>>', self.on_drop_files)

        # 底部全局进度 +状态栏
        frame_bottom = tk.Frame(root, bg="#ffffff")
        frame_bottom.pack(fill="x", padx=10, pady=6)
        tk.Label(frame_bottom, text="总进度：", bg="#ffffff").pack(side="left")
        self.progress_bar = ttk.Progressbar(frame_bottom, orient=tk.HORIZONTAL, mode="determinate")
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=6)

        self.label_status = tk.Label(root, text="就绪｜V2.0 不兼容V1.x旧密文", fg="#c0392b", bg="#ffffff", font=("Microsoft YaHei", 10))
        self.label_status.pack(pady=(0,6))

    def set_progress(self, value: float):
        self.root.after(0, lambda: self.progress_bar.config(value=value))

    def set_status(self, text: str, color="#222222"):
        self.root.after(0, lambda: self.label_status.config(text=text, fg=color))

    def preview_append(self, msg: str):
        self.root.after(0, lambda: (self.text_preview.insert(tk.END, msg + "\n"), self.text_preview.see(tk.END)))

    def preview_clear(self):
        self.root.after(0, lambda: self.text_preview.delete(1.0, tk.END))

    # =========拖拽处理=========
    def on_drop_files(self, event):
        if self.is_working:
            return
        raw = event.data
        paths = self.parse_drop_path(raw)
        for p in paths:
            if os.path.isfile(p):
                self.file_list.append(p)
        self.refresh_file_listbox()

    def parse_drop_path(self, raw_data: str) -> list[str]:
        out = []
        parts = raw_data.split()
        for s in parts:
            if s.startswith("{") and s.endswith("}"):
                s = s[1:-1]
            out.append(s)
        return out

    # =========文件选择UI=========
    def select_multi_files(self):
        if self.is_working:
            return
        paths = filedialog.askopenfilenames(title="选择多个待加密文件（支持几乎所有Windows文件格式）")
        if not paths:
            return
        for p in paths:
            self.file_list.append(p)
        self.refresh_file_listbox()

    def refresh_file_listbox(self):
        self.listbox_files.delete(0, tk.END)
        for fp in self.file_list:
            self.listbox_files.insert(tk.END, os.path.basename(fp))
        self.preview_clear()
        self.preview_append(f"已加载 {len(self.file_list)} 个文件")

    def ui_clear_all(self):
        self.file_list.clear()
        self.last_cipher_hex = ""
        self.last_protected_key = ""
        self.last_decrypted_bytes = None
        self.last_dec_ext = ""
        self.listbox_files.delete(0, tk.END)
        self.preview_clear()
        self.progress_bar["value"] = 0
        self.set_status("已全部清空，就绪", "#27ae60")

    # =========批量加密线程=========
    def start_batch_encrypt_thread(self):
        if self.is_working:
            return
        if len(self.file_list) <= 0:
            messagebox.showwarning("提示", "请先选择/拖拽待加密文件！")
            return
        password = simpledialog.askstring("设置加密口令（可以留空不设置密码）", "口令，直接点确定代表不设置密码", show="*")
        if password is None:
            return
        mode_auto = self.enc_mode_var.get()
        self.is_working = True
        self.set_status("批量加密进行中……", "#d35400")
        self.preview_clear()

        def worker():
            try:
                total_file_count = len(self.file_list)
                package_data = {"version":"V2.0","files":[]}
                global_crypt_key = random.randbytes(16) if mode_auto else b"PassKeyV2FixedKey1"

                for idx, fpath in enumerate(self.file_list):
                    fname = os.path.basename(fpath)
                    self.preview_append(f"正在加密：{fname}")
                    with open(fpath, "rb") as f:
                        raw_bytes = f.read()
                    # 单文件加密，复用同一个全局密钥（批量统一密钥）
                    chunk_size = 8192
                    total_len = len(raw_bytes)
                    buf = bytearray()
                    for offset in range(0, total_len, chunk_size):
                        c = raw_bytes[offset:offset+chunk_size]
                        buf.extend(xor_crypt_bytes(c, global_crypt_key))
                        sub_progress = (idx / total_file_count)*100 + ((offset/total_len)/total_file_count)*100
                        self.set_progress(sub_progress)
                    hex_cipher = binascii.hexlify(buf).decode("ascii")
                    package_data["files"].append({
                        "orig_name": fname,
                        "cipher_hex": hex_cipher
                    })
                # 全部文件完成，生成统一受保护密钥
                protected_global_key = password_wrap_key(global_crypt_key, password if password else "")
                self.last_protected_key = protected_global_key
                self.last_cipher_hex = json.dumps(package_data, ensure_ascii=False)
                self.preview_append(f"\n✅ {total_file_count}个文件加密完成！请导出【密文包】和【统一密钥】")
                self.set_progress(100)
                self.set_status("批量加密完成，请导出密文包、统一密钥", "#27ae60")
            except Exception as e:
                messagebox.showerror("加密异常", str(e))
                self.set_status("加密失败", "#e74c3c")
            finally:
                self.is_working = False
        threading.Thread(target=worker, daemon=True).start()

    def export_cipher_package(self):
        if not self.last_cipher_hex:
            messagebox.showwarning("提示","请先执行批量加密！")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("V2密文包 *.txt","*.txt")])
        if not save_path:
            return
        with open(save_path, "w", encoding="utf‑8") as fw:
            fw.write(self.last_cipher_hex)
        messagebox.showinfo("导出成功", "密文包已保存")

    def export_global_key(self):
        if not self.last_protected_key:
            messagebox.showwarning("提示","请先执行批量加密！")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("V2统一密钥 *.txt","*.txt")])
        if not save_path:
            return
        with open(save_path, "w", encoding="utf‑8") as fw:
            fw.write(self.last_protected_key)
        messagebox.showinfo("导出成功", "统一密钥已保存")

    # =========批量解密=========
    def start_batch_decrypt_thread(self):
        if self.is_working:
            return
        cipher_pack_path = filedialog.askopenfilename(title="选择V2密文包txt", filetypes=[("密文包txt","*.txt")])
        if not cipher_pack_path:
            return
        key_path = filedialog.askopenfilename(title="选择V2统一密钥txt", filetypes=[("统一密钥txt","*.txt")])
        if not key_path:
            return
        try:
            with open(cipher_pack_path, "r", encoding="utf‑8") as f:
                cipher_package_json = f.read()
            with open(key_path, "r", encoding="utf‑8") as f:
                key_json_text = f.read()
        except Exception as e:
            messagebox.showerror("读取失败", str(e))
            return
        password = simpledialog.askstring("输入加密口令（无密码直接确定）", "口令", show="*")
        if password is None:
            return
        self.is_working = True
        self.set_status("批量解密中……", "#d35400")
        self.preview_clear()

        def decrypt_worker():
            try:
                pkg = json.loads(cipher_package_json)
                if pkg.get("version") != "V2.0":
                    raise RuntimeError("不是V2.0密文包，V2不兼容V1.x旧密文！")
                files_list = pkg["files"]
                master_key = password_unwrap_key(key_json_text, password if password else "")
                if master_key is None:
                    raise RuntimeError("口令错误 / 密钥损坏")
                self.preview_append(f"待解密总数量：{len(files_list)}")
                # 存解密结果到内存
                self._batch_decrypt_result_cache = []
                for idx, item in enumerate(files_list):
                    orig_name = item["orig_name"]
                    hex_cip = item["cipher_hex"]
                    self.preview_append(f"解密：{orig_name}")
                    cip_bytes = binascii.unhexlify(hex_cip)
                    buf = bytearray()
                    chunk_sz = 8192
                    total_len = len(cip_bytes)
                    for offset in range(0, total_len, chunk_sz):
                        c = cip_bytes[offset:offset+chunk_sz]
                        buf.extend(xor_crypt_bytes(c, master_key))
                        subp = (idx/len(files_list))*100 + ((offset/total_len)/len(files_list))*100
                        self.set_progress(subp)
                    self._batch_decrypt_result_cache.append((orig_name, bytes(buf)))
                self.set_progress(100)
                self.preview_append("\n✅全部解密完成！点击【批量导出解密文件】选择输出文件夹")
                self.set_status("批量解密完成，请导出文件", "#27ae60")
            except Exception as err:
                messagebox.showerror("解密失败", str(err))
                self.set_status("解密失败", "#e74c3c")
            finally:
                self.is_working = False
        threading.Thread(target=decrypt_worker, daemon=True).start()

    def batch_save_decrypted(self):
        if not hasattr(self, "_batch_decrypt_result_cache") or len(self._batch_decrypt_result_cache) <= 0:
            messagebox.showwarning("提示","请先执行批量解密！")
            return
        out_dir = filedialog.askdirectory(title="选择解密文件输出目录，保持原文件名格式导出")
        if not out_dir:
            return
        for orig_filename, raw_bytes in self._batch_decrypt_result_cache:
            fullpath = os.path.join(out_dir, orig_filename)
            with open(fullpath, "wb") as fw:
                fw.write(raw_bytes)
        messagebox.showinfo("导出完成", f"全部文件已经输出到：{out_dir}\n保持原始文件名与后缀格式不变")

    # =========协议说明弹窗=========
    def show_license_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("PassKey‑V2 使用说明与版权协议")
        win.geometry("680x520")
        win.resizable(False,False)
        txt = tk.Text(win, font=("Microsoft YaHei", 10), wrap="word")
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        license_text = """
PassKey‑Password V2.0 批量文件加密解密工具
Windows 专用版本

原项目作者：WiseWang1013
Github主页：https://github.com/WiseWang1013

【重要兼容性警告】
⚠️ V2.0 完全不兼容 V1.0 ~ V1.1.1‑beta 的密文与密钥！
旧版本生成的密文密钥无法被V2解密。

【加密模式说明】
1.随机密钥(推荐)：每次加密生成全新随机16字节密钥，安全性高。
2.固定测试密钥：使用写死固定密钥，仅用于测试调试，不要正式加密重要文件。

【功能说明】
‑支持几乎全部Windows文件格式，全部文件统一二进制异或加密
‑批量多选文件加密，全部文件使用同一个密钥
‑批量解密，导出时自动保持原始文件名、原始后缀格式不变
‑支持不设置密码（口令留空）

【版权与免责声明】
本项目仅为编程学习演示软件。
禁止用于加密他人文件、锁机、勒索等一切违法行为。
加密后的文件，请务必保管好密钥与口令；遗忘口令无法找回数据。
软件不提供任何商业级安全保证，重要资料请自行额外备份。
"""
        txt.insert(tk.END, license_text)
        txt.config(state=tk.DISABLED)
        tk.Button(win, text="关闭", command=win.destroy, bg="#4488dd", fg="white", relief="flat").pack(pady=8)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PassKeyV2GUI(root)
    root.mainloop()
