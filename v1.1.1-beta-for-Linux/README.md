# PassKey v1.1.1-beta-for-Linux
🟡 Beta测试版｜**Linux专属版本**
> 本分支仅面向Linux，移除Windows相关格式（bat/cmd），新增sh、conf、systemd service格式支持

## ✨项目简介
基于Python+Tkinter+tkinterdnd2开发的本地图形化加密工具
支持文本、脚本、配置文件、图片、压缩包、音视频等文件加密
支持文件拖拽导入、实时加密进度显示，密文与密钥分开保存

> ⚠️重要提醒：口令一旦丢失，文件无法解密！
> 本项目仅用于编程学习，禁止用于恶意加密、勒索等违规用途。

## 📂支持文件后缀
**文本类：**
txt, py, html, cpp, json, csv, toml, ini, md, js, css, java, go, rs, sh, conf, service

**二进制类：**
png, jpg, gif, docx, zip, rar, 7z, mp3, wav, mp4

## 📦 源码运行（推荐方式）
### Ubuntu / Debian / Linux Mint
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip
pip3 install -r requirements.txt
python3 PassKey.py
Fedora
bash
sudo dnf install python3 python3-tkinter python3-pip
pip3 install -r requirements.txt
python3 PassKey.py
Arch / Manjaro
bash
sudo pacman -S python tk python-pip
pip3 install -r requirements.txt
python3 PassKey.py
🛠️打包为独立 Linux 可执行文件
打包必须在 Linux 系统环境执行，Windows 打包产物不能在 Linux 运行
bash
# 添加脚本执行权限
chmod +x build.sh
# 运行打包脚本
./build.sh
打包完成后，程序位于 dist/PassKey
bash
# 运行打包好的程序
./dist/PassKey
📖 使用教程
启动软件，可以直接拖拽文件进窗口，或者点击导入文件
文本框也可以手动输入文字直接加密
点击【加密文件 / 文本】，设置你的通行口令
加密完成，分别导出密文 txt、密钥 txt，两个文件都需要妥善保存
解密：选择密文 txt、密钥 txt，输入当时设置的口令，解密后导出原始文件
解密三要素缺一不可：密文 txt + 密钥 txt + 你的口令
⚠️安全声明
通行口令遗忘，数据永久无法解密，无找回手段
本项目仅用于学习研究，不保证商业级安全
禁止用于加密他人文件、锁机、勒索等违法行为
Beta 版本，Linux 环境下可能存在兼容性 bug
📁本目录文件说明
PassKey.py：主程序源码
app.png：窗口图标
build.sh：一键打包脚本
requirements.txt：Python 依赖清单
README.md：本文档