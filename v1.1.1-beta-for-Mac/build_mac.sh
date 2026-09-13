#!/bin/bash
echo "====================================="
echo "PassKey v1.1.1-beta-for-macOS 本地打包脚本"
echo "====================================="

pip3 install pyinstaller pillow tkinterdnd2-universal

# --windowed macOS图形程序，不弹出终端控制台
pyinstaller --windowed --name PassKey PassKey.py

echo ""
echo "✅打包完成！输出目录 dist/PassKey.app"
echo "❗macOS安全隔离，运行前必须执行：xattr -dr com.apple.quarantine dist/PassKey.app"
echo "启动命令：open dist/PassKey.app"