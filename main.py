import sys
import os
import threading
import time
from pathlib import Path

# GUI
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                               QFileDialog, QComboBox, QLineEdit, QProgressBar, 
                               QTextEdit, QFrame, QMessageBox, QGridLayout, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect, QCheckBox, QSpinBox)
from PySide6.QtCore import Qt, Signal, QObject, Slot, QSize, QTimer
from PySide6.QtGui import QIcon, QFont, QPixmap, QImage, QAction, QColor, QTextCursor

# Plotting
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Logic
import torch
from PIL import Image
from torchvision import transforms
import numpy as np

# Internal
from src.dataset import DatasetHandler
from src.model import ModelFactory
from src.trainer import Trainer, TrainingCallback
from src.exporter import ModelExporter
from src.ui_styles import StyleSheet
from src.ui_components import PremiumButton, StatusPill, KPICard

# --- Logging (Signal Only) ---
class LogSignal(QObject):
    log_emit = Signal(str)

# --- UI Pages ---

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet(StyleSheet.SIDEBAR)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Header
        header = QFrame()
        header.setFixedHeight(120)
        hl = QVBoxLayout(header)
        hl.setAlignment(Qt.AlignCenter)
        hl.setSpacing(5)
        
        lbl = QLabel("INSPEC")
        lbl.setFont(QFont("Segoe UI", 24, QFont.Bold))
        lbl.setStyleSheet(f"color: {StyleSheet.TEXT_MAIN};")
        
        sub = QLabel("PRO ENTERPRISE")
        sub.setFont(QFont("Segoe UI", 9, QFont.Bold))
        sub.setStyleSheet(f"color: {StyleSheet.ACCENT_PRIMARY}; letter-spacing: 2px;")
        
        hl.addWidget(lbl)
        hl.addWidget(sub)
        layout.addWidget(header)
        
        # Navigation
        self.buttons = []
        self.add_btn("Dataset", "📁", 0, layout)
        self.add_btn("Training", "⚡", 1, layout)
        self.add_btn("Inference", "🎯", 2, layout)
        
        layout.addStretch()
        
        # Device Status
        dev_frame = QFrame()
        dev_frame.setStyleSheet("background: rgba(255,255,255,0.03); border-radius: 8px; margin: 15px; border: 1px solid #30363d;")
        dl = QVBoxLayout(dev_frame)
        
        self.dev_lbl = QLabel("Checking Device...")
        self.dev_lbl.setStyleSheet("color: #8b949e; font-size: 11px;")
        self.dev_lbl.setAlignment(Qt.AlignCenter)
        dl.addWidget(self.dev_lbl)
        
        layout.addWidget(dev_frame)

    def add_btn(self, text, icon, idx, layout):
        btn = QPushButton(f"  {icon}   {text}")
        btn.setFixedHeight(50)
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(StyleSheet.NAV_BUTTON)
        layout.addWidget(btn)
        self.buttons.append(btn)
        
    def update_device(self):
        if torch.cuda.is_available():
            d = torch.cuda.get_device_name(0)
            self.dev_lbl.setText(f"🚀 CUDA ACTIVE\n{d}")
            self.dev_lbl.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 10px;")
        else:
            self.dev_lbl.setText("⚠️ CPU MODE\nGPU Not Detected")
            self.dev_lbl.setStyleSheet("color: #f1c40f; font-weight: bold; font-size: 10px;")

class DataPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50,50,50,50)
        layout.setSpacing(25)
        
        # Header
        h = QLabel("Dataset Configuration")
        h.setFont(QFont("Segoe UI Light", 26))
        h.setStyleSheet(f"color: {StyleSheet.TEXT_MAIN};")
        layout.addWidget(h)
        
        # Controls Card
        card = QFrame()
        card.setStyleSheet(f"background: {StyleSheet.BG_SURFACE}; border-radius: 10px; border: 1px solid #30363d;")
        cl = QHBoxLayout(card)
        cl.setContentsMargins(20,20,20,20)
        
        self.path_in = QLineEdit()
        self.path_in.setPlaceholderText("Path to dataset root folder...")
        self.path_in.setStyleSheet(StyleSheet.INPUT_FIELD)
        self.path_in.setFixedHeight(40)
        
        btn_br = PremiumButton("Browse", primary=False)
        btn_br.clicked.connect(self.browse)
        
        btn_ld = PremiumButton("Load Dataset")
        btn_ld.clicked.connect(self.load_safe)
        
        cl.addWidget(self.path_in, stretch=1)
        cl.addWidget(btn_br)
        cl.addWidget(btn_ld)
        layout.addWidget(card)

        # Content
        self.info = QLabel("Please load a dataset to begin.")
        self.info.setStyleSheet("color: #8b949e; font-size: 14px; margin-left: 5px;")
        layout.addWidget(self.info)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.grid_w = QWidget()
        self.grid = QGridLayout(self.grid_w)
        self.grid.setSpacing(15)
        self.scroll.setWidget(self.grid_w)
        layout.addWidget(self.scroll)

    def browse(self):
        d = QFileDialog.getExistingDirectory(self, "Select Folder")
        if d: self.path_in.setText(d)

    def load_safe(self):
        p = self.path_in.text()
        if not p: return
        
        self.info.setText("Scanning directory...")
        QApplication.processEvents()
        
        try:
            h = DatasetHandler({})
            h.load_local_dataset(p)
            self.app.data = h
            self.info.setText(f"✓ Loaded {len(h.file_paths)} images across {len(h.classes)} classes: {', '.join(h.classes)}")
            self.info.setStyleSheet("color: #2ecc71; font-weight: bold;")
            self.populate_grid(h)
            
            # Auto Init Model
            if not self.app.model:
                try:
                    self.app.model = ModelFactory.get_model("MobileNetV2", len(h.classes))
                    print("Auto-Initialized Model Architecture")
                except: pass
                
        except Exception as e:
            self.info.setText(f"Error: {e}")
            self.info.setStyleSheet("color: #e74c3c")

    def populate_grid(self, h):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        samples = h.get_sample_images(12)
        if not samples: return
        
        for i, (path, cls) in enumerate(samples):
            try:
                card = QFrame()
                card.setStyleSheet("background: #21262d; border-radius: 8px; border: 1px solid #30363d;")
                card.setFixedSize(140, 160)
                l = QVBoxLayout(card)
                l.setContentsMargins(10,10,10,10)
                
                pix = QPixmap(path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img = QLabel()
                img.setPixmap(pix)
                img.setAlignment(Qt.AlignCenter)
                
                txt = QLabel(cls)
                txt.setAlignment(Qt.AlignCenter)
                txt.setStyleSheet("color: #8b949e; font-size: 11px; font-weight: 600; margin-top: 5px;")
                
                l.addWidget(img)
                l.addWidget(txt)
                self.grid.addWidget(card, i//4, i%4)
            except: pass

class TrainingPage(QWidget):
    update_signal = Signal(dict)
    log_signal = Signal(str)

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.update_signal.connect(self.on_update, Qt.QueuedConnection)
        self.log_signal.connect(self.on_log, Qt.QueuedConnection)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(20)
        
        # --- Left Col (Config) ---
        l_col = QVBoxLayout()
        l_col.setSpacing(15)
        
        # Header
        header_lbl = QLabel("TRAINING CONFIG")
        header_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #00d2ff; margin-bottom: 5px;")
        l_col.addWidget(header_lbl)
        
        # KPI Cards
        kpi_row = QHBoxLayout()
        self.kpi_best = KPICard("Best Acc", "0.0%")
        self.kpi_time = KPICard("Time", "0s")
        kpi_row.addWidget(self.kpi_best)
        kpi_row.addWidget(self.kpi_time)
        l_col.addLayout(kpi_row)
        
        self.c_model = QComboBox()
        self.c_model.addItems(["MobileNetV2", "ResNet50", "EfficientNetB0"])
        self.c_model.setStyleSheet(StyleSheet.COMBO_BOX)
        l_col.addWidget(QLabel("Architecture"))
        l_col.addWidget(self.c_model)
        
        self.in_ep = QLineEdit("20")
        self.in_ep.setStyleSheet(StyleSheet.INPUT_FIELD)
        self.in_ep.setToolTip("Number of training epochs (recommended: 20-50)")
        l_col.addWidget(QLabel("Epochs"))
        l_col.addWidget(self.in_ep)
        
        self.in_bs = QLineEdit("32")
        self.in_bs.setStyleSheet(StyleSheet.INPUT_FIELD)
        l_col.addWidget(QLabel("Batch Size"))
        l_col.addWidget(self.in_bs)
        
        self.in_lr = QLineEdit("0.001")
        self.in_lr.setStyleSheet(StyleSheet.INPUT_FIELD)
        l_col.addWidget(QLabel("Learning Rate"))
        l_col.addWidget(self.in_lr)
        
        self.btn_train = PremiumButton("START TRAINING")
        self.btn_train.clicked.connect(self.start)
        l_col.addWidget(self.btn_train)
        
        self.btn_export = PremiumButton("EXPORT ONNX", primary=False)
        self.btn_export.clicked.connect(self.export_model)
        self.btn_export.setEnabled(False) 
        l_col.addWidget(self.btn_export)
        
        # Early Stopping Controls
        early_stop_frame = QFrame()
        early_stop_frame.setStyleSheet("background: rgba(0, 210, 255, 0.05); border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid rgba(0, 210, 255, 0.2);")
        es_layout = QVBoxLayout(early_stop_frame)
        es_layout.setSpacing(8)
        
        self.chk_early_stop = QCheckBox("Enable Early Stopping")
        self.chk_early_stop.setChecked(False)
        self.chk_early_stop.setStyleSheet("QCheckBox { color: #00d2ff; font-size: 12px; font-weight: bold; }")
        self.chk_early_stop.setToolTip("Stop training when validation accuracy stops improving")
        es_layout.addWidget(self.chk_early_stop)
        
        patience_layout = QHBoxLayout()
        patience_label = QLabel("Patience:")
        patience_label.setStyleSheet("color: #8b949e; font-size: 11px;")
        self.spin_patience = QSpinBox()
        self.spin_patience.setRange(3, 30)
        self.spin_patience.setValue(10)
        self.spin_patience.setSuffix(" epochs")
        self.spin_patience.setStyleSheet(StyleSheet.INPUT_FIELD + " QSpinBox { max-width: 120px; }")
        self.spin_patience.setToolTip("Number of epochs to wait for improvement before stopping")
        patience_layout.addWidget(patience_label)
        patience_layout.addWidget(self.spin_patience)
        patience_layout.addStretch()
        es_layout.addLayout(patience_layout)
        
        l_col.addWidget(early_stop_frame)
        
        # Abort Training Button
        self.btn_abort = PremiumButton("ABORT TRAINING", primary=False)
        self.btn_abort.clicked.connect(self.abort_training)
        self.btn_abort.setEnabled(False)
        self.btn_abort.setStyleSheet("QPushButton { background: #8b0000; } QPushButton:hover { background: #a52a2a; }")
        l_col.addWidget(self.btn_abort)
        
        self.pill = StatusPill("IDLE")
        l_col.addWidget(self.pill)
        
        l_col.addStretch()
        layout.addLayout(l_col, stretch=1)
        
        # --- Right Col (Plots) ---
        r_col = QVBoxLayout()
        r_col.setSpacing(15)
        
        # Charts
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig.patch.set_facecolor(StyleSheet.BG_SURFACE)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)
        r_col.addWidget(self.canvas, stretch=2)
        
        # Status Section
        s_frame = QFrame()
        s_frame.setStyleSheet("background: #0d1117; border-radius: 6px; border: 1px solid #30363d;")
        sl = QVBoxLayout(s_frame)
        sl.setContentsMargins(15,15,15,15)
        
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet("color: #00d2ff; font-weight: bold; font-family: 'Consolas'; font-size: 13px;")
        sl.addWidget(self.status_lbl)
        
        self.pbar = QProgressBar()
        self.pbar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #21262d;
                border-radius: 4px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00d2ff;
                border-radius: 4px;
            }
        """)
        self.pbar.setValue(0)
        sl.addWidget(self.pbar)
        
        r_col.addWidget(s_frame)

        # Console
        lbl_con = QLabel("LIVE LOGS")
        lbl_con.setStyleSheet("font-size: 11px; font-weight: bold; color: #8b949e; margin-top: 5px;")
        r_col.addWidget(lbl_con)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(StyleSheet.CONSOLE)
        r_col.addWidget(self.console, stretch=3)
        
        layout.addLayout(r_col, stretch=4)
        self.style_plots()

    def style_plots(self):
        self.ax.set_facecolor(StyleSheet.BG_SURFACE)
        self.ax.grid(color='#30363d', linestyle=':')
        self.ax.tick_params(colors='#8b949e', labelsize=8)
        for s in self.ax.spines.values(): s.set_color('#30363d')
        self.ax.set_title("Validation Accuracy", color='#e6edf3', fontsize=12, fontweight='bold')
        self.fig.tight_layout()
        self.canvas.draw()

    def start(self):
        if not self.app.data:
            return QMessageBox.warning(self, "Error", "Load Dataset First")
            
        try:
            m = self.c_model.currentText()
            self.app.model = ModelFactory.get_model(m, len(self.app.data.classes))
            
            # Start fresh log
            self.console.clear()
            self.status_lbl.setText("Initializing Training...")
            self.pbar.setValue(0)
            self.on_log("--- STARTING NEW TRAINING SESSION ---")
            
            # Params
            ep = int(self.in_ep.text())
            bs = int(self.in_bs.text())
            lr = float(self.in_lr.text())
            
            # Initialize Trainer with user Params
            self.app.trainer = Trainer(self.app.model) 
            self.app.trainer.set_optimizer("Adam", lr)
            
            # Early Stopping Configuration
            self.app.trainer.use_early_stop = self.chk_early_stop.isChecked()
            self.app.trainer.early_stop_patience = self.spin_patience.value()
            
            if self.app.trainer.use_early_stop:
                self.on_log(f"Early Stopping enabled with patience = {self.app.trainer.early_stop_patience} epochs")
            
            threading.Thread(target=self.worker, args=(ep, bs), daemon=True).start()
            
            self.btn_train.setEnabled(False)
            self.btn_export.setEnabled(False)
            self.btn_abort.setEnabled(True)
            self.pill.set_status("WARN")
            self.pill.setText("TRAINING")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def abort_training(self):
        """User-initiated abort – signals the Trainer to stop."""
        if hasattr(self.app, "trainer") and self.app.trainer:
            self.app.trainer.stop_training = True
            self.on_log("⚠️  Training abort requested by user...")
            self.btn_abort.setEnabled(False)
            self.pill.set_status("WARN")
            self.pill.setText("ABORTING")
            
    def export_model(self):
        if not self.app.model: return
        
        path, _ = QFileDialog.getSaveFileName(self, "Export ONNX", "model.onnx", "ONNX Models (*.onnx)")
        if path:
            try:
                d = os.path.dirname(path)
                out, success = ModelExporter.export_to_onnx(self.app.model, export_path=d)
                if success:
                    if out != path:
                        try:
                            if os.path.exists(path): os.remove(path)
                            os.rename(out, path)
                        except: pass
                    
                    QMessageBox.information(self, "Success", f"Exported to {path}")
                    self.on_log(f"Exported ONNX model to {path}")
                else:
                    QMessageBox.critical(self, "Error", f"Export failed: {out}")
            except Exception as e:
                 QMessageBox.critical(self, "Error", str(e))

    def worker(self, ep, bs):
        start_time = time.time()
        try:
            tr, val, _ = self.app.data.get_data_loaders(bs)
            steps_per_epoch = len(tr)
            total_steps = ep * steps_per_epoch
            
            class Bridge(TrainingCallback):
                def __init__(self, sig, log_sig):
                    self.sig = sig
                    self.log_sig = log_sig
                    self.h = {'t_acc':[], 'v_acc':[]}
                
                def on_batch_end(self, batch, logs):
                     epoch = logs.get('epoch', 0)
                     current_global_step = epoch * steps_per_epoch + batch
                     
                     if total_steps > 0:
                         prog = int((current_global_step / total_steps) * 100)
                     else:
                         prog = 0
                     
                     if batch % 5 == 0:
                        self.sig.emit({
                            'type':'status', 
                            'msg':f"Epoch {epoch+1}/{ep} | Batch {batch}/{steps_per_epoch} | Loss: {logs['batch_loss']:.4f}",
                            'val': min(prog, 99) # Cap at 99
                        })

                def on_epoch_end(self, epoch, logs):
                    self.h['t_acc'].append(logs['train_acc'])
                    self.h['v_acc'].append(logs['val_acc'])
                    self.sig.emit({'type':'epoch', 'data':self.h, 'ep':epoch, 
                                   'msg':f"Epoch {epoch+1} Complete | Val Acc: {logs['val_acc']:.2%}"})

            # Direct Logger Bridge
            def log_bridge_func(text):
                self.log_signal.emit(str(text))

            self.app.trainer.train_model(tr, val, ep, 
                                         callback=Bridge(self.update_signal, self.log_signal),
                                         log_callback=log_bridge_func)
            
            total_time = time.time() - start_time
            self.update_signal.emit({'type':'done', 'time': total_time})
        except Exception as e:
            self.update_signal.emit({'type':'error', 'msg':str(e)})

    @Slot(dict)
    def on_update(self, d):
        if 'msg' in d: self.status_lbl.setText(d['msg'])
        if 'val' in d: self.pbar.setValue(d['val'])
             
        if d['type'] == 'epoch':
            h = d['data']
            self.ax.clear()
            self.style_plots()
            self.ax.plot(h['t_acc'], label='Train Acc', color='#00d2ff', linewidth=2, marker='o', markersize=4)
            self.ax.plot(h['v_acc'], label='Val Acc', color='#2ecc71', linewidth=2, marker='s', markersize=4)
            self.ax.legend(facecolor=StyleSheet.BG_SURFACE, edgecolor='#30363d', labelcolor='white')
            self.canvas.draw()
            best = max(h['v_acc']) if h['v_acc'] else 0
            self.kpi_best.update_value(f"{best:.1%}")
            
        elif d['type'] == 'done':
            self.btn_train.setEnabled(True)
            self.btn_export.setEnabled(True)
            self.btn_abort.setEnabled(False)
            self.pill.set_status("GOOD")
            self.pill.setText("COMPLETE")
            self.status_lbl.setText("Training Successfully Completed")
            self.pbar.setValue(100)
            
            # Update time KPI
            if 'time' in d:
                mins = int(d['time'] // 60)
                secs = int(d['time'] % 60)
                time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
                self.kpi_time.update_value(time_str)
            
            QMessageBox.information(self, "Success", "Training Finished")
            
        elif d['type'] == 'error':
            self.pill.set_status("DANGER")
            self.pill.setText("ERROR")
            self.status_lbl.setText("Error Occurred")
            self.btn_train.setEnabled(True)
            self.btn_export.setEnabled(True)
            self.btn_abort.setEnabled(False)
            QMessageBox.critical(self, "Error", d['msg'])

    @Slot(str)
    def on_log(self, text):
        c = self.console.textCursor()
        c.movePosition(QTextCursor.End)
        c.insertText(text + "\n")
        self.console.setTextCursor(c)
        self.console.ensureCursorVisible()

class InferencePage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        l = QVBoxLayout(self)
        l.setAlignment(Qt.AlignCenter)
        l.setSpacing(30)
        
        self.zone = QLabel("DROP IMAGE HERE")
        self.zone.setFixedSize(400, 300)
        self.zone.setAlignment(Qt.AlignCenter)
        self.zone.setStyleSheet(f"""
            background: {StyleSheet.BG_SURFACE}; border: 2px dashed #30363d; color: #8b949e; 
            font-size: 20px; font-weight: bold; border-radius: 20px;
        """)
        # Click only for now
        btn = PremiumButton("Select External Image", primary=True)
        btn.setFixedWidth(250)
        btn.clicked.connect(self.pick)
        
        self.res = QLabel("--")
        self.res.setStyleSheet(f"font-size: 32px; color: {StyleSheet.ACCENT_PRIMARY}; font-weight: bold; margin-top: 20px;")
        
        l.addWidget(self.zone)
        l.addWidget(btn)
        l.addWidget(self.res)
        
    def pick(self):
        f, _ = QFileDialog.getOpenFileName(self, "Image")
        if f:
            pix = QPixmap(f).scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.zone.setPixmap(pix)
            self.predict(f)
            
    def predict(self, path):
        if not self.app.model: return
        try:
            img = Image.open(path).convert('RGB')
            # Same transform as val
            tf = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            t = tf(img).unsqueeze(0)
            dev = next(self.app.model.parameters()).device
            
            self.app.model.eval()
            with torch.no_grad():
                out = self.app.model(t.to(dev))
                probs = torch.nn.functional.softmax(out, dim=1)
                conf, idx = torch.max(probs, 1)
                
            cls = self.app.data.classes[idx.item()]
            self.res.setText(f"{cls.upper()} ({conf.item():.1%})")
            
        except Exception as e:
            self.res.setText("Error")
            print(e)
            
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InspecNet Pro | Enterprise Edition")
        self.resize(1400, 900)
        self.setStyleSheet(StyleSheet.MAIN_WINDOW)
        
        # State
        self.data = None
        self.model = None
        self.trainer = None
        
        # UI
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)
        
        self.stack = QStackedWidget()
        self.pages = [DataPage(self), TrainingPage(self), InferencePage(self)]
        for p in self.pages: self.stack.addWidget(p)
        layout.addWidget(self.stack)
        
        # Nav Wire
        for i, btn in enumerate(self.sidebar.buttons):
            btn.clicked.connect(lambda c, x=i: self.nav(x))
            
        self.sidebar.buttons[0].click()
        
        # Logic
        QTimer.singleShot(1000, self.sidebar.update_device)

    def nav(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.sidebar.buttons): b.setChecked(i==idx)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = QFont("Segoe UI", 10)
    app.setFont(f)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
