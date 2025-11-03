from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTime, QTimer
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from uv_led_controller import Controller
import os, json

try:
    controller_object = Controller()  
except Exception as e:
    print("unable to connect to the UV controller")

step_dictonary = {
    i: {"intensity": 0, "time":"00:00:00", "pos":0, "step": "STEP "+ str(i+1)}
    for i in range(0, 5)
}
pos_dictonary = {
    "pos": 0
}

# def func_ch_button(indicator):
#     if indicator.isChecked():
        
#         indicator.setChecked(False)
#     else:
        
#         indicator.setChecked(True)

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

    if (self.ch1_button.isChecked() and self.ch2_button.isChecked() and self.ch3_button.isChecked() and self.ch4_button.isChecked()):
        uv_list.append(0)
    else:
        if self.ch1_button.isChecked():
            uv_list.append(1)
        if self.ch2_button.isChecked():
            uv_list.append(2)
        if self.ch3_button.isChecked():
            uv_list.append(3)
        if self.ch4_button.isChecked():
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
    if (pos_dictonary["pos"] > 4):
        print("Step Procedure Completed")
        self.step_indicator.setChecked(False)
        
        orginal_style = self.intensity_control.styleSheet()
        orginal_style2 = self.timer_input.styleSheet()
        color_widget = getattr(self, f"step{pos_dictonary['pos']}_intensity")
        color_widget.setStyleSheet(orginal_style)
        color_widget = getattr(self, f"step{pos_dictonary['pos']}_time")
        color_widget.setStyleSheet(orginal_style2)
    else:
        if (step_dictonary[pos_dictonary["pos"]]["intensity"] == 0):
            print("Skipping step Ending Early")
            self.step_indicator.setChecked(False)
        else:
            orginal_style = self.intensity_control.styleSheet()
            orginal_style2 = self.timer_input.styleSheet()
            color_widget = getattr(self, f"step{pos_dictonary['pos']}_intensity")
            color_widget.setStyleSheet(orginal_style)
            color_widget = getattr(self, f"step{pos_dictonary['pos']}_time")
            color_widget.setStyleSheet(orginal_style2)

            self.step_display.setText(step_dictonary[pos_dictonary["pos"]]["step"])
            func_set_time_display(self, step_dictonary[pos_dictonary["pos"]]["time"])
            self.intensity_control.setValue(step_dictonary[pos_dictonary["pos"]]["intensity"])
            self.timer.start()

            color_widget = getattr(self, f"step{pos_dictonary['pos']+1}_intensity")
            color_widget.setStyleSheet("background-color: rgb(181, 234, 170); color: rgb(0, 0, 0);")
            color_widget = getattr(self, f"step{pos_dictonary['pos']+1}_time")
            color_widget.setStyleSheet("background-color: rgb(181, 234, 170); color: rgb(0, 0, 0);")

        pos_dictonary["pos"] += 1

def func_manual_mode(self):
    if(self.manual_box.isChecked()):
        print("Going Manual, Disabling GUI")
        controller_object.func_manual_control_enable()
    else:
        print("Going Program mode, enabling GUI") 
        controller_object.func_program_control_enable()

def func_start_step_control(self):

    pos_dictonary["pos"] = 0
    self.step_indicator.setChecked(True)

    for i in range (5):
        step_num = i + 1
        intensity_widget = getattr(self, f"step{step_num}_intensity")
        time_widget = getattr(self, f"step{step_num}_time")
        step_dictonary[i]["intensity"] = int(intensity_widget.value())
        step_dictonary[i]["time"] = time_widget.text().split(":")

    pos_dictonary["pos"] += 1
    
    func_set_time_display(self, self.step1_time.text().split(":"))
    self.intensity_control.setValue(int(self.step1_intensity.value()))
    self.step_display.setText( step_dictonary[0]["step"])

    color_widget = getattr(self, f"step{pos_dictonary['pos']}_intensity")
    color_widget.setStyleSheet("background-color: rgb(181, 234, 170); color: rgb(0, 0, 0);")
    color_widget = getattr(self, f"step{pos_dictonary['pos']}_time")
    color_widget.setStyleSheet("background-color: rgb(181, 234, 170); color: rgb(0, 0, 0);")

    start_timer(self)  
    
def func_time_comboBox(self):
    
    current_index = self.time_comboBox.currentIndex()
    if(current_index == 0):
        self.timer_input.setText("00:03:00")
    elif(current_index == 1):
        self.timer_input.setText("00:05:00")
    elif(current_index == 2):
        self.timer_input.setText("00:20:00")

def func_open_json():
    with open("saved_procedure.json") as file:
        data = json.load(file)
    return data

def func_step_comboBox(self):
    current_index = self.step_comboBox.currentIndex()

    if current_index == 0:
        self.save_procedure_button.show()
        self.save_procedure_input.show()
    else:
        data = func_open_json()

        self.save_procedure_button.hide()
        self.save_procedure_input.hide()
            
        self.step1_intensity.setValue(data[str(current_index)]["step_1_value"])
        self.step2_intensity.setValue(data[str(current_index)]["step_2_value"])
        self.step3_intensity.setValue(data[str(current_index)]["step_3_value"])
        self.step4_intensity.setValue(data[str(current_index)]["step_4_value"])
        self.step5_intensity.setValue(data[str(current_index)]["step_5_value"])
        self.step1_time.setText(data[str(current_index)]["step_1_time"])
        self.step2_time.setText(data[str(current_index)]["step_2_time"])
        self.step3_time.setText(data[str(current_index)]["step_3_time"])
        self.step4_time.setText(data[str(current_index)]["step_4_time"])
        self.step5_time.setText(data[str(current_index)]["step_5_time"])

def func_save_procedure(self):

    new_data = {
     str(self.step_comboBox.count()): {
        "procedure": self.save_procedure_input.text(),        
        "step_1_value": self.step1_intensity.value(), 
        "step_2_value": self.step2_intensity.value(), 
        "step_3_value": self.step3_intensity.value(), 
        "step_4_value": self.step4_intensity.value(), 
        "step_5_value": self.step5_intensity.value(), 
        "step_1_time": self.step1_time.text(), 
        "step_2_time": self.step2_time.text(), 
        "step_3_time": self.step3_time.text(), 
        "step_4_time": self.step4_time.text(), 
        "step_5_time": self.step5_time.text()
        }
    }
    self.step_comboBox.addItem(new_data[str(self.step_comboBox.count())]["procedure"])
   
    with open("saved_procedure.json", "r") as file:
        existing_data = json.load(file)
    
    existing_data.update(new_data)

    with open("saved_procedure.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controller_Design.ui") 
        uic.loadUi(ui_file_path, self)
 
        # self.ch1_button.clicked.connect(lambda: func_ch_button(self.ch1_indicator))
        # self.ch2_button.clicked.connect(lambda: func_ch_button(self.ch2_indicator))
        # self.ch3_button.clicked.connect(lambda: func_ch_button(self.ch3_indicator))
        # self.ch4_button.clicked.connect(lambda: func_ch_button(self.ch4_indicator))

        self.setIntensity1_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity1_button))
        self.setIntensity2_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity2_button))
        self.setIntensity3_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity3_button))
        self.setIntensity4_button.clicked.connect(lambda: func_setIntensity_button(self.intensity_control, self.setIntensity4_button))

        self.saveIntensity1_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity1_button))
        self.saveIntensity2_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity2_button))
        self.saveIntensity3_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity3_button))
        self.saveIntensity4_button.clicked.connect(lambda: func_saveIntensity_button(self.intensity_control, self.setIntensity4_button))

        self.timer_input.setInputMask("00:00:00;_")
        self.step1_time.setInputMask("00:00:00;_")
        self.step2_time.setInputMask("00:00:00;_")
        self.step3_time.setInputMask("00:00:00;_")
        self.step4_time.setInputMask("00:00:00;_")
        self.step5_time.setInputMask("00:00:00;_")

        time_regex = QRegularExpression("^(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d$")
        time_validator = QRegularExpressionValidator(time_regex, self.timer_input)

        self.timer_input.setValidator(time_validator)
        self.step1_time.setValidator(time_validator)
        self.step2_time.setValidator(time_validator)
        self.step3_time.setValidator(time_validator)
        self.step4_time.setValidator(time_validator)
        self.step5_time.setValidator(time_validator)
        
        self.onOff_button.clicked.connect(lambda: func_uv_onOff_button(self, controller_object))
        self.confirmTimer_button.clicked.connect(lambda: func_setTimer(self))

        self.manual_box.clicked.connect(lambda: func_manual_mode(self))
        self.step_control_button.clicked.connect(lambda: func_start_step_control(self))


        self.time_comboBox.currentIndexChanged.connect(lambda: func_time_comboBox(self))
        self.step_comboBox.currentIndexChanged.connect(lambda: func_step_comboBox(self))

        self.save_procedure_button.clicked.connect(lambda: func_save_procedure(self))
        self.save_procedure_button.hide()
        self.save_procedure_input.hide()

        data = func_open_json()

        for procedure_id, procedure in data.items():
            print(procedure["procedure"])
            self.step_comboBox.addItem(procedure["procedure"])

        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(lambda: update_time(self))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())