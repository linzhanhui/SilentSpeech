import time
import numpy as np
import math
import datetime

def get_current_time():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s%03d" % (data_head, data_secs)
    return time_stamp


def get_data(data):
    data = data.hex()
    for i in range(4):
        bin_data_tmp = bin(int(data[2 * i:2 * i + 2], 16))[2:]
        if len(bin_data_tmp) < 8:
            loss = 8 - len(bin_data_tmp)
            for j in range(loss):
                bin_data_tmp = '0' + bin_data_tmp
        if i == 0:
            data_out = bin_data_tmp
        else:
            data_out = bin_data_tmp + data_out

    sign = int(data_out[0], 2)
    exp = int(data_out[1:9], 2)
    frac = int(data_out[9:32], 2)

    if exp == 0:
        data_out = ((-1) ** sign) * (2 ** (-126)) * (frac / (2 ** 23))
    else:
        data_out = ((-1) ** sign) * (2 ** (exp - 127)) * (1 + (frac / (2 ** 23)))

    return data_out

def convert_time(time):
    return int(time[0:2]) * 3600 * 1000 + int(time[2:4]) * 60 * 1000 + int(time[4:6]) * 1000 + int(time[6:])


# feature extraction, input should be of shape (n_channels, n_samples)

def feature_extraction(x, window_len=2, step_len=2):

    fs = 1000
    zc_ssc_thresh = 0.0004

    x = x.T

    # rms
    rms = get_rms(x, window_len=window_len, step_len=step_len, fs=fs).reshape(1, -1)

    # ssc
    ssc = get_ssc(x, window_len=window_len, step_len=step_len,
                  fs=fs, threshold=zc_ssc_thresh).reshape(1, -1)
    # zc
    zc = get_zc(x, window_len=window_len, step_len=step_len,
                fs=fs, threshold=zc_ssc_thresh).reshape(1, -1)
    
    # wl
    wl = get_wl(x, window_len=window_len, step_len=step_len, fs=fs).reshape(1, -1)

    feature_vec = np.concatenate((rms, ssc, zc, wl), axis=1).reshape(-1)

    return feature_vec

# root mean square

def my_rms(signal):
    return np.mean(signal**2)

def get_rms(signal, window_len, step_len, fs):

    # length of the sliding time window
    window_sample = math.floor(window_len * fs)

    # step length of the time window
    step_sample = math.floor(step_len * fs)

    N_samples, N_channels = signal.shape

    rms = np.zeros([math.floor((N_samples-window_sample)/step_sample)+1, N_channels])


    for idx, i in enumerate(range(0, N_samples-window_sample+1, step_sample)):
        for j in range(N_channels):
            signal_seg = signal[i:i+window_sample, j]
            rms[idx, j] = my_rms(signal_seg)


    return rms

# slope sign change

def my_ssc(signal, threshold):
    N = len(signal)
    ssc_value = 0

    for i in range(2, N-1):
        if ((signal[i] - signal[i-1]) * (signal[i] - signal[i+1]) > 0) and \
                ((np.abs(signal[i] - signal[i-1]) > threshold) or \
                 (np.abs(signal[i] - signal[i+1]) > threshold)):
            ssc_value += 1

    return ssc_value

def get_ssc(signal, window_len, step_len, fs, threshold):

    # length of the sliding time window
    window_sample = math.floor(window_len * fs)

    # step length of the time window
    step_sample = math.floor(step_len * fs)

    N_samples, N_channels = signal.shape

    ssc = np.zeros([math.floor((N_samples-window_sample)/step_sample)+1, N_channels])

    for idx, i in enumerate(range(0, N_samples - window_sample + 1, step_sample)):
        for j in range(N_channels):
            signal_seg = signal[i:i+window_sample, j]
            ssc[idx, j] = my_ssc(signal_seg, threshold)

    return ssc

# zero crossing

def my_zc(signal, threshold):
    N = len(signal)
    zc_value = 0

    for i in range(1, N-1):
        if (signal[i] * signal[i+1] < 0) and (np.abs(signal[i] - signal[i+1]) > threshold):
            zc_value += 1

    return zc_value

def get_zc(signal, window_len, step_len, fs, threshold):

    # length of the sliding time window
    window_sample = math.floor(window_len * fs)

    # step length of the time window
    step_sample = math.floor(step_len * fs)

    N_samples, N_channels = signal.shape

    zc = np.zeros([math.floor((N_samples-window_sample)/step_sample)+1, N_channels])

    for idx, i in enumerate(range(0, N_samples-window_sample+1, step_sample)):
        for j in range(N_channels):
            signal_seg = signal[i:i+window_sample, j]
            zc[idx, j] = my_ssc(signal_seg, threshold)

    return zc

# wave length

def my_wl(signal, fs):
    N = len(signal)
    wl_value = 0

    for i in range(1, N-1):
        wl_value += np.abs(signal[i+1] - signal[i])

    wl_value *= fs / N

    return wl_value

def get_wl(signal, window_len, step_len, fs):

    # length of the sliding time window
    window_sample = math.floor(window_len * fs)

    # step length of the time window
    step_sample = math.floor(step_len * fs)

    N_samples, N_channels = signal.shape

    wl = np.zeros([math.floor((N_samples-window_sample)/step_sample)+1, N_channels])

    for idx, i in enumerate(range(0, N_samples-window_sample+1, step_sample)):
        for j in range(N_channels):
            signal_seg = signal[i:i+window_sample, j]
            wl[idx, j] = my_wl(signal_seg, fs)

    return wl


