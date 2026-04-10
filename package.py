# build.py - 蓝牙防休眠工具一键打包脚本
import os
import sys
import subprocess

def build_exe():
    print("=" * 50)
    print("  蓝牙音箱防休眠工具 - 打包程序")
    print("=" * 50)

    # 安装依赖（如果没装）
    try:
        import PyQt5
        import pygame
        import numpy
        import pystray
        import pillow
    except:
        print("\n正在安装打包依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "pygame", "numpy", "pystray", "pillow", "pyqt5"])

    # PyInstaller 打包命令（核心）
    cmd = [
        "pyinstaller",
        "--onefile",                  # 单文件
        "--windowed",                 # 无控制台窗口
        "--noconsole",
        "--name", "蓝牙音箱防休眠工具",  # 生成exe名称
        "--icon", "NONE",             # 无图标（你有图标可以替换）
        "sound.py"                    # 要打包的主程序
    ]

    print("\n开始打包...\n")
    subprocess.run(cmd)

    print("\n" + "=" * 50)
    print("✅ 打包完成！")
    print("📁 输出位置：dist 文件夹里面")
    print("▶  直接双击 蓝牙音箱防休眠工具.exe 运行")
    print("=" * 50)

if __name__ == '__main__':
    build_exe()