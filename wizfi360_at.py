import os, sys
import utime
from machine import UART,Pin
print(os.uname())
led = machine.Pin(25, machine.Pin.OUT)
led.value(0)
utime.sleep(0.5)
led.value(1)
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
uart = machine.UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
print("UART Setting...")
print(uart)
def sendCMD_waitResp(cmd, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd.encode('utf-8'))
    waitResp(timeout)
    print()   
def waitResp(timeout):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp)
sendCMD_waitResp("AT\r\n") 
sendCMD_waitResp("AT+GMR\r\n") 
utime.sleep(0.5)
sendCMD_waitResp("AT+RST\r\n")
sendCMD_waitResp("AT+CWMODE_CUR=1\r\n") 
sendCMD_waitResp("AT+CWDHCP_CUR=1,1\r\n") 
utime.sleep(0.5)
sendCMD_waitResp('AT+CWJAP_CUR="TP_Link_01D4","61173491"\r\n') 
sendCMD_waitResp("AT+CIPSTA_CUR?\r\n") 
sendCMD_waitResp("AT+CIPMUX=1\r\n")
sendCMD_waitResp('AT+CIPSTART=1, "TCP","192.168.0.103",5000\r\n')
print("connected...")
print("RPi-PICO with WizFi360")
Data = bytes()
while True:
    reading = sensor_temp.read_u16() * conversion_factor  
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    temp = str(temperature)
    utime.sleep(1)
    sendCMD_waitResp("AT+CIPSENDBUF=1,20\r\n")
    sendCMD_waitResp("Temperature: ")
    send = uart.write(temp.encode('utf-8'))
