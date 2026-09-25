# 🔐 PassKey 通行密钥｜多格式文件加密工具
![PassKey主界面](./screenshots/main_ui.png)
基于Python+Tkinter构建的图形化加密GUI工具，支持文件拖拽、文本/二进制文件加解密，Windows可打包单文件EXE。

> ⚠️ **版本重大警告：V2.0 / v2.1.1 不兼容 v1.0 ~ v1.1.1‑beta 的旧密文、旧密钥！旧版本加密的文件无法使用V2.0及v2.1.1解密。**

> 🔗 **国内镜像仓库(Gitee)：[Gitee‑PassKey‑PassWord](https://gitee.com/WiseWang1013/PassKey-PassWord)**

**✅ 当前最新版本：v2.1.1（Web网页 + Android APK 新增版）**
**✅ Windows桌面正式版本：v2.0（批量加密新版）**
**✅ 历史版本：v1.1（UI美化版）、v1.0（原始基础版）**
**🟡 Beta测试源码版：v1.1.1‑beta‑for‑Linux / v1.1.1‑beta‑for‑Mac**
**💡 版本互通说明：v1.0 / v1.1 / v1.1.1‑beta 之间加密文件双向互通；v2.0、v2.1.1使用全新加密逻辑，与旧版本完全隔离。**

---

## ✨ 核心功能
### 🆕 v2.1.1 新增特性（Web网页与安卓APK版本）
- 基于 **HTML + CSS + JavaScript** 开发Web网页端，浏览器直接打开运行，无需安装任何程序
- 网页源码目录：[`V2.1.1_WEB`](https://github.com/WiseWang1013/PassKey-PassWord/tree/main/V2.1.1_WEB)
- 网页版加密逻辑与PC v2.0保持完全一致，密文、密钥双向互通
- 网页源码可编译打包为 **安卓离线APK** 和 **安卓联网APK**两个版本
- 网页本身可直接作为Windows浏览器联网版使用，支持密钥云端备份、跨设备同步密钥

### 🆕 v2.0 桌面版新增特性
- **批量加密解密**：一次性多选多个文件，全部文件使用同一套密钥
- **统一异或加密**：不再区分文件后缀专属加密策略，支持几乎全部Windows文件格式
- **大文件多文件进度显示**：加密解密实时展示子任务进度
- **无密码加密**：支持口令留空，不设置密码保护
- **加密模式选择**：随机安全密钥(推荐) / 固定测试密钥（仅调试使用）
- **纯白简约全新UI**：左侧操作面板，右侧预览区域
- **使用协议弹窗**：内置版权、免责、版本说明弹窗
- **批量导出解密文件**：自动保留原始文件名与后缀格式

### 旧版本已有功能（v1.x）
- **文本加密解密**：支持手动输入文字内容加密
- **全类型文件加密**：支持图片、文档、压缩包等二进制文件加解密
- **拖拽快速导入**：直接拖拽文件进程序，无需手动选择路径
- **完整导出体系**：独立导出密文、密钥、解密文件
- **各平台本地打包**：用户可在本机打包对应平台可执行程序

> 📌 v2.0桌面版优先维护Windows；Linux、macOS暂不更新新版本，可继续使用旧Beta源码。

---

## 🌐 Web网页版 & 📱 Android APK
> Web网页源码存放目录：[`V2.1.1_WEB`](https://github.com/WiseWang1013/PassKey-PassWord/tree/main/V2.1.1_WEB)，采用 **HTML + CSS + JavaScript** 原生前端开发，全部加解密运算在浏览器本地执行，加密逻辑和PC v2.0保持一致，密文、密钥双向互通。

**🚀 在线直接使用网页版：**
👉 [PassKey v2.1.1 Web在线工具](https://wisewang1013.github.io/PassKey-PassWord/V2.1.1_WEB/index.html)

> 网页源码可编译打包为**安卓离线APK** 和 **安卓联网APK**两个版本；网页本身可直接作为Windows浏览器联网版使用。
> 编译完成的APK安装包，后续会发布到Release页面：👉 [GitHub Release发布页](https://github.com/WiseWang1013/PassKey-PassWord/releases)

### 版本区分
1. **Windows网页联网版（浏览器直接打开）**
    - ✅ 网页直接运行，不用下载EXE，打开上面在线链接即可使用
    - ✅ 具备网络权限，支持密钥云端备份、跨设备同步密钥
    - ✅ 加密算法与v2.0桌面版完全一致，密文互通
2. **Android APK - 离线版（推荐隐私优先）**
    - ❌ 移除全部网络权限，APP完全无法访问互联网
    - ✅ 加密解密全部在手机本地完成，文件、密钥不会上传任何服务器
    - ⚠️ 未签名测试包，安装需开启手机「允许安装未知来源应用」
3. **Android APK - 联网版**
    - ✅ 拥有网络访问权限，支持密钥云端备份同步
    - ⚠️ 联网会产生数据上传，注重隐私建议选择离线APK

> 💡 重要：Web/安卓全部版本，**加密算法与PC v2.0一致，和v1.x旧版本依旧不兼容**！
> 网页功能：支持多文件批量加密、批量解密；自定义密文包、密钥文件名；日志状态实时输出。

---

## 📂 项目文件说明
- [`PassKey.py`](https://github.com/WiseWang1013/PassKey-PassWord/blob/main/PassKey.py)：项目主程序完整源码（v2.0 Windows桌面版）
- [`app.ico`](https://github.com/WiseWang1013/PassKey-PassWord/blob/main/app.ico)：Windows软件自定义图标文件
- [`build.bat`](https://github.com/WiseWang1013/PassKey-PassWord/blob/main/build.bat)：Windows一键打包 EXE 脚本
- [`PassKey.spec`](https://github.com/WiseWang1013/PassKey-PassWord/blob/main/PassKey.spec)：PyInstaller 打包配置文件
- [`hook‑tkinterdnd2.py`](https://github.com/WiseWang1013/PassKey-PassWord/blob/main/hook-tkinterdnd2.py)：拖拽功能专属打包依赖文件（解决打包失效问题）
- [`V2.1.1_WEB/`](https://github.com/WiseWang1013/PassKey-PassWord/tree/main/V2.1.1_WEB) 📂 v2.1.1 Web网页版源码，基于HTML+CSS+JavaScript开发，用于网页在线运行、编译安卓APK
- [`v1.0/`](https://github.com/WiseWang1013/PassKey-PassWord/tree/main/v1.0)：历史原版源码文件夹（保留初代版本）
- [`v1.1.1‑beta‑for‑Linux/`](https://github.com/WiseWang1013/PassKey-PassWord/tree/main/v1.1.1-beta-for-Linux) 📂 Linux专属Beta源码版本（基于v1.1.1，**不包含v2.0/v2.1.1新功能**）
- [`v1.1.1‑beta‑for‑Mac/`](https://github.com/WiseWang1013/PassKey-PassWord/tree/main/v1.1.1-beta-for-Mac) 📂 macOS专属Beta源码版本（基于v1.1.1，**不包含v2.0/v2.1.1新功能**）

👉 [Linux Beta版本 v1.1.1‑beta‑for‑Linux](./v1.1.1_beta_for_Linux)
👉 [macOS Beta版本 v1.1.1‑beta‑for‑Mac](./v1.1.1_beta_for_Mac)

## 📄 项目配套文档
- [版本更新日志 CHANGELOG.md](./CHANGELOG.md)
- [贡献指南 CONTRIBUTING.md](./CONTRIBUTING.md)
- [Bug反馈模板](./.github/ISSUE_TEMPLATE/bug_report.md)
- [功能建议模板](./.github/ISSUE_TEMPLATE/feature_request.md)

---

## 📦 运行环境依赖
Python 3.8 及以上
pip install tkinterdnd2 pyinstaller
Linux /macOS 平台请查看对应 v1.1.1‑beta 版本内 README 安装平台专属依赖，v2.0 桌面版暂不支持 Linux/macOS。

## 🔨 打包教程
Windows（打包独立 EXE，v2.0 桌面版）
安装全部依赖库
直接双击运行 build.bat
打包完成，程序输出在 dist 文件夹
✅ 打包成果：单文件 EXE、带自定义图标、拖拽功能正常可用
⚠️ Linux /macOS：v2.0 桌面版没有适配；v1.1.1‑beta 分支不能 Windows 交叉编译，请在对应系统内本地编译。
📱 Android 打包：使用仓库内 GitHub Actions CI 脚本，自动从 V2.1.1_WEB 网页源码编译离线 APK / 联网 APK。

## 📖 v2.0 完整使用说明（桌面 GUI 版）
运行 PassKey.py 启动软件
批量导入文件：点击【多选待加密文件】，或者直接把文件拖拽进窗口左侧列表。
批量加密
选择加密模式：随机密钥 (推荐) / 固定测试密钥
点击【批量加密全部文件】，输入口令（可以直接确定，不设置密码）
加密完成后，分别导出「密文包」和「统一密钥 txt」，两个文件必须同时保存。
批量解密
点击【批量解密 (密文 + 密钥)】，依次选择 v2 生成的密文包 txt、统一密钥 txt
输入加密时设置的口令（无密码直接确定）
解密完成，点击【批量导出解密文件】，选择保存文件夹，文件会按原始名字、后缀输出。
✅ v2.0 /v2.1.1 解密必备条件（缺一不可）
v2.0/v2.1.1 生成的密文包 txt
v2.0/v2.1.1 生成的统一密钥 txt
加密时设置的通行口令
❗ 无法解密 v1.x 版本生成的密文密钥。

## ⚠️ 重要安全提醒（必读）
通行口令一旦丢失、遗忘，文件永久无法解密，没有找回手段！
本项目仅用于 Python 编程学习、开源练习。
v2.0 桌面版优先适配 Windows 平台；Linux、macOS 仅可使用旧 v1.1.1‑beta 源码，没有 v2 版本。
v2.1.1 Web 网页版、安卓 APK（离线 / 联网）加密算法同 v2.0 桌面版，同样不兼容 v1.x 旧密文。
禁止用来加密重要业务、机密资料，重要文件务必备份原始文件。
安卓 APK 为测试构建包，离线版无网络权限；联网版会支持密钥云端存储。
禁止利用本工具做恶意加密、锁机、勒索等一切违规违法行为。

## 📜 开源说明
本项目采用 MIT 开源协议，仅供学习、参考、二次练习。
任何人都可以查看、学习、修改源码，但禁止商用违规用途。
