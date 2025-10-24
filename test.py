from PyExpLabSys.drivers.hamamatsu import LCL1V5
import time

lc_l1v5 = LCL1V5(port="COM8")
lc_l1v5.select_command_communication()

#will turn on and off automatically, 3 requirements (channel, (intensity), (time)) 
# < 10s it has to be in decimal (EX: 8.5s) >10 can be int numbers. Max time allowed is 99s
lc_l1v5.set_step_settings(0, ("021",'022','033'),('2.2','2.2','2.2'))
lc_l1v5.switch_led_on(0)
time.sleep(5)
lc_l1v5.set_step_settings(0, ("050",'022','033'),('2.2','2.2','2.2'))
time.sleep(2)
lc_l1v5.switch_led_off(0)
#Starts the whole program
#lc_l1v5.start_stepped_program(0)


