# 蓝牙音箱防休眠工具（Bluetooth Speaker Anti-Sleep Tool）软件介绍

# 中文介绍

## 一、软件概述

蓝牙音箱防休眠工具（Bluetooth Speaker Anti-Sleep Tool）是一款基于Python开发的图形化工具，专为解决蓝牙音箱闲置时自动关机（休眠）的问题而设计。软件支持后台常驻系统托盘，可通过可视化界面灵活设置参数，实现定时播放声音（纯音/自定义音频文件），全程低资源占用、静默运行，不打扰日常使用。

核心优势：界面简洁、操作便捷，支持秒级定时控制，托盘实时显示倒计时，两种发声模式自由切换，适配所有主流蓝牙音箱设备，无需复杂配置，双击即可运行。

## 二、核心功能

- **双发声模式**：支持纯音频率模式（可调节频率）和自定义音频文件模式（支持MP3/WAV/OGG/FLAC格式），满足不同场景需求。

- **秒级定时控制**：循环间隔可精确到秒（1秒~1小时），可自由设置，适配不同蓝牙音箱的休眠时长。

- **实时倒计时显示**：系统托盘和软件界面同步显示倒计时，播放时托盘显示“播”字，直观了解下次播放时间。

- **音频文件控制**：音频文件模式支持暂停/继续播放，确保每次完整播放音频后再进入倒计时间隔，不打断音频播放。

- **后台常驻**：关闭软件窗口后，程序自动最小化到系统托盘，后台持续运行，不占用前台窗口资源。

- **低资源占用**：运行时仅占用少量CPU和内存，静默运行不影响电脑正常使用。

- **图形化界面**：操作简单，参数设置直观，无需命令行操作，适合所有用户使用。

## 三、安装与运行

### 3.1 环境依赖

运行该软件需要安装以下Python依赖包，可通过命令行一键安装：

```bash
pip install PyQt5 pygame numpy pystray pillow
```

### 3.2 直接运行

1. 下载项目中的 `sound.py` 文件（主程序）；

2. 确保已安装上述依赖包；

3. 双击 `sound.py` 或通过命令行运行 `python sound.py`，即可启动软件。

### 3.3 打包为EXE（可选）

若需要生成可直接双击运行的EXE文件（无需安装Python环境），可使用项目中的 `build.py`打包脚本：

1. 将 `build.py` 与 `sound.py` 放在同一文件夹；

2. 运行 `build.py`，脚本会自动安装打包依赖并生成EXE文件；

3. 打包完成后，在 `dist` 文件夹中找到 `蓝牙音箱防休眠工具.exe`，双击即可运行。

自定义图标：将 `icon.ico` 放在同一目录，修改 `build.py` 中 `--icon` 参数为 `"icon.ico"` 即可。

## 四、使用说明

### 4.1 参数设置

- 循环间隔（秒）：设置两次播放之间的时间间隔，建议设置60~180秒（适配大多数蓝牙音箱的休眠时间）；

- 纯音频率（Hz）：仅纯音模式有效，范围20~20000Hz，建议440~1000Hz（人耳无明显不适感，唤醒效果好）；

- 纯音时长（秒）：仅纯音模式有效，范围0.1~10秒，建议0.5~1秒（足够唤醒音箱，不打扰使用）；

- 音频文件：仅音频文件模式有效，点击“音频文件”按钮可选择本地音频文件，支持MP3/WAV/OGG/FLAC格式。

### 4.2 操作步骤

1. 启动软件后，选择发声模式（纯音频率/音频文件）；

2. 根据需求设置对应参数（音频文件模式需先选择音频文件）；

3. 点击“开始运行”，软件开始工作，托盘显示倒计时，界面显示当前状态；

4. 音频文件模式下，播放期间可点击“暂停播放”暂停，点击“继续播放”恢复；

5. 点击“停止全部”可停止运行，参数恢复可编辑状态；

6. 关闭软件窗口，程序最小化到系统托盘，右键托盘图标可进行显示窗口、开始/停止、退出操作。

## 五、常见问题

- Q：托盘图标不显示倒计时？
A：检查是否安装了pillow依赖，若托盘被系统隐藏，点击右下角箭头即可找到。

- Q：纯音模式无声音？
A：检查电脑音量和蓝牙音箱连接状态，确认频率设置在20~20000Hz范围内。

- Q：音频文件无法播放？
A：确认音频文件格式正确（支持MP3/WAV/OGG/FLAC），文件路径无中文或特殊字符。

- Q：软件无法启动？
A：检查是否安装了所有依赖包，Python版本建议3.7及以上。

## 六、技术栈

开发语言：Python 3.7+
核心库：PyQt5（图形化界面）、pygame（音频播放）、numpy（纯音生成）、pystray（系统托盘）、pillow（托盘图标绘制）

# English Introduction

## I. Software Overview

Bluetooth Speaker Anti-Sleep Tool is a Python-based graphical tool designed to solve the problem of automatic shutdown (sleep) of Bluetooth speakers when idle. The software supports resident background in the system tray, allows flexible parameter setting through a visual interface, and realizes timed sound playback (pure tone/custom audio file). It runs silently with low resource consumption and does not interfere with daily use.

Core Advantages: Simple interface, easy operation, second-level timing control, real-time countdown display in the tray, free switching between two sound modes, compatible with all mainstream Bluetooth speaker devices, no complex configuration, and can be run with a double click.

## II. Core Features

- **Dual Sound Modes**: Supports pure tone frequency mode (adjustable frequency) and custom audio file mode (supports MP3/WAV/OGG/FLAC formats) to meet different scenario needs.

- **Second-Level Timing Control**: The cycle interval can be accurate to seconds (1 second ~ 1 hour), which can be freely set to adapt to the sleep duration of different Bluetooth speakers.

- **Real-Time Countdown Display**: The system tray and software interface display the countdown synchronously. When playing, the tray displays the character "Play" to intuitively know the next playback time.

- **Audio File Control**: The audio file mode supports pause/resume playback, ensuring that each audio is played completely before entering the countdown interval without interrupting the audio playback.

- **Background Resident**: After closing the software window, the program is automatically minimized to the system tray and continues to run in the background without occupying foreground window resources.

- **Low Resource Consumption**: It only occupies a small amount of CPU and memory during operation, and runs silently without affecting the normal use of the computer.

- **Graphical Interface**: Simple operation, intuitive parameter setting, no command line operation, suitable for all users.

## III. Installation and Operation

### 3.1 Dependencies

To run the software, you need to install the following Python dependency packages, which can be installed with one command:

```bash
pip install PyQt5 pygame numpy pystray pillow
```

### 3.2 Run Directly

1. Download the `sound.py` file (main program) in the project;

2. Ensure that the above dependency packages are installed;

3. Double-click `sound.py` or run `python sound.py` through the command line to start the software.

### 3.3 Package as EXE (Optional)

If you need to generate an EXE file that can be run directly with a double click (without installing the Python environment), you can use the `build.py` packaging script in the project:

1. Place `build.py` and `sound.py` in the same folder;

2. Run `build.py`, the script will automatically install the packaging dependencies and generate the EXE file;

3. After packaging, find `Bluetooth Speaker Anti-Sleep Tool.exe` in the `dist` folder and double-click to run it.

Custom Icon: Place `icon.ico` in the same directory, and modify the `--icon` parameter in `build.py` to `"icon.ico"`.

## IV. User Guide

### 4.1 Parameter Setting

- Cycle Interval (Seconds): Set the time interval between two plays, it is recommended to set 60~180 seconds (adapts to the sleep time of most Bluetooth speakers);

- Pure Tone Frequency (Hz): Only valid in pure tone mode, range 20~20000Hz, it is recommended to set 440~1000Hz (no obvious discomfort to human ears, good wake-up effect);

- Pure Tone Duration (Seconds): Only valid in pure tone mode, range 0.1~10 seconds, it is recommended to set 0.5~1 second (enough to wake up the speaker without disturbing use);

- Audio File: Only valid in audio file mode, click the "Audio File" button to select a local audio file, supporting MP3/WAV/OGG/FLAC formats.

### 4.2 Operation Steps

1. After starting the software, select the sound mode (Pure Tone Frequency/Audio File);

2. Set the corresponding parameters according to needs (you need to select an audio file first in audio file mode);

3. Click "Start Running", the software starts working, the tray displays the countdown, and the interface displays the current status;

4. In audio file mode, you can click "Pause Play" to pause during playback, and click "Resume Play" to resume;

5. Click "Stop All" to stop running, and the parameters return to the editable state;

6. Close the software window, the program is minimized to the system tray, and you can right-click the tray icon to display the window, start/stop, and exit.

## V. Frequently Asked Questions (FAQs)

- Q: The tray icon does not display the countdown?
A: Check if the pillow dependency is installed. If the tray is hidden by the system, click the arrow in the lower right corner to find it.

- Q: No sound in pure tone mode?
A: Check the computer volume and Bluetooth speaker connection status, and confirm that the frequency is set within the range of 20~20000Hz.

- Q: Audio files cannot be played?
A: Confirm that the audio file format is correct (supports MP3/WAV/OGG/FLAC), and the file path has no Chinese or special characters.

- Q: The software cannot start?
A: Check if all dependency packages are installed, and the Python version is recommended to be 3.7 or above.

## VI. Technology Stack

Development Language: Python 3.7+
Core Libraries: PyQt5 (Graphical Interface), pygame (Audio Playback), numpy (Pure Tone Generation), pystray (System Tray), pillow (Tray Icon Drawing)
