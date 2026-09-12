@echo off
chcp 65001
echo ======================================
echo      PassKey-Password EXE打包脚本
echo      AI辅助开发的Python GUI加密工具
echo ======================================
echo.

:: 清理上次打包产生的旧文件
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist *.spec del *.spec

:: 打包：单文件、无黑窗口、自定义ico图标，加载hook修复拖拽功能
pyinstaller -F -w -i app.ico PassKey.py --additional-hooks-dir=.

echo.
echo ✅ 打包成功！生成的 PassKey.exe 在 dist 文件夹中
echo ⚠️  重要提醒：app.ico 必须和 build.bat、PassKey.py 在同一个文件夹！
pause