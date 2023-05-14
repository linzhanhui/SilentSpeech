import datetime
import winsound
import pyaudio
import wave
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox, QShortcut
from PySide2.QtGui import QPixmap, QKeySequence
from PySide2.QtCore import QRunnable, QThreadPool, Slot, QTimer, QEventLoop, QThread, Signal, QObject, Qt
from LedIndicatorWidget import LedIndicator
import sys
import os
import openpyxl as xl
import scipy.io as scio
from random import shuffle
from SpeechGuide_ui import Ui_MainWindow
from utils import get_current_time, get_data, convert_time
import numpy as np
import socket
import binascii
import pyqtgraph as pg
import scipy.signal as sciSignal
import time
import shutil

# 一次处理的数据量
pack_len = 100
# 丢包阈值设置
LossThreshold = 0.1

# 获取IP
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
IP = '192.168.1.108'
print('Current IP Address:', IP)

# 各类参数
basedir = os.path.dirname(__file__)
fs = 1000
n_channels = 64

categories = ['单词', '句子', '静态表情', '动态表情', '无关动作']
image_dir = ['./images/word/','./images/sentence/','./images/trans_expression/','./images/dynm_expression/','./images/irrelevant/']
# words =['ahead','back','left','right','down','up','turn','on','off','over','out','happy','more','tired','afraid','hurt','pain','sad','fever','dizzy','numb','itchy','thirsty','full','hungry','cold','hot'
#   ,'thank','sorry','sleepy','dyspnea','stop','pause','previous','next','favorite','lighten','dim','go' ,'get','good','better','bad','yes','no','ok','want','help','message','bath','poop','pee','time','wait','come','slow','emergency','pardon','wash','quiet','dressed','move','lie' 
#    ,'I','You','he','it','here','see','when','who','what','why','where','less','much','hi','body']
words =['ahead','back','left','right','down','up','turn']
sentences =['Much better ','thank you','see you','i see ','Come on']#'Slow down .','Move body ','Turn over','Turn on ','Turn off','turn up','turn down','go off','go on','go out','wash up','get dressed','get off','lie down','get up']
tran_expressions = ['委屈（噘嘴）', '打哈欠', '难过（皱眉）', '咬牙', '咳嗽', '开心（微笑唇）', '静息']
dynm_expressions =['微笑唇过渡到噘嘴','左鼓腮过渡到右鼓腮'] 
irrelevant =['不发声，无关动作2min']

# words =['ahead']
# sentences =['Much better ','thank you','see you','i see ','Come on']#'Slow down .','Move body ','Turn over','Turn on ','Turn off','turn up','turn down','go off','go on','go out','wash up','get dressed','get off','lie down','get up']
# tran_expressions = ['委屈（噘嘴）']
# dynm_expressions =['微笑唇过渡到噘嘴'] 
# irrelevant =['不发声，无关动作2min']

all_tasks=[words,sentences,tran_expressions,dynm_expressions,irrelevant]
rt_time =[[3,1,2],[3,1,3],[3,1,2],[3,1,3],[3,0,10]] # [组间休息时间、组内休息时间、任务时间]
ng_tasks = [13,10,7,3,1] # 每组内的任务个数
nt_tasks = [len(words),len(sentences),len(tran_expressions),len(dynm_expressions),len(rt_time)]
n_trials = 1 

# 存储数据的handle
global fileEMG_handle, fileTime_handle

fileEMG_handle = None
fileTime_handle = None

# 存储制造的数据
class DummyDataSaver(QRunnable):
    def __init__(self, n_samples, baseline):
        super().__init__()
        self.n_samples = n_samples//20*20
        self.baseline = baseline

    def run(self):
        data = (0.01*np.random.randn(n_channels, self.n_samples) + self.baseline.reshape(-1,1)).astype(np.float32)
        data = data.flatten(order='F').tobytes()
        global fileEMG_handle, fileTime_handle
        fileEMG_handle.write(data)
        timestamp = ''
        for i in range(self.n_samples//20):
            timestamp += 'xxxxxxxxx xxx -1\n'
        fileTime_handle.write(timestamp)


# 存储数据
class DataSaver(QRunnable):
    def __init__(self, bag, data_all,timestamp):
        super().__init__()
        self.bag = bag
        self.data_all = data_all
        self.timestamp=timestamp

    @Slot()
    def run(self):
        starttime = datetime.datetime.now()
        print("Saving Thread Start")
        pack=np.array(bytearray(self.data_all))
        emg = bytes(pack[(np.arange(256) + np.arange(self.bag * 20).reshape(self.bag * 20, 1) * 280).flatten()])
        global fileEMG_handle, fileTime_handle
        fileEMG_handle.write(emg)
        fileTime_handle.write(self.timestamp)
        print("Saving Thread Complete")
        endtime = datetime.datetime.now()
        print("writing time  ", endtime - starttime)

# 接受数据
class DataReceiver(QThread):
    receive = Signal(dict)
    coon_update = Signal(dict)
    connection_loss = Signal()
    pause = Signal(int)
    continue_sig = Signal()
    begin_exp = Signal(str)
    bat_change = Signal(int)
    update_count = Signal(int)
    trial_complete = Signal(int,int)

    def __init__(self, coon, sk, dp, update_baseline):
        super().__init__()
        self.coon = coon
        self.sk = sk
        self.writing_count = 0
        self.writing_all = 300
        self.threadpool = QThreadPool()  # 线程池
        self._is_running = True
        self.timestamp = None
        self.FirstRecv = True
        # 尝试重新连接的次数
        self.reconnect_attempts = 20
        self.reconnect_cnt = 0
        self.reconnect = False
        # 电量
        self.bat_all = 1000
        self.bat_cnt = 0
        # 测试基线 (5s)
        self.baseline_set = False
        self.update_baseline = update_baseline
        self.EMGBaseline = None
        # trial开始
        self.begin_trial = False
        # 包marker
        self.validpack_cnt = 0
        self.validpack_all = 0
        # 丢包，错包数目
        self.n_loss_pack = 0
        self.n_err_pack = 0
        # ui是否暂停
        self.is_paused = False
        
        # 发送数据
        self.send_all = pack_len // 20
        self.send_cnt = 0
        self.info_time = 0
        
        # 画图object
        self.dp = dp
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())  # 输出最大线程数
 
    def run(self):
        bag_len = 5643
        sign_head = 'aa998877665544332211'
        remain_data = bytes() 
        data_to_save = bytes()
        data_to_send = bytes()

        timestamp = ''
        starttime = datetime.datetime.now()
        while self._is_running:        
            total_data = remain_data
            while True:
                loss_flag = False
                recv_time = time.time()
                try:
                    temp = self.coon.recv(1440)
                except Exception as e:
                    print('-------------')
                    print('connection loss: ', e)
                    print('-------------')
                    loss_flag = True
                if loss_flag or len(temp)==0:  
                    if self.FirstRecv or self.baseline_set == False:
                        self.connection_loss.emit()
                        return
                    else:
                        # 暂停主程序的执行
                        self.pause.emit(recv_time)
                        self.ui_paused()
                        # 尝试重连
                        while self.reconnect_cnt < self.reconnect_attempts and not self.reconnect:
                            self.coon.close()
                            try:
                                self.coon, addr = self.sk.accept()
                                self.reconnect = True
                            except:
                                self.reconnect_cnt += 1
                                time.sleep(0.1)
                        if self.reconnect:
                            self.reconnect_cnt = 0
                            # 尝试接收数据
                            try:
                                temp = self.coon.recv(100)
                                print('reconnect successful')
                                self.coon_update.emit({'coon':self.coon})
                            except:
                                print('check again....')
                                continue
                            # 保存掉线前的部分data
                            total_data = bytes()
                            write_worker = DataSaver(self.writing_count, data_to_save,timestamp)
                            self.threadpool.start(write_worker)
                            self.update_count.emit(self.writing_count*20)
                            timestamp = ''
                            data_to_save = bytes()
                            self.writing_count = 0
                            self.drawing_count = 0
                            time.sleep(0.1)
                            # 示意程序继续
                            self.continue_sig.emit()
                            # 重置标志位
                            self.reconnect = False
                            continue
                        else:
                            self.connection_loss.emit()
                            return

                total_data += temp
                if len(total_data) > bag_len * 2:
                    break

            err_flag = False
            for i in range(len(total_data)-bag_len+1):
                Head = total_data[i:i + 10].hex()
                if Head == sign_head:
                    trg_tmp = get_current_time()
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
                        bat_level = data[5629]
                        PacketIndex = data[5635] + data[5636] * 256 + data[5637] * 256 * 256 + data[5638] * 256 * 256 * 256
                        # 第一次接受正确的包
                        if self.FirstRecv:
                            # 上一次的包序号
                            LastValidPacketIndex = PacketIndex
                            # 1s超时
                            self.coon.settimeout(1)
                            self.sk.settimeout(1)
                            self.FirstRecv = False
                            self.begin_exp.emit(trg_tmp)
                            self.bat_change.emit(bat_level)
                    else: 
                        # print('--------------------')
                        # print("error in the data pack!")
                        # print('--------------------')
                        err_flag = True
                    break

            if head_flag == False:
                remain_data = total_data[-(bag_len-1):]

                # print('--------------------')
                # print('missing data head!')
                # print('--------------------')
        
                
            if err_flag == True or head_flag == False:
                PacketIndex = -1
                if self.begin_trial:
                    self.n_err_pack += 1
                if self.baseline_set == False:
                    pack = bytes(5600)
                else:
                    dummydata = (np.random.randn(n_channels, 20) + self.EMGBaseline.reshape(-1,1)).astype(np.float32)
                    dummydata = np.concatenate([dummydata, np.zeros([6,20],dtype=np.float32)], axis=0)
                    pack = dummydata.flatten(order='F').tobytes()
            else:
                if self.begin_trial:
                    # 检测包序号
                    if LastValidPacketIndex != PacketIndex:
                        self.n_loss_pack += PacketIndex - LastValidPacketIndex - 1                   
                LastValidPacketIndex = PacketIndex
            
                    
            # 数据写入
            if self.begin_trial and not self.is_paused:
                if self.validpack_cnt < self.validpack_all:
                    timestamp = timestamp + trg_tmp + ' ' + str(PacketIndex) + ' ' + '1' + '\n'
                    self.validpack_cnt += 1
                    if self.validpack_cnt == self.validpack_all:
                        self.trial_complete.emit(max(self.n_loss_pack-self.n_err_pack,0), self.n_err_pack)
                        self.n_loss_pack = 0
                        self.n_err_pack = 0
                        self.begin_trial = False
                        self.validpack_cnt = 0                    
            else:
                timestamp = timestamp + trg_tmp + ' ' + str(PacketIndex) + ' ' + '0' + '\n'

            data_to_save += pack
            self.writing_count += 1
            
            if self.writing_count ==self.writing_all:
                self.writing_count = 0
                write_worker = DataSaver(self.writing_all, data_to_save,timestamp)
                self.threadpool.start(write_worker)
                self.update_count.emit(self.writing_all*20)
                timestamp = ''
                data_to_save = bytes()
                
            if self.baseline_set == False and (head_flag == False or err_flag == True):
                continue
            
            if self.send_cnt < self.send_all:
                data_to_send += pack
                self.send_cnt += 1
                if self.send_cnt == self.send_all:
                    self.info_time += 1
                    worker = DataConverter({"BAG": self.send_all, "EMG": data_to_send})
                    worker.signal.finished.connect(self.dp.update_data)
                    if not self.baseline_set:
                        worker.signal.finished.connect(self.update_baseline)
                    self.threadpool.start(worker)
                    self.send_cnt = 0
                    data_to_send = bytes()
    
            # 更新电量
            self.bat_cnt += 1
            if self.bat_cnt == self.bat_all:
                self.bat_change.emit(bat_level)
                self.bat_cnt = 0
                
            if self.info_time == 10:
                self.info_time = 0
                endtime = datetime.datetime.now()
                print('receive data time (1000 data points):', endtime - starttime)
                starttime = datetime.datetime.now()
                
        write_worker = DataSaver(self.writing_count, data_to_save,timestamp)
        self.threadpool.start(write_worker)
        self.update_count.emit(self.writing_count*20)
        time.sleep(0.5)
    
    def stop(self):
        self._is_running = False

    # 某一trial开始
    @Slot()
    def is_begin(self, duration):
        self.begin_trial = True
        self.validpack_all = duration*1000//20

    # 引导程序停止
    @Slot()
    def ui_paused(self):
        self.is_paused = True
        self.begin_trial = False
        self.validpack_cnt = 0
        self.n_loss_pack = 0
        self.n_err_pack = 0

    # 引导程序继续
    @Slot()
    def ui_continued(self):
        self.is_paused = False
    
    # 基线设置完毕
    @Slot()
    def baseline_ok(self, baseline):
        self.baseline_set = True
        self.EMGBaseline = baseline['EMG']
        
        
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
     
class GainChanger(QRunnable):
    def __init__(self, gain_type, coon):
        super().__init__()
        # Data Structure
        self.DataHead = bytes.fromhex('aa998877665544332211')
        self.type = 65
        self.type = self.type.to_bytes(1, byteorder='little')
        self.Length = 1
        self.Length = self.Length.to_bytes(2, byteorder='little')
        gain = [6,1,2,3,4,8,12]
        self.gain = gain[gain_type].to_bytes(1, byteorder='little')  
        # CRC32 Check Code
        self.crc = binascii.crc32(self.type + self.Length + self.gain).to_bytes(4, byteorder='little')
        # Socket
        self.coon = coon
        
    def run(self):
        self.coon.send(self.DataHead + self.type + self.Length + self.gain + self.crc)

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
    
        self.t += self.drawing_all * 0.1

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

# work in Windows only
class SoundWorker(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        winsound.Beep(600, 1000)

# 录音
class AudioRecorder(QThread):
    def __init__(self, filename):
        super().__init__()
        self._is_running = True
        self.filename = filename

    def run(self):
        # set audio format
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 2
        fs = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
        frames = []

        while self._is_running:
            data = stream.read(chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
         
    def stop(self):
        self._is_running = False
    
class begin_signal(QObject):
    trial_begin = Signal(int)
    
class baseline_signal(QObject):
    baseline_ok = Signal(dict)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('数据采集')
        self.today = datetime.date.today()
        self.flag = 0

        # 开始任务
        self.StartButton.clicked.connect(self.start)

        # 某一trial开始
        self.begin_sig = begin_signal()
        # baseline设置完成
        self.baseline_sig = baseline_signal()

        # 不允许输入的ui
        self.MissionTimer.setReadOnly(True)
        self.CurrentGroup.setReadOnly(True)
        self.CurrentTrial.setReadOnly(True)
        self.CurrentIndex.setReadOnly(True)
        self.TotalIndex.setReadOnly(True)
        self.TotalTrial.setReadOnly(True)
        self.GainType.setEnabled(False)

        # led显示
        self.led = LedIndicator()
        self.led.setEnabled(False)
        self.led.setChecked(False)
        self.LEDLayout.addWidget(self.led)

        # threadpool
        self.threadpool = QThreadPool() 

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

        # 暂停和继续按钮
        self.pause_loop = QEventLoop()
        self.PauseButton.clicked.connect(self.pause_task)
        self.ContinueButton.clicked.connect(self.continue_task)
        self.PauseButton.setEnabled(False)
        self.ContinueButton.setEnabled(False)
        
        # 为暂停按钮设置一个快捷键 (空格)
        shortcut = QShortcut(QKeySequence(Qt.Key_Space), self.PauseButton)
        shortcut.activated.connect(self.pause_task)

        # 连接对话框
        self.connecting_dlg = QMessageBox(self)
        self.connecting_dlg.setWindowTitle('Connecting')
        self.connecting_dlg.setText('正在连接设备')
        self.connecting_dlg.setIcon(QMessageBox.Information)
        self.connecting_dlg.setStandardButtons(QMessageBox.NoButton)

        # 暂停对话框
        self.pause_dlg = QMessageBox(self)
        self.pause_dlg.setWindowTitle('Warning')
        self.pause_dlg.setText('等待当前任务结束')
        self.pause_dlg.setIcon(QMessageBox.Warning)
        self.pause_dlg.setStandardButtons(QMessageBox.NoButton)

        # 断线对话框
        self.reconnect_dlg = QMessageBox(self)
        self.reconnect_dlg.setWindowTitle('Warning')
        self.reconnect_dlg.setText('断线重连中')
        self.reconnect_dlg.setIcon(QMessageBox.Warning)
        self.reconnect_dlg.setStandardButtons(QMessageBox.NoButton)

        # 等待对话框
        self.wait_dlg = QMessageBox(self)
        self.wait_dlg.setWindowTitle('Wait')
        self.wait_dlg.setText('等待补全数据')
        self.wait_dlg.setIcon(QMessageBox.Information)
        self.wait_dlg.setStandardButtons(QMessageBox.NoButton)

        # 测试基线
        self.baseline_dlg = QMessageBox(self)
        self.baseline_dlg.setWindowTitle('Baseline Test')
        self.baseline_dlg.setText('测试基线，请保持静止5s')
        self.baseline_dlg.setIcon(QMessageBox.Information)
        self.baseline_dlg.setStandardButtons(QMessageBox.NoButton)
        
        # 丢包率过高
        self.loss_dlg = QMessageBox(self)
        self.loss_dlg.setWindowTitle('Warning')
        self.loss_dlg.setText('丢包率过高，暂停实验')
        self.loss_dlg.setIcon(QMessageBox.Warning)
    


    def filter_changed(self):
        if self.FilterSelect.currentText() == 'lowpass':
            self.FilterOrderSelect.setEnabled(True)
            self.CutoffLow.setEnabled(True)
            self.CutoffHigh.setEnabled(False)
            self.CutoffLow.setText('499.5')
        if self.FilterSelect.currentText() == 'highpass':
            self.FilterOrderSelect.setEnabled(True)
            self.CutoffLow.setEnabled(False)
            self.CutoffHigh.setEnabled(True)
            self.CutoffHigh.setText('10')
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
    def battery_changed(self,level):
        self.BatteryLevel.setValue(level)

    def plot_image1(self, image):
        pixmap = QPixmap(image).scaled(self.CurrentFig.size())
        self.CurrentFig.setPixmap(pixmap)
        self.CurrentFig.show()

    def plot_image2(self, image):
        pixmap = QPixmap(image).scaled(self.CurrentFig.size())
        self.NextFig.setPixmap(pixmap)
        self.NextFig.show()

    def start(self):
        self.SubjectID.setReadOnly(True)
        self.StartButton.setEnabled(False)
        self.SpeechMode.setEnabled(False)
        # 收到了第一个包
        self.begin_exp = False 
        # 可以开始测基线
        self.ready = False 
        
        self.EMGBaseline = None
        self.baseline_cnt = 0
        self.baseline_set = False
        self.baseline_all = 5000 // pack_len
        self.baseline_data = np.zeros((64, 5000))

        # 掉线标志位
        self.end_flag = False
        
        # 退出app
        self.exit_app = False
        
        # 丢包检测是否完成
        self.LossChecked = True
        self.pack_all = 0 # 每次trial应收包数
        
        # 记录收到数据的数目
        self.sample_count = 0
          
        # 记录成功完成的task数
        self.n_sucess = 0
        
        # 暂停
        self.is_paused = False
        
        ID = self.SubjectID.text()
        if self.SpeechMode.currentIndex()  == 0:
            self.path = basedir + '/DataSave/' + ID + '_' + str(self.today) + '_SS'
        else:
            self.path = basedir + '/DataSave/' + ID + '_' + str(self.today) + '_AS'
        isExists = os.path.exists(self.path)
        if not isExists:
            os.makedirs(self.path)
            print("目录已创建")
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Warning')
            dlg.setText('目录已存在，请更换ID或发声模式')
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()
            self.reset()
            return
 
        # 连接网络
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sk.bind((IP, 8080))  # 192.168.16.100
        except:
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText('IP地址错误！')
            dlg.setIcon(QMessageBox.Critical)
            dlg.exec_()
            os.rmdir(self.path)
            self.reset()
            return
        self.sk.listen(5)
        self.sk.settimeout(15)

        self.connecting_dlg.show()
        QTimer.singleShot(100, self.pause_loop.quit)
        self.pause_loop.exec_()
        
        try:
            self.coon, addr = self.sk.accept()
            self.connecting_dlg.accept()
        except:
            self.connecting_dlg.accept()
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText('连接超时，检查网络连接！')
            dlg.setIcon(QMessageBox.Critical)
            dlg.exec_()
            os.rmdir(self.path)
            
            self.sk.close()
            self.reset()
            return
        
        self.coon.settimeout(10)

        #读数据线程
        self.dr = DataReceiver(self.coon, self.sk, self.dp, self.setBaseline)

        # 丢失连接
        self.dr.connection_loss.connect(self.connection_loss)
        # 开始任务 
        self.dr.begin_exp.connect(self.enable_exp) 
        # 请求暂停和继续
        self.dr.pause.connect(self.connection_loss_pause)
        self.dr.continue_sig.connect(self.connection_loss_continue)
        # ui暂停和继续
        self.PauseButton.clicked.connect(self.dr.ui_paused)
        self.ContinueButton.clicked.connect(self.dr.ui_continued)
        # 更新电量
        self.dr.bat_change.connect(self.battery_changed)
        # 收到数据的数量更新
        self.dr.update_count.connect(self.updateSampleCount)
        # 丢包测试
        self.dr.trial_complete.connect(self.CalLossRate)
        # 开始trial
        self.begin_sig.trial_begin.connect(self.dr.is_begin)
        # baseline设置完成
        self.baseline_sig.baseline_ok.connect(self.dr.baseline_ok)
        #启动读数据线程
        self.dr.start()
        
        # 连接增益combobox与槽函数
        self.GainType.currentIndexChanged.connect(self.GainChanged)
        self.dr.coon_update.connect(self.UpdateSocket)

        self.flag = 1

        # 数据存储
        global fileEMG_handle, fileTime_handle
        fileEMG = self.path + '/' + ID + '_' + str(self.today) + '_EMGData.bin'
        fileTime = self.path + '/' + ID + '_' + str(self.today) + '_timestampData.txt'
        fileEMG_handle = open(fileEMG, mode='wb')
        fileTime_handle = open(fileTime, mode='w')

        # Silent Speech
        if self.SpeechMode.currentIndex()  == 0:
            # save important time stamp and the order of the random array in a file
            LogFileName = self.path+ '/' + ID + '_' + str(self.today) + '_PRlog.xlsx'
            LogMat = self.path + '/' + ID + '_' + str(self.today) + '_PRlog.mat'
        # Audible Speech
        else:
            # save important time stamp and the order of the random array in a file
            LogFileName = self.path + '/' + ID + '_' + str(self.today) + '_PRlog.xlsx'
            LogMat = self.path + '/' + ID + '_' + str(self.today) + '_PRlog.mat'
            # audio filename
            AudioFileName = self.path + '/' + ID + '_' + str(self.today) + '_Audio.wav'
            # create new thread for audio recording
            self.ar = AudioRecorder(AudioFileName)
        if self.SpeechMode.currentIndex() == 1:
            # start recording audio
            self.ar.start()
        workbook = xl.Workbook()
        workbook.save(LogFileName)
        wb = xl.load_workbook(LogFileName)
        sheet = wb.active

        while not self.begin_exp:
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            if self.end_flag:
                shutil.rmtree(self.path)
                return
          
        dlg = QMessageBox(self)
        dlg.setWindowTitle('hint')
        dlg.setText('休息时保持面部放松\n跟随指引，观察显示屏上的计时器，在计时结束前完成相应的动作')
        dlg.setIcon(QMessageBox.Information)
        dlg.exec_()
        
        self.ready = True
        if self.end_flag:
            shutil.rmtree(self.path)
            return
    
        # 测试基线电平（5s）
        self.baseline_dlg.show()
        self.pause_loop.exec_()
        self.baseline_dlg.accept()
        
        if self.end_flag:
            shutil.rmtree(self.path)
            return
        

        # 允许暂停
        self.PauseButton.setEnabled(True)
        # 允许发送指令
        self.GainType.setEnabled(True) 
        # Trial次数
        self.TotalTrial.setText(str(n_trials))

        EventTimingtemp = []
        EventTimingtemp.append(['数据采集开始', get_current_time()])
        rand_hist = []

        # 单词、句子、静态表情和动态表情
        for tt in range(n_trials):
            self.CurrentTrial.setText(str(tt+1))
            
            fileEMG_handle.flush()
            fileTime_handle.flush()
            
            for idx in range(4):
                self.CurrentGroup.setText(categories[idx])
                self.TotalIndex.setText(str(nt_tasks[idx]))
                randIndex = list(range(nt_tasks[idx]))
                shuffle(randIndex)
                rand_hist.extend(randIndex)
                tg = 0
                self.LossChecked = True
                
                while tg <= nt_tasks[idx]:
                    while self.LossCheckOn.isChecked() and not self.LossChecked:
                        Lossloop = QEventLoop()
                        QTimer.singleShot(100, Lossloop.quit)
                        Lossloop.exec_()
                    self.LossChecked = False
                    if self.is_paused:
                        self.n_sucess -= 1
                        self.pause_dlg.accept()
                        self.pause_loop.exec_()
                        # 退出app
                        if self.exit_app:
                            return
                        # 掉线,结束start
                        if self.end_flag:
                            EventTimingtemp.pop()
                            EventTimingtemp.pop()
                            EventTimingtemp.append(['数据采集结束', get_current_time()])
                            # 保存数据，写入文件
                            for j in EventTimingtemp:
                                sheet.append(j)
                            scio.savemat(LogMat, {'randIndex':rand_hist[:(len(EventTimingtemp)-2)//2]})
                            wb.save(LogFileName)
                            # 记录成功次数
                            with open(self.path + '/NumSuccessLog.txt', 'a') as f:
                                f.write(str(self.n_sucess) + '\n')
                                f.close()
                            return
                        # 重新进行上一次trial
                        tg -= 1
                        # 丢弃上一次记时（开始和结束）
                        EventTimingtemp.pop()
                        EventTimingtemp.pop()
                        # 提示重复操作
                        dlg = QMessageBox(self)
                        dlg.setWindowTitle('Notice')
                        dlg.setText('重复本次试验!')
                        dlg.setIcon(QMessageBox.Information)
                        dlg.exec_()
                        continue
                    if tg == nt_tasks[idx]:
                        break
                    
                    self.CurrentIndex.setText(str(tg+1))
                    if tg < nt_tasks[idx] - 1:
                        self.plot_image1(image_dir[idx]+'/'+str(randIndex[tg]+1)+'.jpg')
                        self.plot_image2(image_dir[idx]+'/'+str(randIndex[tg+1]+1)+'.jpg')
                    else:
                        self.plot_image1(image_dir[idx]+'/'+str(randIndex[tg]+1)+'.jpg')
                        self.plot_image2(image_dir[idx]+'/'+'0'+'.jpg')
                    
                    if tg % ng_tasks[idx] == 0:
                        TimeDuration = [rt_time[idx][0], rt_time[idx][2]]
                    else:
                        TimeDuration = [rt_time[idx][1], rt_time[idx][2]]
                    
                    for td in range(len(TimeDuration)):
                        self.MissionTimer.setText(str(TimeDuration[td]))
                        if td == 0:
                            self.label_6.setText('休息计时器')
                        if td == 1:
                            self.begin_sig.trial_begin.emit(TimeDuration[1])
                            self.pack_all = TimeDuration[1] * 50
                            EventTimingtemp.append(['第' + str(tg+1) + '个' + categories[idx] + '第' + str(tt+1) + '组开始', get_current_time()])
                            worker = SoundWorker()
                            self.threadpool.start(worker)

                            self.label_6.setText('任务计时器')
                            self.led.setChecked(True)

                        for t in range(TimeDuration[td]):
                            if self.exit_app:
                                return
                            self.MissionTimer.setText(str(TimeDuration[td]-t))
                            loop = QEventLoop()
                            QTimer.singleShot(1000, loop.quit)
                            loop.exec_()
                        if td == 1:
                            self.led.setChecked(False)
                    
                    EventTimingtemp.append(['第' + str(tg+1) + '个' + categories[idx] + '第' + str(tt+1) + '组结束', get_current_time()])
                    self.n_sucess += 1
                    tg += 1

        # 2分钟无关动作
        self.CurrentGroup.setText(categories[4])
        self.TotalIndex.setText('1')
        self.CurrentIndex.setText('1')
        self.CurrentTrial.setText('1')
        self.TotalTrial.setText('1')
        TimeDuration = [rt_time[4][0], rt_time[4][2]]
        self.plot_image1(image_dir[4]+'/'+'1'+'.jpg')
        self.plot_image2(image_dir[4]+'/'+'0'+'.jpg')
        while True:
            for td in range(len(TimeDuration)):                   
                self.MissionTimer.setText(str(TimeDuration[td]))
                if td == 0:
                    self.label_6.setText('休息计时器')
                if td == 1:
                    self.begin_sig.trial_begin.emit(TimeDuration[1])
                    EventTimingtemp.append(['无关动作开始', get_current_time()])
                    worker = SoundWorker()
                    self.threadpool.start(worker)
                    
                    self.label_6.setText('任务计时器')
                    self.MissionTimer.setText('1')
                    self.led.setChecked(True)

                for t in range(TimeDuration[td]):
                    if self.exit_app:
                        return
                    self.MissionTimer.setText(str(TimeDuration[td]-t))
                    loop = QEventLoop()
                    QTimer.singleShot(1000, loop.quit)
                    loop.exec_()
                if td == 1:
                    self.led.setChecked(False)

            EventTimingtemp.append(['无关动作结束', get_current_time()])
            self.n_sucess += 1
            self.EventEndTime = EventTimingtemp[-1][1]
            if self.is_paused:
                self.n_sucess -= 1
                self.pause_dlg.accept()
                self.pause_loop.exec_()
                # 退出app
                if self.exit_app:
                    return
                # 掉线,结束start
                if self.end_flag:
                    EventTimingtemp.pop()
                    EventTimingtemp.pop()
                    EventTimingtemp.append(['数据采集结束', get_current_time()])
                    # 保存数据，写入文件
                    for j in EventTimingtemp:
                        sheet.append(j)
                    scio.savemat(LogMat, {'randIndex':rand_hist})
                    wb.save(LogFileName)
                    # 记录成功次数
                    with open(self.path + '/NumSuccessLog.txt', 'a') as f:
                        f.write(str(self.n_sucess) + '\n')
                        f.close()
                    return
                # 丢弃上一次记时（开始和结束）
                EventTimingtemp.pop()
                EventTimingtemp.pop()
                # 提示重复操作
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Notice')
                dlg.setText('重复本次试验!')
                dlg.setIcon(QMessageBox.Information)
                dlg.exec_()
            else:
                break

        EventTimingtemp.append(['数据采集结束', get_current_time()])
        # 保存数据，写入文件
        for j in EventTimingtemp:
            sheet.append(j)
        scio.savemat(LogMat, {'randIndex':rand_hist})
        wb.save(LogFileName)
        # 记录成功次数
        with open(self.path + '/NumSuccessLog.txt', 'w') as f:
            f.write(str(self.n_sucess) + '\n')
            f.close()

        # 终止实验
        self.stop()

    # 重置各类状态，停止子线程
    def reset(self):
        if self.flag == 1:
            # 停止录制
            if self.SpeechMode.currentIndex()  == 1:
                self.ar.stop()
                self.ar.deleteLater()
            # 关闭数据接受线程
            self.dr.stop()
            self.dr.wait()
            self.dr.quit()
            # 关闭文件
            global fileEMG_handle, fileTime_handle
            fileEMG_handle.close()
            fileTime_handle.close()
            # 关闭网络
            self.coon.close()
            self.sk.close()
            # 重置绘图
            self.dp.clear()

        self.flag = 0
        self.StartButton.setEnabled(True)
        self.SubjectID.setReadOnly(False)
        self.SpeechMode.setEnabled(True)
        self.PauseButton.setEnabled(False)
        self.ContinueButton.setEnabled(False)
        self.GainType.setEnabled(False)
        self.led.setChecked(False)
        
    # 实验正常结束
    @Slot()
    def stop(self):
        # 无关动作结束时间
        self.EventEndTime = convert_time(self.EventEndTime)
        print('-----------------------------------')
        print('Expected number of packs:')
        print((self.EventEndTime-self.FirstPackTime)//20)
        print('Actual number of packs:')
        print(self.sample_count//20)
        if self.EventEndTime-self.FirstPackTime > self.sample_count:
            self.wait_dlg.show()
        while self.EventEndTime-self.FirstPackTime > self.sample_count:
            time.sleep(0.1)
            QApplication.processEvents()
        self.wait_dlg.accept()
        print('total number of packs received: ', self.sample_count//20)
        print('-----------------------------------')

        self.reset()

        dlg = QMessageBox(self)
        dlg.setWindowTitle('Congrats!')
        dlg.setText('数据采集完毕')
        dlg.setIcon(QMessageBox.Information)
        dlg.exec_()

    # 因掉线暂停实验
    @Slot()
    def connection_loss_pause(self, loss_time):
        self.is_paused = True
        self.LossChecked = True
        self.loss_time = loss_time
        self.reconnect_dlg.show()

        self.GainType.setEnabled(False)
        self.ContinueButton.setEnabled(False)
        self.PauseButton.setEnabled(False)

    # 掉线继续
    @Slot()
    def connection_loss_continue(self):
        self.continue_time = time.time()
       
        self.reconnect_dlg.accept()
        # 写入对应数据丢失期间的dummy数据
        loss_period = self.continue_time-self.loss_time
        n_loss_sample = int(loss_period*1000)
        print('-------------')
        print('reconnection time: '+str(loss_period)+'s')
        print('-------------')
        worker = DummyDataSaver(n_loss_sample, self.EMGBaseline)
        self.threadpool.start(worker)
        self.updateSampleCount(n_loss_sample)

         # 关闭重连对话框
        self.reconnect_dlg.accept()

        self.LossChecked = True
        self.GainType.setEnabled(True)
        self.ContinueButton.setEnabled(True)
        self.PauseButton.setEnabled(False)

    # 正常暂停实验
    @Slot()
    def pause_task(self):
        self.is_paused = True
        self.LossChecked = True
        self.pause_dlg.show()

        self.ContinueButton.setEnabled(True)
        self.PauseButton.setEnabled(False)

    # 正常继续实验
    @Slot()
    def continue_task(self):
        self.is_paused = False
        self.LossChecked = True
        self.pause_loop.quit()

        self.ContinueButton.setEnabled(False)
        self.PauseButton.setEnabled(True)
    
    # 掉线，终止实验
    @Slot()
    def connection_loss(self):
        if self.baseline_set == False:
            self.baseline_dlg.accept()
            
        self.reset()

        dlg = QMessageBox(self)
        dlg.setWindowTitle('Error')
        dlg.setText('丢失网络连接！')
        dlg.setIcon(QMessageBox.Critical)
        dlg.exec_()

        # 退出start
        self.end_flag = True
        self.pause_loop.quit()

        # 关闭重连对话框
        self.reconnect_dlg.accept()

    # 收到第一个正确的包，实验开始
    @Slot()
    def enable_exp(self, time):
        self.begin_exp = True
        # 记录一下第一个包到达的时间
        self.FirstPackTime = convert_time(time)

    # 记录收到包的数量
    @Slot()
    def updateSampleCount(self, new_count):
        self.sample_count += new_count

    # 5s基线测试
    @Slot()
    def setBaseline(self, data):
        if self.ready == True:
            if self.baseline_cnt < self.baseline_all:
                self.baseline_data[:,self.baseline_cnt*pack_len:(self.baseline_cnt+1)*pack_len] = data['EMG']
                self.baseline_cnt += 1
                if self.baseline_cnt == self.baseline_all:
                    self.EMGBaseline = np.mean(self.baseline_data, axis=1)
                    self.baseline_sig.baseline_ok.emit({'EMG':self.EMGBaseline})
                    self.dr.EMGBaseline = self.EMGBaseline
                    self.pause_loop.quit()
                    self.baseline_set = True
                    print('----------------------')
                    print('Baseline set!')
                    print('----------------------')
                    
    # 丢包情况
    @Slot()
    def CalLossRate(self, n_loss_pack, n_err_pack):
        loss_rate = (n_loss_pack + n_err_pack) / (self.pack_all + n_loss_pack)
        print('上次实验的丢包/错包率为：{:.2f}'.format(loss_rate*100) + '%')
        if not self.LossCheckOn.isChecked():
            return
        if loss_rate > LossThreshold:
            self.loss_dlg.show()
            self.is_paused = True
            self.ContinueButton.setEnabled(True)
            self.PauseButton.setEnabled(False)
        self.LossChecked = True
        
    # 改变增益
    @Slot()
    def GainChanged(self):
        gain_type = self.GainType.currentIndex()
        worker = GainChanger(gain_type, self.coon)
        self.threadpool.start(worker)
        
    # 在重连后更新socket
    @Slot()
    def UpdateSocket(self, coon):
        self.coon = coon['coon']
        

    # 关闭app
    def closeEvent(self, event):
        if self.flag == 1:
            dlg = QMessageBox.question(self, 'Message', '确认退出?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if dlg == QMessageBox.Yes:
                self.exit_app = True
                self.pause_loop.quit()
                self.reset()
                shutil.rmtree(self.path)
                event.accept()
            elif not self.is_paused:
                self.pause_task()
                event.ignore()
            else:
                event.ignore()
        else:
            event.accept()    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
