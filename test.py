import pygame as pg
import pygame.event as ev
import pygame.midi as md

pg.init()
md.init()

print(md.get_count())
print(md.get_default_input_id())

i = 0
info_list = []
while md.get_device_info(i) is not None:
    current_info = md.get_device_info(i)
    info_list.append(current_info)
    i += 1
#port_list = [(each[1].decode('utf-8'), i)
#                 for i, each in enumerate(info_list) if each[2] == 0]
#    port_name_list = [i[0] for i in port_list]
#player_list = [
#    pygame.midi.Output(port_list[port_name_list.index(i)][1])
#    for i in ports if i in port_name_list
#]

print(info_list)
for i in range(md.get_count()):
    print(md.get_device_info(i), i)
#print(port_list)

#print(md.Input(3))
pg.display.set_mode((1, 1))
import time
from time import sleep
delaySeconds = 10 # For 15 minutes delay 
close_time = time.time()+delaySeconds
midi_in=md.Input(3)

while close_time>time.time():
    
    sleep(.1)
    midi_data=md.Input.read(midi_in, 100)
    print(len(midi_data))
    for i in range(len(midi_data)):
        midi_note, timestamp = midi_data[i]
        print(timestamp, hex(midi_note[0]), hex(midi_note[1]), hex(midi_note[2]))
        print()
    
    continue
    exit
    run = True
    while run:
        while(md.Input.poll(midi_in) == False):
            sleep(.1)
            continue
        #if run == False:
        #  pygame.midi.Input.close(midi_in)
        #  pygame.midi.quit()
        #  return
        sleep(0.1)
              
    midi_data = md.Input.read(midi_in, 1)
    midi_note, timestamp = midi_data[0]
    print(timestamp)
    print(midi_note)
    print(midi_data)
    #ev.wait()
    #ev.get()
    #print(md.Input(3).read(1))

md.quit()

