import sys
import time
import threading
import numpy as np
import pygame
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
                             QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import os
import ctypes

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("bt.antishutdown")
except:
    pass

pygame.mixer.init()

class AntiSleepApp(QMainWindow):
    update_countdown_ui = pyqtSignal(str)
    update_tray_icon = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("蓝牙音箱防休眠")
        self.setFixedSize(460, 440)

        self.is_running = False
        self.is_playing = False
        self.remaining_seconds = 0
        self.interval = 120
        self.duration = 1
        self.use_custom_file = False
        self.audio_file = ""

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.on_countdown_tick)

        self.tray_icon = None
        self.tray_thread = None

        self.init_ui()
        self.update_countdown_ui.connect(self.update_countdown_label)
        self.update_tray_icon.connect(self.refresh_tray_icon)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(14)
        layout.setContentsMargins(24,24,24,24)

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("循环间隔（秒）："))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 3600)
        self.interval_spin.setValue(300)
        interval_layout.addWidget(self.interval_spin)
        layout.addLayout(interval_layout)

        cd_layout = QHBoxLayout()
        cd_layout.addWidget(QLabel("状态提示："))
        self.countdown_label = QLabel("未运行")
        self.countdown_label.setStyleSheet("font-size:15px; font:bold; color:#0066cc;")
        cd_layout.addWidget(self.countdown_label)
        layout.addLayout(cd_layout)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("发声模式："))
        self.btn_tone = QPushButton("纯频率")
        self.btn_file = QPushButton("音频文件")
        self.btn_tone.setCheckable(True)
        self.btn_file.setCheckable(True)
        self.btn_tone.setChecked(True)
        self.btn_tone.clicked.connect(lambda: self.set_mode(False))
        self.btn_file.clicked.connect(lambda: self.set_mode(True))
        mode_layout.addWidget(self.btn_tone)
        mode_layout.addWidget(self.btn_file)
        layout.addLayout(mode_layout)

        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("纯音频率（Hz）："))
        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(20,20000)
        self.freq_spin.setValue(20)
        freq_layout.addWidget(self.freq_spin)
        layout.addLayout(freq_layout)

        dur_layout = QHBoxLayout()
        dur_layout.addWidget(QLabel("纯音时长（秒）："))
        self.dur_spin = QDoubleSpinBox()
        self.dur_spin.setRange(0.1,10)
        self.dur_spin.setSingleStep(0.1)
        self.dur_spin.setValue(1)
        dur_layout.addWidget(self.dur_spin)
        layout.addLayout(dur_layout)

        self.file_label = QLabel("未选择音频文件")
        self.file_label.setStyleSheet("color:gray;")
        layout.addWidget(self.file_label)

        pause_layout = QHBoxLayout()
        self.pause_btn = QPushButton("暂停播放")
        self.resume_btn = QPushButton("继续播放")
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_audio)
        self.resume_btn.clicked.connect(self.resume_audio)
        pause_layout.addWidget(self.pause_btn)
        pause_layout.addWidget(self.resume_btn)
        layout.addLayout(pause_layout)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始运行")
        self.stop_btn = QPushButton("停止全部")
        self.stop_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_task)
        self.stop_btn.clicked.connect(self.stop_task)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        self.status_label = QLabel("状态：未运行")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def set_mode(self, use_file):
        self.use_custom_file = use_file
        self.btn_tone.setChecked(not use_file)
        self.btn_file.setChecked(use_file)
        self.freq_spin.setEnabled(not use_file)
        self.dur_spin.setEnabled(not use_file)
        if use_file:
            self.choose_file()

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择音频", "", "*.wav *.mp3 *.ogg *.flac")
        if path:
            self.audio_file = path
            self.file_label.setText(os.path.basename(path))
            self.file_label.setStyleSheet("color:green;")

    def create_icon_with_text(self, text=""):
        img = Image.new("RGB", (64,64), color=(0,100,200))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arialbd.ttf", 36)
        except:
            font = ImageFont.load_default(size=36)
        if text:
            bbox = draw.textbbox((0,0), text, font=font)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
            draw.text(((64-w)//2, (64-h)//2-2), text, fill="white", font=font)
        return img

    def refresh_tray_icon(self):
        if not self.tray_icon: return
        if self.is_playing:
            txt = "播"
        elif self.is_running:
            txt = str(self.remaining_seconds)
        else:
            txt = ""
        self.tray_icon.icon = self.create_icon_with_text(txt)

    def create_tray(self):
        menu = (
            item("显示窗口", self.show),
            item("开始", self.start_task),
            item("停止", self.stop_task),
            item("退出", self.quit_app)
        )
        self.tray_icon = pystray.Icon("bt_anti_sleep", self.create_icon_with_text(""), "蓝牙防休眠", menu)
        self.tray_icon.run()

    # ================== 主循环逻辑 ==================
    def start_task(self):
        self.interval = self.interval_spin.value()
        if self.use_custom_file and not self.audio_file:
            QMessageBox.warning(self, "提示", "请先选择音频文件")
            return

        self.is_running = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("状态：运行中")
        self.status_label.setStyleSheet("color:green;")

        if self.use_custom_file:
            self.pause_btn.setEnabled(True)

        self.play_and_wait()

    def play_and_wait(self):
        if not self.is_running:
            return

        # 播放
        if self.use_custom_file:
            self.play_file_full()
        else:
            self.play_tone()

        # 倒计时
        self.remaining_seconds = self.interval
        self.countdown_timer.start(1000)
        self.update_tray_icon.emit()

    def on_countdown_tick(self):
        if not self.is_running:
            self.countdown_timer.stop()
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_countdown_ui.emit(f"倒计时 {self.remaining_seconds} 秒")
        else:
            self.countdown_timer.stop()
            self.play_and_wait()  # 倒计时结束 → 再次播放

        self.update_tray_icon.emit()

    # ================== 纯音播放 ==================
    def play_tone(self):
        self.update_countdown_ui.emit("播放纯音")
        self.is_playing = True
        self.update_tray_icon.emit()

        def run():
            try:
                freq = self.freq_spin.value()
                dur = self.dur_spin.value()
                sr = 44100
                t = np.linspace(0, dur, int(sr * dur), False)
                wave = np.sin(2 * np.pi * freq * t) * 32767
                stereo = np.column_stack([wave, wave]).astype(np.int16)
                snd = pygame.sndarray.make_sound(stereo)
                snd.play()
                time.sleep(dur)
                snd.stop()
            except Exception as e:
                print(e)
            finally:
                self.is_playing = False
                self.update_tray_icon.emit()

        threading.Thread(target=run, daemon=True).start()

    # ================== 文件完整播放 ==================
    def play_file_full(self):
        if not self.is_running:
            return
        self.is_playing = True
        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.update_countdown_ui.emit("播放音频文件中")
        self.update_tray_icon.emit()

        def run():
            try:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and self.is_playing and self.is_running:
                    time.sleep(0.2)
                pygame.mixer.music.stop()
            except Exception as e:
                print(e)
            finally:
                self.is_playing = False
                self.pause_btn.setEnabled(False)
                self.resume_btn.setEnabled(False)
                self.update_tray_icon.emit()

        threading.Thread(target=run, daemon=True).start()

    def pause_audio(self):
        if self.use_custom_file and self.is_playing:
            pygame.mixer.music.pause()
            self.pause_btn.setEnabled(False)
            self.resume_btn.setEnabled(True)

    def resume_audio(self):
        if self.use_custom_file:
            pygame.mixer.music.unpause()
            self.pause_btn.setEnabled(True)
            self.resume_btn.setEnabled(False)

    # ================== 停止 ==================
    def stop_task(self):
        self.is_running = False
        self.is_playing = False
        self.countdown_timer.stop()
        pygame.mixer.music.stop()

        self.update_countdown_ui.emit("已停止")
        self.update_tray_icon.emit()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.status_label.setText("状态：已停止")
        self.status_label.setStyleSheet("color:red;")

    def update_countdown_label(self, s):
        self.countdown_label.setText(s)

    def quit_app(self):
        self.stop_task()
        if self.tray_icon:
            self.tray_icon.stop()
        QApplication.quit()

    def closeEvent(self, e):
        if self.is_running:
            e.ignore()
            self.hide()
        else:
            self.quit_app()

def main():
    app = QApplication(sys.argv)
    w = AntiSleepApp()
    w.tray_thread = threading.Thread(target=w.create_tray, daemon=True)
    w.tray_thread.start()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()