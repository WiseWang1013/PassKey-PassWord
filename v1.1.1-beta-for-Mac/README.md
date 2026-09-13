# PassKey v1.1.1-beta-for‑macOS
🟡 Beta测试版｜macOS源码版本
> ⚠️**不提供预编译app/dmg，仅提供源代码，用户本地自行运行或打包**
> 移除Windows bat/cmd，保留Linux脚本格式(sh/conf/service)，新增mac专属 plist、mobileconfig 支持

## ✨项目简介
Python+Tkinter图形加密工具，支持mac、linux常用脚本与配置文件，文件拖拽，进度显示，密文密钥分离保存。
> ⚠️口令丢失，文件永久无法解密；仅限学习研究，禁止恶意使用。

## 📂支持文件后缀
**文本类：**
txt, py, html, cpp, json, csv, toml, ini, md, js, css, java, go, rs, sh, conf, service, plist, mobileconfig

**二进制类：**
png, jpg, gif, docx, zip, rar, 7z, mp3, wav, mp4

## 📦源码运行
### 1.安装Homebrew（未安装的用户）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. 安装依赖
bash
brew install python-tk
pip3 install -r requirements-mac.txt
python3 PassKey.py
⚠️Mac 坑点：
文件拖拽失效：系统设置 → 隐私与安全性 → 辅助功能，给终端开启权限
M 系列芯片必须使用 tkinterdnd2‑universal，普通 tkinterdnd2 会报错
🛠️本地打包生成 PassKey.app
bash
chmod +x build_mac.sh
./build_mac.sh
打包产物在 dist/PassKey.app
Mac 安全隔离，运行前必须解除隔离：
bash
xattr -dr com.apple.quarantine dist/PassKey.app
open dist/PassKey.app
📖使用教程
拖拽文件进窗口，或点击导入；文本框可直接输入文字加密
点击加密，设置口令
加密后导出密文 txt、密钥 txt，两者务必保存
解密：选择密文 txt + 密钥 txt，输入口令，导出原始文件
解密三要素：密文 txt + 密钥 txt + 加密口令，缺一不可
⚠️安全声明
遗忘口令无法恢复数据
Beta 版本，macOS 存在权限、拖拽兼容性问题
禁止用于非法加密行为
📁目录文件
PassKey.py：主程序源码
app.png：图标
build_mac.sh：Mac 本地打包脚本
requirements‑mac.txt：mac python 依赖
README.md：本文档
plaintext

---

### 上传说明
1. 新建仓库文件夹：`v1.1.1-beta-for-macos`
2. 上传5个文件：
    - PassKey.py（上一轮完整代码）
    - build_mac.sh
    - requirements‑mac.txt
    - README.md
    - app.png（直接复用Linux版本的图片，不用改）

### 根目录主README追加跳转链接（复制）
```markdown
👉 [Linux Beta版本 v1.1.1-beta-for-Linux](./v1.1.1-beta-for-Linux/README.md)
👉 [macOS Beta版本 v1.1.1-beta-for-macos](./v1.1.1-beta-for-macos/README.md)