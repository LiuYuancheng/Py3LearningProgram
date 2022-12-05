# reference link: https://stackoverflow.com/questions/57664320/how-to-record-mouse-and-keyboard-movement-simultaneously-with-python


import threading
import mouse
import keyboard

mouse_events = []


mouse.hook(mouse_events.append)
keyboard.start_recording()

keyboard.wait("a")

mouse.unhook(mouse_events.append)
keyboard_events = keyboard.stop_recording()

#Keyboard threadings:

k_thread = threading.Thread(target = lambda :keyboard.play(keyboard_events))
k_thread.start()

#Mouse threadings:

m_thread = threading.Thread(target = lambda :mouse.play(mouse_events))
m_thread.start()

#waiting for both threadings to be completed

k_thread.join() 
m_thread.join()