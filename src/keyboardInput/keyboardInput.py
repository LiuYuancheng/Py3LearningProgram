import keyboard
import time
keyboard.press_and_release('windows+r')
time.sleep(0.5)
keyboard.press_and_release('backspace')
time.sleep(0.5)
keyboard.write('powerShell')
time.sleep(0.5)
keyboard.press_and_release('enter')
time.sleep(1)
for char in 'start-process':
    time.sleep(0.05)
#keyboard.write('start-process PowerShell -verb runas')
    keyboard.press_and_release(char)

time.sleep(1)
keyboard.press_and_release('space, shift+p')


time.sleep(1)
for char in 'owerShell -verb runas':
    time.sleep(0.05)
    keyboard.press_and_release(char)

time.sleep(1)

keyboard.press_and_release('enter')
time.sleep(2)

#for char in 'Set-MpPreference -DisableRealtimeMonitoring $true':
#    time.sleep(0.1)
#    keyboard.press_and_release(char)

keyboard.press_and_release('windows+r')