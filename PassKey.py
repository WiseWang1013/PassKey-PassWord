import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import random
import json
import binascii
import base64
from urllib.parse import quote, unquote
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import threading

# ===================== 格式-专属编码方案映射表 =====================
TEXT_FORMATS = {
    "txt": ["caesar", "reverse", "base64"],
    "py": ["reverse", "urlencode", "caesar"],
    "html": ["base64", "urlencode"],
    "cpp": ["caesar", "reverse"],
    "cmd": ["urlencode", "reverse"],
    "bat": ["urlencode", "caesar"],
    "json": ["base64", "reverse"],
    "csv": ["caesar", "urlencode"],
    "toml": ["reverse", "base64"],
    "ini": ["caesar", "reverse"],
    "md": ["urlencode", "caesar"],
    "js": ["base64", "reverse", "urlencode"],
    "css": ["caesar", "urlencode"],
    "java": ["reverse", "caesar"],
    "go": ["base64", "caesar"],
    "rs": ["urlencode", "reverse"]
}

BINARY_FORMATS = {
    "png": "binary_xor",
    "jpg": "binary_xor",
    "gif": "binary_xor",
    "docx": "binary_xor",
    "zip": "binary_xor",
    "rar": "binary_xor",
    "7z": "binary_xor",
    "mp3": "binary_xor",
    "wav": "binary_xor",
    "mp4": "binary_xor"
}
ALL_SUPPORT_EXT = list(TEXT_FORMATS.keys()) + list(BINARY_FORMATS.keys())

# 文本加密流水线
def encrypt_text_data(raw_str, fmt, password, progress_callback=None):
    key_info = {}
    methods = TEXT_FORMATS[fmt]
    random.shuffle(methods)
    use_methods = methods[:random.randint(1, len(methods))]
    key_info["methods"] = use_methods
    key_info["format"] = fmt

    data = raw_str
    total_steps = len(use_methods)+2
    step = 0
    for m in use_methods:
        if progress_callback:
            step +=1
            progress_callback(step/total_steps*100)
        if m == "caesar":
            shift = random.randint(3,20)
            key_info["shift"] = shift
            data = "".join([chr(ord(c)+shift) for c in data])
        elif m == "reverse":
            data = data[::-1]
        elif m == "base64":
            b = data.encode("utf-8")
            data = base64.b64encode(b).decode("utf-8")
        elif m == "urlencode":
            data = quote(data, safe='')
    if progress_callback:
        step +=1
        progress_callback(step/total_steps*100)
    b_data = data.encode("utf-8")
    hex_str = binascii.hexlify(b_data).decode("ascii")
    if progress_callback:
        progress_callback(100)
    raw_key_json = json.dumps(key_info, ensure_ascii=False, indent=2)
    protected_key = xor_crypt(raw_key_json, password)
    return hex_str, protected_key

# 文本解密流水线
def decrypt_text_data(hex_cipher, protected_key, password, progress_callback=None):
    try:
        raw_key_json = xor_crypt(protected_key, password)
        key_info = json.loads(raw_key_json)
        methods = key_info["methods"]
        fmt = key_info["format"]
    except Exception:
        return None, "[密钥/口令错误]"
    try:
        raw_bytes = binascii.unhexlify(hex_cipher)
        data = raw_bytes.decode("utf-8")
    except Exception:
        return None, "密文hex解析失败"
    total_steps = len(methods)+1
    step=0
    for m in reversed(methods):
        if progress_callback:
            step +=1
            progress_callback(step/total_steps*100)
        if m == "caesar":
            shift = key_info["shift"]
            data = "".join([chr(ord(c)-shift) for c in data])
        elif m == "reverse":
            data = data[::-1]
        elif m == "base64":
            data = base64.b64decode(data).decode("utf-8")
        elif m == "urlencode":
            data = unquote(data)
    if progress_callback:
        progress_callback(100)
    return data, fmt

# 二进制文件加密（图片、压缩包、音视频、word）
def encrypt_binary_data(raw_bytes, fmt, password, progress_callback=None):
    key_info = {}
    key_info["format"] = fmt
    xor_key = random.randbytes(16)
    key_info["xor_key"] = binascii.hexlify(xor_key).decode()
    out = bytearray()
    length = len(raw_bytes)
    chunk = 4096
    for i in range(0, length, chunk):
        if progress_callback:
            progress_callback(i/length*100)
        part = raw_bytes[i:i+chunk]
        res = bytes([part[b] ^ xor_key[(i+b) % 16] for b in range(len(part))])
        out.extend(res)
    hex_str = binascii.hexlify(out).decode("ascii")
    if progress_callback:
        progress_callback(100)
    raw_key_json = json.dumps(key_info, ensure_ascii=False, indent=2)
    protected_key = xor_crypt(raw_key_json, password)
    return hex_str, protected_key

def decrypt_binary_data(hex_cipher, protected_key, password, progress_callback=None):
    try:
        raw_key_json = xor_crypt(protected_key, password)
        key_info = json.loads(raw_key_json)
        fmt = key_info["format"]
        xor_key = binascii.unhexlify(key_info["xor_key"])
    except Exception:
        return None, "[密钥/口令错误]"
    try:
        cipher_bytes = binascii.unhexlify(hex_cipher)
    except Exception:
        return None, "hex解析失败"
    out = bytearray()
    length = len(cipher_bytes)
    chunk = 4096
    for i in range(0, length, chunk):
        if progress_callback:
            progress_callback(i/length*100)
        part = cipher_bytes[i:i+chunk]
        res = bytes([part[b] ^ xor_key[(i+b) % 16] for b in range(len(part))])
        out.extend(res)
    if progress_callback:
        progress_callback(100)
    return bytes(out), fmt

# 密钥口令异或保护函数
def xor_crypt(text:str, pwd:str):
    res = []
    pwd_len = len(pwd)
    for i,c in enumerate(text):
        res_char = chr(ord(c) ^ ord(pwd[i % pwd_len]))
        res.append(res_char)
    return "".join(res)

# ===================== GUI =====================
class MultiFileCryptoGUI:
    def __init__(self,root):
        self.root = root
        self.root.title("多格式文件加密神器｜支持手动输入文本+进度条")
        self.root.geometry("980x700")
        self.file_raw_data = None
        self.file_format = "txt"  # 默认手动输入为txt格式
        self.cipher_hex = ""
        self.protected_key = ""
        self.decrypted_data = None
        self.in_working = False

        # 顶部按钮区
        frame_top = tk.Frame(root)
        frame_top.pack(pady=8)
        tk.Button(frame_top,text="📂导入原始文件(拖拽支持)",command=self.load_file).grid(row=0,column=0,padx=3)
        tk.Button(frame_top,text="🔒加密文件/文本",command=self.start_encrypt_thread).grid(row=0,column=1,padx=3)
        tk.Button(frame_top,text="🔓解密(密文txt+密钥txt)",command=self.start_decrypt_thread).grid(row=0,column=2,padx=3)
        tk.Button(frame_top,text="💾导出密文txt",command=self.save_cipher).grid(row=0,column=3,padx=3)
        tk.Button(frame_top,text="🔑导出密钥txt",command=self.save_key).grid(row=0,column=4,padx=3)
        tk.Button(frame_top,text="📤导出解密后的文件",command=self.save_decrypted).grid(row=0,column=5,padx=3)
        tk.Button(frame_top,text="🗑清空文本框",command=self.clear_textbox).grid(row=0,column=6,padx=3)

        tip_text = f"💡可以直接在下方文本框手动输入文字加密（默认txt格式），也可以拖拽文件导入！支持格式：{', '.join(ALL_SUPPORT_EXT)}"
        tk.Label(root, text=tip_text, fg="#206020", wraplength=960).pack()

        self.text_box = tk.Text(root,height=28,width=120)
        self.text_box.pack(padx=10,pady=4)
        self.text_box.drop_target_register(DND_FILES)
        self.text_box.dnd_bind('<<Drop>>', self.on_file_drop)

        # 进度条
        progress_frame = tk.Frame(root)
        progress_frame.pack(fill="x",padx=10)
        tk.Label(progress_frame,text="进度：").pack(side="left")
        self.progress = ttk.Progressbar(progress_frame,orient=tk.HORIZONTAL,length=800,mode="determinate")
        self.progress.pack(side="left",fill="x",expand=True)

        self.status = tk.Label(root,text="就绪，可以直接在文本框打字，或拖拽文件",fg="#333")
        self.status.pack()

    def set_progress(self,val):
        self.root.after(0,lambda:self.progress.config(value=val))

    def get_ext(self,filepath):
        return os.path.splitext(filepath)[1].lower().strip(".")

    def on_file_drop(self, event):
        if self.in_working:
            return
        path = event.data
        if path.startswith("{") and path.endswith("}"):
            path = path[1:-1]
        self.load_file_by_path(path)

    def load_file(self):
        if self.in_working:
            return
        path = filedialog.askopenfilename()
        if not path:
            return
        self.load_file_by_path(path)

    def load_file_by_path(self, path):
        ext = self.get_ext(path)
        self.file_format = ext
        if ext not in ALL_SUPPORT_EXT:
            messagebox.showerror("不支持格式",f"暂不支持后缀 .{ext}，支持列表：\n{ALL_SUPPORT_EXT}")
            return
        try:
            if ext in TEXT_FORMATS:
                with open(path,"r",encoding="utf-8") as f:
                    self.file_raw_data = f.read()
                preview = f"【文本文件】后缀:{ext}\n{self.file_raw_data[:1200]}"
            elif ext in BINARY_FORMATS:
                with open(path,"rb") as f:
                    self.file_raw_data = f.read()
                preview = f"【二进制文件】后缀:{ext}，二进制内容，无法预览"
            self.text_box.delete(1.0,tk.END)
            self.text_box.insert(tk.END,preview)
            self.status.config(text=f"✅加载成功，文件格式：{ext}")
        except Exception as e:
            messagebox.showerror("读取失败",str(e))

    def clear_textbox(self):
        self.text_box.delete(1.0,tk.END)
        self.file_raw_data = None
        self.file_format = "txt"
        self.cipher_hex = ""
        self.protected_key = ""
        self.decrypted_data = None
        self.progress["value"] = 0
        self.status.config(text="已清空，就绪，可以手动输入文字")

    def start_encrypt_thread(self):
        if self.in_working:
            return
        pwd = simpledialog.askstring("设置密钥口令","设置密钥保护口令",show="*")
        if not pwd:
            return
        # 判断：文本框有内容，且没有加载外部文件 → 使用手动输入文本
        text_content = self.text_box.get("1.0",tk.END).strip()
        if self.file_raw_data is None and len(text_content)>0:
            self.file_raw_data = text_content
            self.file_format = "txt"
        if self.file_raw_data is None:
            messagebox.showwarning("提示","请导入文件 或者 在文本框手动输入文字！")
            return
        self.in_working = True
        self.progress["value"] = 0
        self.status.config(text="🔄加密中，请等待...")
        def encrypt_worker():
            try:
                fmt = self.file_format
                if fmt in TEXT_FORMATS:
                    cipher_hex, protected_key = encrypt_text_data(self.file_raw_data, fmt, pwd, progress_callback=self.set_progress)
                elif fmt in BINARY_FORMATS:
                    cipher_hex, protected_key = encrypt_binary_data(self.file_raw_data, fmt, pwd, progress_callback=self.set_progress)
                self.cipher_hex = cipher_hex
                self.protected_key = protected_key
                preview = f"====十六进制密文====\n{self.cipher_hex[:1200]}...\n\n====口令保护密钥(里面记录原始格式:{fmt})====\n{self.protected_key}"
                self.root.after(0,lambda:self.text_box.delete(1.0,tk.END))
                self.root.after(0,lambda:self.text_box.insert(tk.END,preview))
                self.root.after(0,lambda:self.status.config(text="✅加密完成！导出密文txt 和密钥txt，记住口令！"))
            except Exception as e:
                self.root.after(0,lambda:messagebox.showerror("加密失败",str(e)))
                self.root.after(0,lambda:self.status.config(text="❌加密出错"))
            finally:
                self.in_working = False
        threading.Thread(target=encrypt_worker,daemon=True).start()

    def start_decrypt_thread(self):
        if self.in_working:
            return
        cipher_path = filedialog.askopenfilename(title="选择【十六进制密文txt】",filetypes=[("txt","*.txt")])
        if not cipher_path:
            return
        key_path = filedialog.askopenfilename(title="选择【密钥txt】",filetypes=[("txt","*.txt")])
        if not key_path:
            return
        try:
            with open(cipher_path,"r",encoding="utf-8") as f:
                cipher_txt = f.read().strip()
            with open(key_path,"r",encoding="utf-8") as f:
                key_txt = f.read()
        except Exception as e:
            messagebox.showerror("读取错误",str(e))
            return
        pwd = simpledialog.askstring("输入密钥口令","输入加密时设置的口令",show="*")
        if not pwd:
            return
        self.in_working = True
        self.progress["value"] =0
        self.status.config(text="🔄解密中，请等待...")
        def decrypt_worker():
            try:
                data, fmt = decrypt_text_data(cipher_txt, key_txt, pwd, progress_callback=self.set_progress)
                if data is not None:
                    self.decrypted_data = data
                    preview = f"✅解密成功！原始格式：{fmt}\n====还原内容====\n{data[:1200]}"
                else:
                    data, fmt = decrypt_binary_data(cipher_txt, key_txt, pwd, progress_callback=self.set_progress)
                    self.decrypted_data = data
                    preview = f"✅解密成功！原始二进制格式：{fmt}（二进制，无法预览）"
                self.root.after(0,lambda:self.text_box.delete(1.0,tk.END))
                self.root.after(0,lambda:self.text_box.insert(tk.END,preview))
                self.root.after(0,lambda:self.status.config(text=f"✅解密完成！点击【导出解密后的文件】保存，可以修改后缀！"))
            except Exception as e:
                self.root.after(0,lambda:messagebox.showerror("解密失败",str(e)))
                self.root.after(0,lambda:self.status.config(text="❌解密出错"))
            finally:
                self.in_working = False
        threading.Thread(target=decrypt_worker,daemon=True).start()

    def save_cipher(self):
        if not self.cipher_hex:
            messagebox.showwarning("提示","先加密！")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("txt","*.txt")])
        if path:
            with open(path,"w",encoding="utf-8") as f:
                f.write(self.cipher_hex)
            messagebox.showinfo("保存成功","✅密文txt已导出")

    def save_key(self):
        if not self.protected_key:
            messagebox.showwarning("提示","先加密！")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("txt","*.txt")])
        if path:
            with open(path,"w",encoding="utf-8") as f:
                f.write(self.protected_key)
            messagebox.showinfo("保存成功","✅密钥txt已导出（密钥保存原始文件格式）")

    def save_decrypted(self):
        if self.decrypted_data is None:
            messagebox.showwarning("提示","先解密文件！")
            return
        filetype_list = []
        for ext in ALL_SUPPORT_EXT:
            filetype_list.append((f"{ext}文件",f"*.{ext}"))
        filetype_list.append(("所有文件","*.*"))
        path = filedialog.asksaveasfilename(
            defaultextension=".*",
            filetypes=filetype_list
        )
        if not path:
            return
        try:
            if isinstance(self.decrypted_data, str):
                with open(path,"w",encoding="utf-8") as f:
                    f.write(self.decrypted_data)
            else:
                with open(path,"wb") as f:
                    f.write(self.decrypted_data)
            messagebox.showinfo("导出成功！","解密文件保存完成，可自定义后缀名")
        except Exception as e:
            messagebox.showerror("保存失败",str(e))


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MultiFileCryptoGUI(root)
    root.mainloop()