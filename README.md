# 🔐 PassKey 通行密钥｜多格式文件加密工具
![PassKey主界面](./screenshots/main_ui.png)
基于Python+Tkinter构建的跨平台图形化加密GUI工具，支持文件拖拽、文本/二进制文件加解密，Windows可打包单文件EXE，附带Linux、macOS Beta源码版。

**✅ 当前Windows最新版本：v1.1（UI美化版）**
**✅ 历史版本：v1.0（原始基础版）**
**🟡 Beta测试源码版：v1.1.1-beta-for‑Linux / v1.1.1-beta-for-Mac**
**💡 版本说明：v1.1仅优化界面，底层加密算法完全不变；v1.0 / v1.1 / Beta版加密文件双向完全互通！**

---

## ✨ 核心功能
- **文本加密解密**：支持手动输入文字内容加密
- **全类型文件加密**：支持图片、文档、压缩包等二进制文件加解密
- **拖拽快速导入**：直接拖拽文件进程序，无需手动选择路径
- **智能加密策略**：不同文件采用适配的加密处理逻辑
- **进度条可视化**：加密和解密过程实时显示进度
- **深色科技UI**：v1.1全新美化界面、彩色功能按钮、自适应窗口
- **完整导出体系**：独立导出密文、密钥、解密文件
- **各平台本地打包**：用户可在本机打包对应平台可执行程序

---

## 📂 项目文件说明
- `PassKey.py`：项目主程序完整源码
- `app.ico`：Windows软件自定义图标文件
- `build.bat`：Windows一键打包 EXE 脚本
- `PassKey.spec`：PyInstaller 打包配置文件
- `hook-tkinterdnd2.py`：拖拽功能专属打包依赖文件（解决打包失效问题）
- `v1.0/`：历史原版源码文件夹（保留初代版本）
- `v1.1.1-beta-for-Linux/` 📂 Linux专属Beta源码版本
- `v1.1.1-beta-for-Mac/` 📂 macOS专属Beta源码版本

👉 [Linux Beta版本 v1.1.1-beta-for-Linux](./v1.1.1-beta-for-Linux/README.md)
👉 [macOS Beta版本 v1.1.1-beta-for-Mac](./v1.1.1-beta-for-Mac/README.md)

## 📄 项目配套文档
- [版本更新日志 CHANGELOG.md](./CHANGELOG.md)
- [贡献指南 CONTRIBUTING.md](./CONTRIBUTING.md)
- [Bug反馈模板](./.github/ISSUE_TEMPLATE/bug_report.md)
- [功能建议模板](./.github/ISSUE_TEMPLATE/feature_request.md)

---

## 📦 运行环境依赖
Python 3.8 及以上
```bash
pip install tkinterdnd2 pyinstaller
Linux /macOS 平台请查看对应版本内 README 安装平台专属依赖。
🔨 打包教程
Windows（打包独立 EXE）
安装全部依赖库
直接双击运行 build.bat
打包完成，程序输出在 dist 文件夹
✅ 打包成果：单文件 EXE、带自定义图标、无额外依赖，拖拽功能正常可用
⚠️ Linux / macOS：不能在 Windows 交叉编译，请在对应系统内运行打包脚本本地编译。
📖 完整使用说明
运行 PassKey.py 启动软件，支持两种工作模式：
1. 文本模式（手动文字加密）
在文本框输入内容
设置通行口令，点击加密
导出密文文件与密钥文件保存
2. 文件模式（任意文件加密）
点击导入 或者 直接拖拽文件到窗口
设置通行口令，执行加密
分别保存密文 txt 与密钥 txt
✅ 解密必须三样齐全（缺一不可）
加密生成的 密文文件
加密生成的 密钥文件
加密时设置的 通行口令
⚠️ 重要安全提醒（必读）
通行口令一旦丢失、遗忘，文件永久无法解密，没有找回手段！
本项目仅用于 Python 编程学习、开源练习。
禁止用于加密隐私、机密、企业重要数据。
Windows 为主适配平台；Linux、macOS 仅 Beta 源码版本，存在权限、拖拽兼容问题，需要手动配置系统权限。
暂无安卓版本。
禁止利用本工具做恶意加密、勒索等违规违法行为。
📜 开源说明
本项目采用 MIT 开源协议，仅供学习、参考、二次练习。
任何人都可以查看、学习、修改源码，但禁止商用违规用途。
📌 版本更新日志
v1.1（Windows 正式版）
全新深色科技风 UI 界面
彩色功能按钮、状态文字动态变色
优化布局、支持窗口自由缩放
优化代码字体与文本框视觉效果
核心加密算法完全不变，完美兼容 v1.0
v1.1.1‑beta‑for‑Linux｜v1.1.1‑beta‑for‑Mac
适配 Linux/macOS 平台，移除 Windows 专属 bat/cmd 文件
新增平台特有配置文件格式支持
提供对应系统源码、打包脚本，不提供预编译二进制包，用户本地自行构建
底层加密算法与 v1.0/v1.1 完全互通
v1.0（初始版本）
实现全部核心加解密功能
支持多格式文件、拖拽加密、进度条
支持一键打包 Windows EXE
