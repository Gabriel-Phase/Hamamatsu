from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTime, QTimer
from PyQt6.QtCore import QTimer, QTime
from uv_led_controller import Controller
import os

try:
    controller_object = Controller()  
except Exception as e:
    print("unable to connect to the UV controller")

step_dictonary = {
    i: {"intensity": 0, "time":"00:00:00", "pos":0, "step": "step "+ str(i+1)}
    for i in range(0, 5)
}

def func_ch_button(indicator, self):
    if indicator.isChecked():
        
        indicator.setChecked(False)
    else:
        
        indicator.setChecked(True)

def func_setIntensity_button(intensity_control, intensity_button):
    intensity_value = intensity_button.text()
    intensity_value = intensity_value.strip("%")
    print(intensity_value)
    intensity_control.setValue(int(intensity_value))
    
def func_saveIntensity_button(intensity_control, intensity_button):
    value = intensity_control.value()
    intensity_button.setText(str(value) + "%")

def func_uv_onOff_button(self, controller_object):
    intensity_control = self.intensity_control
    indicator = self.onOff_indicator

    controller_object.func_set_uv_intensity(intensity_control.value())

    uv_list = []

    if indicator.isChecked():
        print("Turning on the uv off")
        controller_object.func_uv_off()
        indicator.setChecked(False)
    else:
        print("Turning on the uv on... power set to", intensity_control.value())
        indicator.setChecked(True)

        uv_list = func_check_ch(self, uv_list)
        controller_object.func_uv_on(uv_list)

def func_check_ch(self, uv_list):

    if (self.ch1_indicator.isChecked() and self.ch2_indicator.isChecked() and self.ch3_indicator.isChecked() and self.ch4_indicator.isChecked()):
        uv_list.append(0)
    else:
        if self.ch1_indicator.isChecked():
            uv_list.append(1)
        if self.ch2_indicator.isChecked():
            uv_list.append(2)
        if self.ch3_indicator.isChecked():
            uv_list.append(3)
        if self.ch4_indicator.isChecked():
            uv_list.append(4)
    print(uv_list)
    
    return uv_list

def func_setTimer(self):

    entered_time = self.timer_input.text()

    print(entered_time)

    time_list = entered_time.split(":")

    func_set_time_display(self, time_list)
    
    start_timer(self)

def func_set_time_display(self, time_list):

    if(len(time_list) == 3):
        hours = time_list[0]
        min = time_list[1]
        sec = time_list[2]

    self.current_time = QTime(int(hours), int(min), int(sec))
    self.timer_display.setText(self.current_time.toString("hh:mm:ss"))

def start_timer(self):
    # func_uv_onOff_button(self, controller_object)
    self.timer.start()

def update_time(self):
    self.current_time = self.current_time.addSecs(-1)
    self.timer_display.setText(self.current_time.toString("hh:mm:ss"))
  
    if(self.current_time.toString("hh:mm:ss") == "00:00:00"):
        print("TIMER HIT")
        # func_uv_onOff_button(self, controller_object)
        self.timer.stop()
        if(self.step_indicator.isChecked()):
            func_next_step_control(self)

def func_next_step_control(self):
    if (step_dictonary[0]["pos"] > 4):
        print("Step Procedure Completed")
        self.step_indicator.setChecked(False)
    else:
        if (step_dictonary[step_dictonary[0]["pos"]]["intensity"] == 0):
            print("Skipping step Ending Early")
            self.step_indicator.setChecked(False)
        else:    
            self.step_display.setText(step_dictonary[step_dictonary[0]["pos"]]["step"])
            func_set_time_display(self, step_dictonary[step_dictonary[0]["pos"]]["time"])
            print(step_dictonary[step_dictonary[0]["pos"]]["time"])
            self.intensity_control.setValue(step_dictonary[step_dictonary[0]["pos"]]["intensity"])
            print(step_dictonary[step_dictonary[0]["pos"]]["intensity"])
            self.timer.start()
        step_dictonary[0]["pos"] += 1

def func_manual_mode(self):
    if(self.manual_box.isChecked()):
        print("Going Manual, Disabling GUI")
        controller_object.func_manual_control_enable()
    else:
        print("Going Program mode, enabling GUI") 
        controller_object.func_program_control_enable()

def func_start_step_control(self):
    step_dictonary[0]["pos"] = 0
    
    step1_intensity_value = self.step1_intensity.value()
    step2_intensity_value = self.step2_intensity.value()
    step3_intensity_value = self.step3_intensity.value()
    step4_intensity_value = self.step4_intensity.value()
    step5_intensity_value = self.step5_intensity.value()
    step1_time_value = self.step1_time.text()
    step2_time_value = self.step2_time.text()
    step3_time_value = self.step3_time.text()
    step4_time_value = self.step4_time.text()
    step5_time_value = self.step5_time.text()

    self.step_indicator.setChecked(True)
    
    step1_time = step1_time_value.split(":")
    step2_time = step2_time_value.split(":")
    step3_time = step3_time_value.split(":")
    step4_time = step4_time_value.split(":")
    step5_time = step5_time_value.split(":")
    


    step_dictonary[0]["intensity"] = int(step1_intensity_value)
    step_dictonary[0]["time"] = step1_time
    step_dictonary[1]["intensity"] = int(step2_intensity_value)
    step_dictonary[1]["time"] = step2_time
    step_dictonary[2]["intensity"] = int(step3_intensity_value)
    step_dictonary[2]["time"] = step3_time
    step_dictonary[3]["intensity"] = int(step4_intensity_value)
    step_dictonary[3]["time"] = step4_time
    step_dictonary[4]["intensity"] = int(step5_intensity_value)
    step_dictonary[4]["time"] = step5_time

    step_dictonary[0]["pos"] += 1
    
    func_set_time_display(self, step1_time)
    self.intensity_control.setValue(int(step1_intensity_value))
    self.step_display.setText( step_dictonary[0]["step"])
    start_timer(self)  
    
def func_time_comboBox(self):
    
    print(self.time_comboBox.currentIndexChanged())
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controller_Design.ui") 
        uic.loadUi(ui_file_path, self)
 
        self.ch1_button.clicked.connect(lambda: func_ch_button(self.ch1_indicator, self))
        self.ch2_button.clicked.connect(lambda: func_ch_button(self.ch2_indicator, self))
        self.ch3_button.clicked.connect(lambda: func_ch_button(self.ch3_indicator, self))
        self.ch4_button.clicked.connect(lambda: func_ch_button(self.ch4_indicator, self))

        self.setIntensity1_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity1_button))
        self.setIntensity2_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity2_button))
        self.setIntensity3_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity3_button))
        self.setIntensity4_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity4_button))

        self.saveIntensity1_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity1_button))
        self.saveIntensity2_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity2_button))
        self.saveIntensity3_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity3_button))
        self.saveIntensity4_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity4_button))

        self.onOff_button.clicked.connect(lambda: func_uv_onOff_button(self, controller_object))

        self.confirmTimer_button.clicked.connect(lambda: func_setTimer(self))
        self.manual_box.clicked.connect(lambda: func_manual_mode(self))
        self.step_control_button.clicked.connect(lambda: func_start_step_control(self))
        self.time_comboBox.currentIndexChanged.connect(lambda: func_time_comboBox(self))
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(lambda: update_time(self))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())