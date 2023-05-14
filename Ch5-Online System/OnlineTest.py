from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtCore import QRunnable, QThreadPool, Slot, QTimer, QEventLoop, QThread, Signal, QObject
from PySide2.QtGui import QPixmap
from OnlineTest_ui import Ui_MainWindow
import sys
import time
import datetime
from utils import get_current_time, get_data, feature_extraction
from trigger_alarm import saglrstepvar
import numpy as np
import socket
import binascii
import pyqtgraph as pg
import os
import scipy.signal as sciSignal
from multiprocessing.dummy import Pool as ThreadPool
import scipy.io as scio
import pickle
from LedIndicatorWidget import LedIndicator
from playsound import playsound
import threading

# 获取IP
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
IP = '192.168.1.100'
print('Current IP Address:', IP)

n_channels = 64
fs = 1000
category = 'word'

# 一次发送的数据长度
pack_len = 100
words =['ahead','back','left','right','down','up','turn','on','off','over','out','happy','more','tired','afraid','hurt','pain','sad','fever','dizzy','numb','itchy','thirsty','full','hungry','cold','hot'
  ,'thank','sorry','sleepy','dyspnea','stop','pause','previous','next','favorite','lighten','dim','go' ,'get','good','better','bad','yes','no','ok','want','help','message','bath','poop','pee','time','wait','come','slow','emergency','pardon','wash','quiet','dressed','move','lie' 
   ,'I','you','he','it','here','see','when','who','what','why','where','less','much','hi','body']

# 最大阈值
max_threshold = 1000

# 记录运行时间
run_time = []

class ActiveChecker(QThread):
    Onset = Signal(bool)

    def __init__(self, setFigure, mode, model, scaler, pca, pre_model, pre_scaler, pre_pca):
        super().__init__()
        # 线程正在运行
        self._is_running = True
        # 收到新数据标志位
        self.newdata_flag = False
        # 是否开启滤波
        self.FilterOn = True
        # 是否已经触发
        self.is_active = False
        # 识别是否结束
        self.task_over = True
        # 是否按下按钮
        self.button_on = False
        
        # 接收数据的次数
        self.emg_len = pack_len
        self.emgdata = np.zeros([64, self.emg_len])

        # 自动检测模式
        # 2s 单词长度
        self.data_length = 2000
        # 用于存放过去的数据
        self.past_length = 100
        # 检测长度及数据
        self.detection_length = 300
        self.detection_data = np.zeros([64,self.detection_length])
        
        # 用于存放检测到onset以后未来的数据
        self.future_length = self.data_length-self.past_length
        self.future_data = np.zeros([64,self.future_length])
        self.future_cnt = 0
        self.future_all = self.future_length // self.emg_len

        # 手动触发模式
        self.data_cnt = 0
        self.data = np.zeros([64,self.data_length])
        self.data_all = self.data_length // self.emg_len

        # 滤波器参数
        self.fs = fs
        self.sos = sciSignal.butter(8, [10*2/self.fs, 400*2/self.fs], 'bandpass', output='sos')
        self.nb, self.na = sciSignal.iirnotch(50*2/self.fs, 30.0)
        self.nsos = sciSignal.tf2sos(self.nb, self.na)

        # 模式（0为自动触发，1为按钮触发, 2为模型触发）
        self.mode = mode
        # 阈值
        self.threshold = 500
        # onset通道数
        self.onset_ch = n_channels // 2

        # 用于识别
        self.threadpool = QThreadPool()
        self.setFigure = setFigure
        self.model = model
        self.scaler = scaler
        self.pca = pca
        self.pre_model = pre_model
        self.pre_scaler = pre_scaler
        self.pre_pca = pre_pca

        # 刚开始不识别，把detection_data填满
        self.trigger_cnt = 0
        


    def run(self):
        while self._is_running:
            if self.newdata_flag:
                st = datetime.datetime.now()
                self.newdata_flag = False
                if self.mode == 0:
                    # 开始检测
                    if self.FilterOn:
                        self.emgdata = sciSignal.sosfiltfilt(self.sos, self.emgdata)
                        self.emgdata = sciSignal.sosfiltfilt(self.nsos, self.emgdata)

                    if not self.is_active:
                        cnt = 0
                        self.detection_data[:,:-self.emg_len] = self.detection_data[:,self.emg_len:]
                        self.detection_data[:,-self.emg_len:] = self.emgdata
                        if self.trigger_cnt < self.detection_length // self.emg_len:
                            self.trigger_cnt += 1
                            QThread.msleep(20)
                            continue
                        # 识别已结束
                        if self.task_over:
                            for i in range(n_channels):
                                cnt += saglrstepvar(self.detection_data[i,:], 50, self.threshold, 10)
                            
                            # 达到onset条件
                            if cnt >= self.onset_ch:
                                self.is_active = True
                                self.task_over = False
                                self.Onset.emit(True)
                            if cnt > 0:
                                print('activated channel:',cnt)
                    else:
                        # 记录onset以后的有效数据，并在达到指定长度后发送
                        if self.future_cnt < self.future_all:
                            self.future_data[:,self.future_cnt*self.emg_len:(self.future_cnt+1)*self.emg_len] = self.emgdata
                            self.future_cnt += 1
                        else:
                            # 开始识别
                            self.future_cnt = 0
                            self.is_active = False
                            if self.past_length != 0:
                                # scio.savemat('testdata.mat', 
                                #             {'data':np.concatenate([self.detection_data[:,-self.past_length:],self.future_data], axis=1)})
                                self.wr = WordRecognizer(np.concatenate([self.detection_data[:,-self.past_length:],self.future_data], axis=1), 
                                                        self.model, self.scaler, self.pca)
                            else:
                                # scio.savemat('testdata.mat', {'data':self.future_data})
                                self.wr = WordRecognizer(self.future_data,
                                                            self.model, self.scaler, self.pca)
                            self.wr.signals.finished.connect(self.recognition_finished)
                            self.wr.signals.finished.connect(self.setFigure)
                            self.threadpool.start(self.wr)
                elif self.mode == 1:
                    if self.task_over and self.button_on:
                        self.Onset.emit(True)
                        if self.data_cnt < self.data_all:
                            self.data[:,self.data_cnt*self.emg_len:(self.data_cnt+1)*self.emg_len] = self.emgdata
                            self.data_cnt += 1
                        else:
                            if self.FilterOn:
                                self.data = sciSignal.sosfiltfilt(self.sos, self.data)
                                self.data = sciSignal.sosfiltfilt(self.nsos, self.data)
                            self.task_over = False
                            self.data_cnt = 0
                            self.button_on = False
                            
                            # scio.savemat('testdata.mat', {'data':self.data})
                            self.wr = WordRecognizer(self.data, self.model, self.scaler, self.pca)
                            self.wr.signals.finished.connect(self.recognition_finished)
                            self.wr.signals.finished.connect(self.setFigure)
                            self.threadpool.start(self.wr)

                elif self.mode == 2:
                    # 开始检测
                    if self.FilterOn:
                        self.emgdata = sciSignal.sosfiltfilt(self.sos, self.emgdata)
                        self.emgdata = sciSignal.sosfiltfilt(self.nsos, self.emgdata)    
                    if not self.is_active:
                        cnt = 0
                        self.detection_data[:,:-self.emg_len] = self.detection_data[:,self.emg_len:]
                        self.detection_data[:,-self.emg_len:] = self.emgdata
                        # 识别已结束
                        if self.task_over:
                            feature = feature_extraction(self.emgdata, window_len=self.emg_len/1000, 
                                                         step_len=self.emg_len/1000).reshape(1,-1)
                            feature = self.pre_scaler.transform(feature)
                            if self.pre_pca is not None:
                                feature = self.pre_pca.transform(feature)
                            self.is_active = self.pre_model.predict(feature)[0]
                            if self.is_active:
                                self.task_over = False
                                self.Onset.emit(True)
                    else:
                        # 记录onset以后的有效数据，并在达到指定长度后发送
                        if self.future_cnt < self.future_all:
                            self.future_data[:,self.future_cnt*self.emg_len:(self.future_cnt+1)*self.emg_len] = self.emgdata
                            self.future_cnt += 1
                        else:
                            # 开始识别
                            self.future_cnt = 0
                            self.is_active = False
                            if self.past_length != 0:
                                self.wr = WordRecognizer(np.concatenate([self.detection_data[:,-self.past_length:],self.future_data], axis=1), 
                                                        self.model, self.scaler, self.pca)
                            else:
                                self.wr = WordRecognizer(self.future_data,
                                                            self.model, self.scaler, self.pca)
                            self.wr.signals.finished.connect(self.recognition_finished)
                            self.wr.signals.finished.connect(self.setFigure)
                            self.threadpool.start(self.wr)  
            else:
                QThread.msleep(20)

            
    # 停止线程
    def stop(self):
        self._is_running = False

    # 接收到新数据
    @Slot()
    def data_received(self, data):
        self.emgdata = data['EMG']
        self.newdata_flag = True


    # 按钮触发
    @Slot()
    def button_clicked(self):
        self.button_on = True

    @Slot()
    def update_mode(self, mode):
        self.mode = mode
        if mode == 0 or mode == 2:
            self.detection_data = np.zeros([64,self.detection_length])
            self.future_cnt = 0
            self.is_active = False
        elif mode == 1:
            self.data_cnt = 0
            self.button_on = False
        self.task_over = True
        self.Onset.emit(False)

    @Slot()
    def update_sensitivity(self, value):
        self.onset_ch = value

    @Slot()
    def update_threshold(self, value):
        print('Current threshold:', value, )
        self.threshold = value
     
    @Slot()
    def update_filter_on(self, filter_on):
        self.FilterOn = filter_on

    # 识别完成
    @Slot()
    def recognition_finished(self, index):
        self.task_over = True
        self.Onset.emit(False)

            

class WordRecognizerSignal(QObject):
    finished = Signal(int)
    

class WordRecognizer(QRunnable):
    def __init__(self,emgdata,model, scaler, pca):
        super().__init__()
        self.emgdata = emgdata
        self.signals = WordRecognizerSignal()
        self.model = model
        self.scaler = scaler
        self.pca = pca
        self.feature = []

    def run(self):
        print('Begin Recognition')
        st = time.time()
        feature = feature_extraction(self.emgdata).reshape(1,-1)
        # normalize feature
        feature = self.scaler.transform(feature)
        # reduce dimension if self.pca is not None
        if self.pca is not None:
            feature = self.pca.transform(feature)
        # perform recognition using LDA
        y_pred = self.model.predict(feature)
        en = time.time()
        run_time.append(en-st)
        print('识别花费时间',en-st,'s')
        print('识别结果', y_pred[0])
        # play corresponding .mp3 file using speaker
        playsound('./audio/'+ words[int(y_pred[0])] +'.mp3')
        # inform the checker thread after the .mp3 file finished playing
        self.signals.finished.emit(int(y_pred[0]))

class DataReceiver(QThread):
    plot_signal = Signal(dict)
    check_signal  = Signal(dict)
    connection_loss = Signal()
    def __init__(self, coon, dp, ac):
        super().__init__()
        self.coon = coon
        
        self._is_running = True
        self.packetIndex = -1
        self.send_cnt = 0
        self.send_all = pack_len // 20 # 对数据进行一次发送，并解包

        # 临时变量，记录大概14000个点，并保存成mat
        self.temp_all = 14000 // 20
        self.temp_cnt = 0
        self.temp_data = np.zeros((64, self.temp_all * 20))
        
        # 线程池
        self.threadpool = QThreadPool()
        
        # 画图object
        self.dp = dp
        
        # checker线程
        self.ac = ac
        
    def run(self):
        bag_len = 5643
        sign_head = 'aa998877665544332211'
        remain_data = bytes()
        data_to_send = bytes()
        timestamp = ''
        while self._is_running:
            EMG_data_tmp = np.zeros((64, 20))
            total_data = remain_data
            while True:
                no_receive = False
                temp = ''
                try:
                    temp = self.coon.recv(1440)
                except:
                    no_receive = True
                if len(temp) == 0 or no_receive:
                    self.connection_loss.emit()
                    return
                
                total_data += temp
                if len(total_data) > bag_len * 2:
                    break
            head_flag = False
            err_flag = False
            # fix
            # ----------------
            for i in range(len(total_data)-bag_len+1):
            # ----------------
                Head = total_data[i:i + 10].hex()
                trg_tmp = get_current_time()
                if Head == sign_head:
                    head_flag = True
                    data = total_data[i:i + bag_len]
                    remain_data = total_data[i + bag_len:]
                    Type = data[10]
                    len_a = hex(data[12])
                    len_b = hex(data[11])
                    Length = int(len_a[2:] + len_b[2:], 16)     # 5626
                    a = hex(binascii.crc32(data[10:13 + Length]))[2:]   # CRC32
                    if len(a) < 8:
                        for j in range(8 - len(a)):
                            a = '0' + a
                    b = data[-4:].hex()
                    c = a[-2:] + a[-4:-2] + a[-6:-4] + a[-8:-6]
                    if b == c and Type == 1 and Length == 5626:
                        pack = data[13:5613]
                        packetIndex = data[5635] + data[5636] * 256 + data[5637] * 256 * 256 + data[5638] * 256 * 256 * 256
                    else: 
                        print("error in the data pack!")
                        err_flag = True
                    break
            # fix
            # ----------------
            if head_flag == False:
                remain_data = total_data[-(bag_len-1):]
                print('missing data head!')
             # ----------------
            if err_flag == True or head_flag == False:
                continue
            timestamp = timestamp + trg_tmp + '\n'
                             
            if self.send_cnt < self.send_all:
                data_to_send += pack
                self.send_cnt += 1
                if self.send_cnt == self.send_all:
                    worker = DataConverter({"BAG": self.send_all, "EMG": data_to_send})
                    worker.signal.finished.connect(self.ac.data_received)
                    worker.signal.finished.connect(self.dp.update_data)
                    self.threadpool.start(worker)
                    self.send_cnt = 0
                    data_to_send = bytes()

                
    def stop(self):
        self._is_running = False
        
class DataConverter(QRunnable):
    def __init__(self, data):
        super().__init__()
        self.raw_data = data['EMG']
        self.n_packs = data['BAG']
        self.signal = DataConverterSignal()
        
    def run(self):
        EMGdata = np.zeros((64, self.n_packs*20))
        for i in range(self.n_packs*20):
            for j in range(64):
                EMGdata[j,i] = get_data(self.raw_data[280*i+j*4:280*i+j*4+4])
        self.signal.finished.emit({"EMG":EMGdata})
        
        
class DataConverterSignal(QObject):
     finished = Signal(dict)
     
class GainWorker(QRunnable):
    def __init__(self, gain_type, sk):
        # Data Structure
        self.DataHead = bytes.fromhex('aa998877665544332211')
        self.type = 65
        self.type = self.type.to_bytes(1, byteorder='little')
        self.Length = 1
        self.Length = self.Length.to_bytes(1, byteorder='little')
        gain = [6,1,2,3,4,8,12]
        self.gain = gain[gain_type].to_bytes(1, byteorder='little')
        # CRC32 Check Code
        self.crc = binascii.crc32(self.DataHead + self.type + self.Length + self.gain).to_bytes(4, byteorder='little')
        # Socket
        self.sk = sk
        
    def run(self):
        self.sk.send(self.DataHead + self.type + self.Length + self.gain + self.crc)
        

class DataPlotter(QObject):
    def __init__(self,p):
        super().__init__()
        self._is_running = True
        self.p = p

        # 初始化上下限，步长，窗口大小
        self.high = 2600
        self.low = -50
        self.step = 40
        self.window_len = '1s'
        self.wl = 1000
        self.p.setRange(yRange=[self.low, self.high], padding=0)

        # for i in range(6):
        #     self.range_minus()

        # 数据
        self.t = np.linspace(0,10,10000)
        self.act = np.zeros((64, 10000))

        #  初始绘图
        self.EMGline = [None]*64
        for k in range(64):
            self.EMGline[k] = self.p.plot(self.t[:self.wl], self.act[k, -self.wl:], pen=(0, 0, 255))

        # 初始化滤波器
        self.filter_type = None
        self.notch_on = False
        
        # 采样率
        self.fs = fs
        
        # 接受多少次画图
        self.drawing_all = 6
        self.drawing_cnt = 0
        self.data_to_plot = np.zeros((64, self.drawing_all*pack_len))
        

    @Slot()
    def range_plus(self):
        self.high = self.high / 2
        self.low = self.low / 2
        self.step = self.step / 2
        self.p.setRange(yRange=[self.low, self.high], padding=0)

    @Slot()
    def range_minus(self):
        self.high = self.high * 2
        self.low = self.low * 2
        self.step = self.step * 2
        self.p.setRange(yRange=[self.low, self.high], padding=0)
    
    @Slot()
    def window_len_changed(self, s):
        self.window_len = s
        if self.window_len == '0.1s':
            self.wl = 100
        elif self.window_len == '1s':
            self.wl = 1000
        else:
            self.wl = 10000

    @Slot()
    def set_filter(self, filter_type, filter_order, f_low, f_high, notch_on):
        self.filter_type = filter_type
        self.filter_order = filter_order
        self.f_low = f_low
        self.f_high = f_high
        self.notch_on = notch_on

        # 高通或低通
        if filter_type == 'lowpass' or filter_type == 'highpass':
            self.sos = sciSignal.butter(filter_order+1, float(f_low)*2/self.fs, filter_type, output='sos')

        # 带通
        elif filter_type == 'bandpass':
            self.sos = sciSignal.butter(filter_order+1, [float(f_low)*2/self.fs, float(f_high)*2/self.fs], filter_type, output='sos')
        else:
            self.filter_type = None
        # notch
        if notch_on:
            self.nb, self.na = sciSignal.iirnotch(50*2/self.fs, 30.0)
            self.nsos = sciSignal.tf2sos(self.nb, self.na)
            
    @Slot()
    def update_data(self, data):
        emgdata = data["EMG"]
        if self.drawing_cnt < self.drawing_all:
            self.data_to_plot[:, self.drawing_cnt*100:self.drawing_cnt*100+100] = emgdata
            self.drawing_cnt += 1
            if self.drawing_cnt == self.drawing_all:
                self.plot_data()
                self.drawing_cnt = 0
        
    def plot_data(self):
        BAG = self.drawing_all * 100 // 20
        EMGdata = self.data_to_plot
    
        self.t += 0.6

        if self.filter_type != None:
            EMGdata = sciSignal.sosfiltfilt(self.sos, EMGdata)
        if self.notch_on:
            EMGdata = sciSignal.sosfiltfilt(self.nsos, EMGdata)

        #刷新buffer
        self.act[:, 0:-BAG*20] = self.act[:, BAG*20:]
        self.act[:, -BAG*20:] = EMGdata
        t_plot = self.t[:self.wl]-self.wl/1000
        act_plot = self.act[:, -self.wl:]+np.arange(64).reshape(64,1)*self.step
        self.p.setRange(xRange=[min(t_plot), max(t_plot)], padding=0)
        for i in range(64):
            self.EMGline[i].setData(t_plot, act_plot[i])

    def clear(self):
        self.p.clear()
        self.t = np.linspace(0,10,10000)
        self.act = np.zeros((64, 10000))
        for k in range(64):
            self.EMGline[k] = self.p.plot(self.t[:self.wl], self.act[k, -self.wl:], pen=(0, 0, 255))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.flag = 0 
        # 配置ui
        self.StartButton.clicked.connect(self.start)
        self.StopButton.clicked.connect(self.stop)
        self.StopButton.setEnabled(False)
        self.led = LedIndicator()
        self.led.setEnabled(False)
        self.led.setChecked(False)
        self.IndicatorLayout.addWidget(self.led)

        # 绘图设置
        pg.setConfigOption('background', '#FFFFFF')
        pg.setConfigOption('foreground', 'k')
        self.EMG = pg.GraphicsLayoutWidget()
        self.p = self.EMG.addPlot()
        self.EMGPlotLayout.addWidget(self.EMG)

        # 绘图
        self.dp = DataPlotter(self.p)

        # 连接按钮与绘图线程中的槽
        self.RangeMinusButton.clicked.connect(self.dp.range_minus)
        self.RangePlusButton.clicked.connect(self.dp.range_plus)
        self.WindowLen.currentIndexChanged.connect(lambda: self.dp.window_len_changed(self.WindowLen.currentText()))

        # 滤波器相关
        self.FilterSelect.setCurrentIndex(3)
        self.FilterOrderSelect.setCurrentIndex(7)
        self.WindowLen.setCurrentIndex(1) 
        
        self.dp.set_filter(self.FilterSelect.currentText(), self.FilterOrderSelect.currentIndex(), 
                           self.CutoffLow.text(), self.CutoffHigh.text(), self.NotchOn.isChecked())
        self.FilterSelect.currentIndexChanged.connect(self.filter_changed)   
        self.SetFilter.clicked.connect(lambda: self.dp.set_filter(self.FilterSelect.currentText(), self.FilterOrderSelect.currentIndex(), 
                                                                  self.CutoffLow.text(), self.CutoffHigh.text(), self.NotchOn.isChecked()))
        self.FilterOrderSelect.setEnabled(True)
        self.CutoffLow.setEnabled(True)
        self.CutoffHigh.setEnabled(True)

        # 起始禁止按下begin
        self.BeginButton.setEnabled(False)
        self.DetectionMode.currentIndexChanged.connect(self.mode_enable)

        # 自动滤波
        self.FilterOn.setChecked(True)

        # 连接对话框
        self.connecting_dlg = QMessageBox(self)
        self.connecting_dlg.setWindowTitle('Connecting')
        self.connecting_dlg.setText('正在连接设备')
        self.connecting_dlg.setIcon(QMessageBox.Information)
        self.connecting_dlg.setStandardButtons(QMessageBox.NoButton)
        
        # 阈值进度条
        self.Threshold.setMinimum(10)
        self.Threshold.setMaximum(300)
        self.Threshold.setSingleStep(10)
        self.Threshold.setValue(150)

    
    @Slot()
    def start(self):
        self.SubjectID.setReadOnly(True)
        self.StartButton.setEnabled(False)
        self.StopButton.setEnabled(True)

        # 检查该用户是否存在模型
        if not os.path.exists('./Model/'+ category + '/' +self.SubjectID.text() + '/model.pkl'):
            self.reset()
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Warning')
            dlg.setText('该用户不存在模型，请先训练模型！')
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()
            return
        
        with open('./Model/'+ category + '/' +self.SubjectID.text() + '/model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        with open('./Model/'+ category + '/' +self.SubjectID.text() + '/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        if os.path.exists('./Model/'+ category + '/' +self.SubjectID.text() + '/pca.pkl'):
            with open('./Model/'+ category + '/' +self.SubjectID.text() + '/pca.pkl', 'rb') as f:
                self.pca = pickle.load(f)
        else:
            self.pca = None

        # 同样的，检查pre模型
        if not os.path.exists('./Model/'+ category + '/' +self.SubjectID.text() + '/pre_model.pkl'):
            self.pre_model = None
            self.pre_scaler = None
            self.pre_pca = None
            self.DetectionMode.removeItem(2)
        else:
            with open('./Model/'+ category + '/' +self.SubjectID.text() + '/pre_model.pkl', 'rb') as f:
                self.pre_model = pickle.load(f)
            with open('./Model/'+ category + '/' +self.SubjectID.text() + '/pre_scaler.pkl', 'rb') as f:
                self.pre_scaler = pickle.load(f)
            if os.path.exists('./Model/'+ category + '/' +self.SubjectID.text() + '/pre_pca.pkl'):
                with open('./Model/'+ category + '/' +self.SubjectID.text() + '/pre_pca.pkl', 'rb') as f:
                    self.pre_pca = pickle.load(f)
            else:
                self.pre_pca = None

        # 连接网络
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sk.bind((IP, 8080)) # 192.168.16.100
        except:
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Warning')
            dlg.setText('检查本机IP是否正确!')
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()
            
            self.sk.close()
            self.SubjectID.setReadOnly(False)
            self.StartButton.setEnabled(True)
            self.StopButton.setEnabled(False)
            return

        self.sk.listen(5)
        self.sk.settimeout(15)

        loop = QEventLoop()
        self.connecting_dlg.show()
        QTimer.singleShot(100, loop.quit)
        loop.exec_()

        try:
            self.coon, addr = self.sk.accept()
            self.connecting_dlg.accept()
        except:
            self.connecting_dlg.accept()
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Warning')
            dlg.setText('连接超时，检查网络连接！')
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()
            
            self.sk.close()
            self.StartButton.setEnabled(True)
            self.SubjectID.setReadOnly(False)
            self.StopButton.setEnabled(False)
            return
        # 设置超时时间
        self.coon.settimeout(1)
        # 创建checker线程
        self.ac = ActiveChecker(self.setFigure, self.DetectionMode.currentIndex(), 
                                self.model, self.scaler, self.pca, 
                                self.pre_model, self.pre_scaler, self.pre_pca)
        # 连接onset
        #读数据线程
        self.dr = DataReceiver(self.coon, self.dp, self.ac) 
        # 连接网络丢失警告与读数据线程
        self.dr.connection_loss.connect(self.connection_loss_stop)
        self.ac.Onset.connect(self.Is_onset)
        # 调整灵敏度（触发通道数）
        self.Sensitivity.valueChanged.connect(self.ac.update_sensitivity)
        # 调整阈值
        self.Threshold.valueChanged.connect(self.ac.update_threshold)
        # begin按钮触发
        self.BeginButton.clicked.connect(self.ac.button_clicked)
        # 模式选择
        self.DetectionMode.currentIndexChanged.connect(self.ac.update_mode)
        # 滤波器启动
        self.FilterOn.stateChanged.connect(self.ac.update_filter_on)
        # 启动checker线程
        self.ac.start()
        # 启动读数据线程
        self.dr.start()
        # 设置标志位
        self.flag = 1

        # 记录变化
        self.mode_enable(self.DetectionMode.currentIndex())
        self.ac.update_sensitivity(self.Sensitivity.value())
        self.ac.update_threshold(self.Threshold.value())
        self.ac.update_filter_on(self.FilterOn.isChecked())
        
    
    @Slot()
    def setFigure(self,index):
        image = QPixmap('./images/word/' + str(index+1) + '.jpg').scaled(self.PredResult.size())
        self.PredResult.setPixmap(image)
        self.PredResult.show()


    @Slot()
    def Is_onset(self,is_onset):
        self.led.setChecked(is_onset)
        if self.DetectionMode.currentIndex() == 1:
            if is_onset:
                self.BeginButton.setEnabled(False)
            else:
                self.BeginButton.setEnabled(True)


    @Slot()
    def filter_changed(self):
        if self.FilterSelect.currentText() == 'lowpass':
            self.FilterOrderSelect.setEnabled(True)
            self.CutoffLow.setEnabled(True)
            self.CutoffHigh.setEnabled(False)
            self.CutoffLow.setText('499.5')
        elif self.FilterSelect.currentText() == 'highpass':
            self.FilterOrderSelect.setEnabled(True)
            self.CutoffLow.setEnabled(True)
            self.CutoffHigh.setEnabled(False)
            self.CutoffLow.setText('10') 
        elif self.FilterSelect.currentText() == 'bandpass':
            self.FilterOrderSelect.setEnabled(True)
            self.CutoffLow.setEnabled(True)
            self.CutoffHigh.setEnabled(True)
            self.CutoffLow.setText('10')
            self.CutoffHigh.setText('499.5')
        else:
            self.FilterOrderSelect.setEnabled(False)
            self.CutoffLow.setText('')
            self.CutoffHigh.setText('')
            self.CutoffLow.setEnabled(False)
            self.CutoffHigh.setEnabled(False)

    @Slot()
    def connection_loss_stop(self):
        self.reset()
        dlg = QMessageBox(self)
        dlg.setText('丢失网络连接！')
        dlg.setIcon(QMessageBox.Warning)
        dlg.exec_()
        

    @Slot()
    def mode_enable(self, mode):
        if mode == 0:
            self.BeginButton.setEnabled(False)
            self.Sensitivity.setEnabled(True)
            self.Threshold.setEnabled(True)
        elif mode == 1:
            if self.flag == 1:
                self.BeginButton.setEnabled(True)
            self.Sensitivity.setEnabled(False)
            self.Threshold.setEnabled(False)
        else:
            self.BeginButton.setEnabled(False)
            self.Sensitivity.setEnabled(False)
            self.Threshold.setEnabled(False)

    @Slot()
    def stop(self):
        self.reset()
        # 测试结束
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Congrats!')
        dlg.setText('测试结束')
        dlg.setIcon(QMessageBox.Information)
        dlg.exec_()

    def reset(self):
        if self.flag == 1:
            # 重置标志位
            self.flag = 0
            # 关闭数据接受线程
            self.dr.stop()
            self.dr.wait()
            self.dr.quit()
            # 关闭checker
            self.ac.stop()
            self.ac.wait()
            self.ac.quit()
            # 关闭网络
            self.coon.close()
            self.sk.close()
            # 清空绘图
            self.dp.clear()
            
        # 恢复按钮和用户输入
        self.SubjectID.setReadOnly(False)
        self.StartButton.setEnabled(True)
        self.StopButton.setEnabled(False)
        # 禁止调整设置
        self.BeginButton.setEnabled(False)
        # 关闭LED
        self.led.setChecked(False)

        # 关闭app
    def closeEvent(self, event):
        if self.flag == 1:
            dlg = QMessageBox.question(self, 'Message', '确认退出?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if dlg == QMessageBox.Yes:
                self.reset()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    scio.savemat('run_time.mat', {'runtime':run_time})
