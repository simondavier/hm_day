#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from scipy.fftpack import fft 
from matplotlib.pyplot import xticks, yticks

#%matplotlib tk
CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 #48000

p = pyaudio.PyAudio()

#make the stream as wave file
stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
    )

#data = stream.read(CHUNK)
#print data
#print len(data)
#data_int = struct.unpack(str(2 * CHUNK)+ 'B',data)
#data_int = np.array(struct.unpack(str(2 * CHUNK)+ 'B',data), dtype='int')[::2]
#print data_int

#fig, ax = plt.subplots()
fig, (ax, ax2) = plt.subplots(2, figsize=(8,6))

x = np.arange(0, 2 * CHUNK, 2) #x ax value, from 0 to 2048, step=2
x_fft = np.linspace(0, RATE, CHUNK) # 44.1k采样率，按2个字节均匀分布

line, = ax.plot(x, np.random.rand(CHUNK),'b-',lw=2)
line_fft, = ax2.plot(x_fft,np.random.rand(CHUNK),'r-',lw=1)
#line_fft, = ax2.semilogx(x_fft,np.random.rand(CHUNK),'r-',lw=2)

ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
#ax.set_ylim(0,255)
ax.set_ylim(0,CHUNK)
ax.set_xlim(0,2*CHUNK)

ax2.set_xlabel('AUDIO FREQUENCY')

plt.setp(
    ax, yticks=[0, 128, CHUNK],
    xticks = [0, CHUNK, 2*CHUNK]
    )

plt.setp(ax2, yticks = [0, 1],)

ax2.set_xlim(20, RATE / 2) #x轴20-20kHz

tstart = time.time()
num_plots = 0

while time.time()-tstart < 1000:
    data = stream.read(CHUNK)
    #data_int = np.array(struct.unpack(str(2 * CHUNK)+ 'B',data), dtype='int')[::2]
    data_int = struct.unpack(str(2 * CHUNK)+ 'B',data)
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    audio_data = np.fromstring(data, dtype=np.short)
    print np.abs(audio_data[0:])
    
    """if np.max(audio_data)>500:
        raise RuntimeError("Volume is unmute!")"""#if unmute
    line.set_ydata(audio_data)
    #line.set_ydata(data_np)
    #fig.canvas.draw()
    #fig.canvas.flush_events()
    y_fft = fft(data_int)
    line_fft.set_ydata(np.abs(y_fft[0:CHUNK]) / (128 * CHUNK))
    plt.pause(0.001)
    num_plots += 1
#ax.plot(data_int,'-')
plt.show()

"""fig, ax = plt.subplots()

tstart = time.time()
num_plots = 0
while time.time()-tstart < 100:
    ax.clear()
    ax.plot(np.random.randn(1000))
    #plt.pause(0.001) # interval seconds 
    num_plots += 1
print(num_plots)
"""

"""fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))
print line

tstart = time.time()
num_plots = 0
while time.time()-tstart < 100:
    line.set_ydata(np.random.randn(100))
    plt.pause(0.001)
    num_plots += 1
print(num_plots)
"""

"""fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))

tstart = time.time()
num_plots = 0
while time.time()-tstart < 100:
    line.set_ydata(np.random.randn(100))
    fig.canvas.draw()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots)
"""

"""fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))
plt.show(block=False)

tstart = time.time()
num_plots = 0
while time.time()-tstart < 50:
    line.set_ydata(np.random.randn(100))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.update()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots/5)"""