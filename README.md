# PassKey-PassWord
基于 Python + Tkinter 开发的Windows图形化加密工具。

## ✨ 功能
- 文本加密 / 解密
- 文件拖拽加密解密
- 支持打包为单文件EXE，自带自定义ICO图标

## 📁 项目文件说明
- `PassKey.py`：主程序源码
- `app.ico`：程序图标
- `build.bat`：一键打包脚本
- `PassKey.spec`：PyInstaller打包配置
- `hook-tkinterdnd2.py`：拖拽功能依赖文件

## 🛠 打包方法
运行 `build.bat`，自动使用PyInstaller打包生成独立exe。

## ⚠️ 提示
本项目仅用于学习演示，请勿用于重要机密文件加密。
