#!/bin/bash
echo "====================================="
echo "PassKey v1.1.1-beta-for-Linux 打包脚本"
echo "====================================="

# 安装打包依赖
pip3 install pyinstaller pillow tkinterdnd2

# 开始打包
pyinstaller --onefile --noconsole PassKey.py

echo ""
echo "✅打包完成！"
echo "可执行文件在 dist/ 目录内"
echo "运行命令: ./dist/PassKey"