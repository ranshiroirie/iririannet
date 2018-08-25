# !/usr/bin/env python
# coding: utf-8
# pyaudioをインポート
import pyaudio

# PyAudioクラスのインスタンスを取得
a = pyaudio.PyAudio()

# ホストAPI数
hostAPICount = a.get_host_api_count()
print "Host API Count = " + str(hostAPICount)

# ホストAPIの情報を列挙
for cnt in range(0, hostAPICount):
    print a.get_host_api_info_by_index(cnt)
    
# ASIOデバイスの情報を列挙
asioInfo = a.get_host_api_info_by_type(pyaudio.paASIO)
print "ASIO Device Count = " + str(asioInfo.get("deviceCount"))
for cnt in range(0, asioInfo.get("deviceCount")):
    print a.get_device_info_by_host_api_device_index(asioInfo.get("index"), cnt)