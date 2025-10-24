from PyExpLabSys.drivers.hamamatsu import LCL1V5

lc_l1v5 = LCL1V5(port="COM8")
lc_l1v5.comm("CNT0")
lc_l1v5.check_control_mode()

