# Import the required libraries
import customtkinter
import tkinterdnd2 as tkinterDnD
from tkinter import filedialog
import time
import os
import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure
import subprocess
import sys
import json
import os

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.geometry(f"{1100}x{580}")


app.title("Combined Environment Control Interface")
# app.grid_rowconfigure(0, weight=1)
# app.grid_rowconfigure(1, weight=1)

# configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

radiobutton_var = customtkinter.IntVar(value=1)
label_font = ("Arial", 14)
label_font_small = ("Arial", 12)
desktop_directory = os.path.expanduser("~/Desktop")


class Widget():
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory.set(directory)

    def calibrate(self):
        print('\n~~~~~Calibrate SAL~~~~~')
        print('Saleae Channels: ', self.saleae_segmented_button_2.get())
        print('Saleae Buffer Size: ', self.saleae_combobox_2_1.get())
        print('Saleae Sampling Rate: ', self.saleae_combobox_2_2.get())
        print('Saleae Device Id: ', self.saleae_entry_2.get())

        master_folder_path = self.selected_directory.get()
        experiment_folder = master_folder_path + r"/" + 'ExperimentName'
        # experiment_folder = r"/mnt/desktop" + r"/" + 'ExperimentName'
        calibration_subfolder = r'calibration_saleae'
        voltages_subfolder = r'voltages_saleae'
        voltages_analog_subfolder = voltages_subfolder + r'/analog_voltages'

        total_seconds = 30

        saleae_channels = self.saleae_segmented_button_2.get()
        saleae_buffer_size = self.saleae_combobox_2_1.get()
        saleae_sampling_rate = self.saleae_combobox_2_2.get()
        saleae_device_id = self.saleae_entry_2.get()

        # Experiment parameters
        parameters_dict = {"master_folder_path": master_folder_path, "experiment_folder": experiment_folder, "calibration_subfolder": calibration_subfolder, "voltages_subfolder": voltages_subfolder, 'voltages_analog_subfolder': voltages_analog_subfolder,
                           "total_seconds": total_seconds, "saleae_channels": saleae_channels, "saleae_buffer_size": saleae_buffer_size, "saleae_sampling_rate": saleae_sampling_rate, "saleae_device_id": saleae_device_id}

        # Check and create each subfolder
        for subfolder_path in [experiment_folder]:
            if not os.path.exists(experiment_folder+'/'+subfolder_path):
                os.mkdir(subfolder_path)
                print(f"Subfolder {subfolder_path} created successfully.")
            else:
                print(f"Subfolder {subfolder_path} already exists.")

        dict_name = r"\calibration_parameters.json"
        path_to_save_parameters = experiment_folder + dict_name

        # Save parameters as JSON
        with open(path_to_save_parameters, "w") as json_file:
            json.dump(parameters_dict, json_file)
        print("Parameters Dictionary saved as JSON in 'calibration_parameters.json'")
        json_string = json.dumps(parameters_dict)

        script_path_saleae = r"Modules/Saleae.py"

        def run_script(script_path):
            process = subprocess.Popen(["python", script_path, json_string])
            return process

        def close_script(process):
            process.communicate()
            process.kill()

        calibration_saleae = run_script(script_path_saleae)
        close_script(calibration_saleae)

    def start(self):
        print('Switch Syringe Pump: ', self.switch_syringe_pump.get())
        print('Syringe Pump COM: ', self.syring_pump_combobox_1_0.get())
        print('Syringe Pump Syringe: ', self.syring_pump_segmented_button_1.get())
        print('Syringe Pump Syringe Type: ',
              self.syring_pump_combobox_1_2.get())
        print('Syringe Pump Syringe Volume: ', self.syring_pump_entry_1.get())
        print('Syringe Pump Flow Rate: ', self.syring_pump_entry_1_2.get())

        print('Switch Saleae: ', self.saleae_switch_2.get())
        print('Saleae Channels: ', self.saleae_segmented_button_2.get())
        print('Saleae Buffer Size: ', self.saleae_combobox_2_1.get())
        print('Saleae Sampling Rate: ', self.saleae_combobox_2_2.get())
        print('Saleae Device Id: ', self.saleae_entry_2.get())

        print('Switch Fluigent: ', self.switch_3.get())

        print('Switch SLS: ', self.sls_switch_4.get())

        print('Experiment Folder Name: ', self.entry_5_1.get())
        print('Export Directory: ', self.selected_directory.get())
        print('Capture Duration: ', self.entry_5.get())
        duration = int(self.entry_5.get())

        if duration > 0:
            self.countdown(duration)
            self.time_remaining.set(0)
            self.progressbar_5.set(0)

    def switch_syringe_pump(self):
        # Define logic for Syringe Pump switch
        pass

    def switch_saleae(self):
        # Define logic for Saleae switch
        pass

    def switch_fluigent(self):
        # Define logic for Fluigent switch
        pass

    def switch_sls(self):
        # Define logic for SLS switch
        pass

    def countdown(self, duration):
        for i in range(duration, -1, -1):
            self.time_remaining.set(i)
            progress = 1 - ((duration - i) / duration)
            self.progressbar_5.set(progress)
            app.update()
            time.sleep(1)

    def create_syringe_pump_frame(self, app, width_syringe_frame=200, padx=20, pady=20):
        width_syringe_frame = width_syringe_frame

        self.frame_1 = customtkinter.CTkFrame(master=app)
        self.frame_1.grid(row=0, column=0, padx=padx, pady=pady, sticky="nsew")

        label_1 = customtkinter.CTkLabel(
            master=self.frame_1, justify=customtkinter.LEFT, text="Pump 33 DDS", font=label_font)
        label_1.pack(pady=10, padx=10)

        self.switch_syringe_pump = customtkinter.CTkSwitch(
            master=self.frame_1, text="On/Off", command=self.switch_syringe_pump)
        self.switch_syringe_pump.pack(pady=10, padx=10)

        self.syring_pump_combobox_1_0 = customtkinter.CTkComboBox(
            self.frame_1, values=['COM'+str(i) for i in range(1, 13)], width=width_syringe_frame)
        self.syring_pump_combobox_1_0.pack(pady=10, padx=10)
        self.syring_pump_combobox_1_0.set("Choose COM")

        self.syring_pump_segmented_button_1 = customtkinter.CTkSegmentedButton(
            master=self.frame_1, values=["       Syringe A       ", "       Syringe B       "], width=width_syringe_frame)
        self.syring_pump_segmented_button_1.pack(pady=10, padx=10)

        self.syring_pump_combobox_1_2 = customtkinter.CTkComboBox(
            self.frame_1, values=["BDP", "BDG"], width=width_syringe_frame)
        self.syring_pump_combobox_1_2.pack(pady=10, padx=10)
        self.syring_pump_combobox_1_2.set("Syringe Type")

        self.entry_1_text_var = customtkinter.StringVar()
        self.syring_pump_entry_1 = customtkinter.CTkEntry(
            master=self.frame_1, placeholder_text="Syringe Volume [mL] ", width=width_syringe_frame)
        self.syring_pump_entry_1.pack(pady=10, padx=10)

        self.syring_pump_entry_1_2 = customtkinter.CTkEntry(
            master=self.frame_1, placeholder_text="Flow Rate [uL/min] ", width=width_syringe_frame)
        self.syring_pump_entry_1_2.pack(pady=10, padx=10)

    def create_saleae_frame(self, app, width_saleae_frame=200, padx=20, pady=20):
        width_saleae = width_saleae_frame
        frame_2 = customtkinter.CTkFrame(master=app)
        frame_2.grid(row=0, column=1, padx=padx, pady=pady, sticky="nsew")

        label_2 = customtkinter.CTkLabel(
            master=frame_2, justify=customtkinter.LEFT, text="Saleae - Logic Pro 8", font=label_font)
        label_2.pack(pady=10, padx=10)

        self.saleae_switch_2 = customtkinter.CTkSwitch(
            master=frame_2, text="On/Off", command=self.switch_saleae)
        self.saleae_switch_2.pack(pady=10, padx=10)

        self.saleae_segmented_button_2 = customtkinter.CTkSegmentedButton(
            master=frame_2, values=[" Channel 0-1-2-3 ", " Channel 4-5-6-7 "], width=width_saleae)
        self.saleae_segmented_button_2.pack(pady=10, padx=10)

        self.saleae_combobox_2_1 = customtkinter.CTkComboBox(
            frame_2,  values=[f"{i} GB" for i in range(1, 13)], width=width_saleae)
        self.saleae_combobox_2_1.pack(pady=10, padx=10)
        self.saleae_combobox_2_1.set("Buffer Size [GB]")

        self.saleae_combobox_2_2 = customtkinter.CTkComboBox(
            frame_2, values=['781250', '1562500', '3125000'], width=width_saleae)
        self.saleae_combobox_2_2.pack(pady=10, padx=10)

        entry_2_text_var = customtkinter.StringVar()
        self.saleae_entry_2 = customtkinter.CTkEntry(
            master=frame_2, placeholder_text="Device Id", width=width_saleae)
        self.saleae_entry_2.pack(pady=10, padx=10)

        self.calibrate_button = customtkinter.CTkButton(
            master=frame_2, text="Calibrate SALEAE", command=self.calibrate, fg_color="#777777")
        self.calibrate_button.pack(pady=10, padx=10)

    def create_fluigent_frame(self, app, width_fluigent_frame=100, padx=20, pady=20):
        width_fluigent_frame = width_fluigent_frame
        self.frame_3 = customtkinter.CTkFrame(master=app)
        self.frame_3.grid(row=0, column=2, padx=padx, pady=pady, sticky="nsew")

        label_fluigent = customtkinter.CTkLabel(
            master=self.frame_3, justify=customtkinter.LEFT, text="LineUp™ Push-Pull", font=label_font)
        label_fluigent.pack(pady=10, padx=10)

        self.switch_3 = customtkinter.CTkSwitch(
            master=self.frame_3, text="On/Off", command=self.switch_fluigent)
        self.switch_3.pack(pady=10, padx=10)

        self.flg_tabview_1 = customtkinter.CTkTabview(
            master=self.frame_3, width=width_fluigent_frame)
        self.flg_tabview_1.pack(pady=10, padx=10)
        self.flg_tabview_1.add("Controller 1")
        self.flg_tabview_1.add("Controller 2")
        self.flg_tabview_1.set("Controller 1")

        entry_p1_start = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 1"), placeholder_text="Start Pressure", width=width_fluigent_frame)
        entry_p1_start.pack(padx=20, pady=20)
        entry_p1_end = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 1"), placeholder_text="End Pressure", width=width_fluigent_frame)
        entry_p1_end.pack(padx=20, pady=20)
        entry_p1_step = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 1"), placeholder_text="Pressure Step", width=width_fluigent_frame)
        entry_p1_step.pack(padx=20, pady=20)

        entry_pp1_start = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 2"), placeholder_text="1: Start Pressure", width=width_fluigent_frame)
        entry_pp1_start.pack(padx=2, pady=2)
        entry_pp1_end = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 2"), placeholder_text="1: End Pressure", width=width_fluigent_frame)
        entry_pp1_end.pack(padx=2, pady=2)
        entry_pp1_step = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 2"), placeholder_text="1:Pressure Step", width=width_fluigent_frame)
        entry_pp1_step.pack(padx=2, pady=2)

        entry_pp2_start = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 2"), placeholder_text="2: Start Pressure", width=width_fluigent_frame)
        entry_pp2_start.pack(padx=2, pady=2)
        entry_pp2_end = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 2"), placeholder_text="2: End Pressure", width=width_fluigent_frame)
        entry_pp2_end.pack(padx=2, pady=2)
        entry_pp2_step = customtkinter.CTkEntry(master=self.flg_tabview_1.tab(
            "Controller 2"), placeholder_text="2:Pressure Step", width=width_fluigent_frame)
        entry_pp2_step.pack(padx=2, pady=2)

    def create_sls_frame(self, app, width_sls_frame=100, padx=20, pady=20):

        width_sls_frame = width_sls_frame
        self.frame_4 = customtkinter.CTkFrame(master=app)
        self.frame_4.grid(row=0, column=3, padx=padx, pady=pady, sticky="nsew")

        label_flow_sensors = customtkinter.CTkLabel(
            master=self.frame_4, justify=customtkinter.LEFT, text="Flow Sensors", font=label_font,)
        label_flow_sensors.pack(pady=10, padx=10)

        self.sls_switch_4 = customtkinter.CTkSwitch(
            master=self.frame_4, text="SLS-1500", command=self.switch_sls)
        self.sls_switch_4.pack(pady=10, padx=10)

        self.sls_combobox_1_0 = customtkinter.CTkComboBox(
            self.frame_4, values=['COM'+str(i) for i in range(1, 13)], width=width_sls_frame)
        self.sls_combobox_1_0.pack(pady=10, padx=10)
        self.sls_combobox_1_0.set("Choose COM")

        self.flg_m_switch_4 = customtkinter.CTkSwitch(
            master=self.frame_4, text="Flow Unit M+", command=self.switch_sls)
        self.flg_m_switch_4.pack(pady=10, padx=10)

    def create_capture_param_frame(self, app, width_bottom_frame=400, padx=20, pady=20):
        frame_bottom = customtkinter.CTkFrame(master=app)
        frame_bottom.grid(row=1, column=0, columnspan=4, padx=padx,
                          pady=pady, sticky="nsew")

        label_5 = customtkinter.CTkLabel(
            master=frame_bottom, justify=customtkinter.LEFT, text="CAPTURE PARAMETERS", font=label_font)
        label_5.pack(pady=10, padx=10)

        width_bottom_frame = width_bottom_frame

        self.entry_5_1 = customtkinter.CTkEntry(
            master=frame_bottom, placeholder_text="Experiment Folder Name", width=width_bottom_frame)
        self.entry_5_1.pack(pady=10, padx=10)

        self.selected_directory = customtkinter.StringVar()
        self.selected_directory.set(desktop_directory)

        self.select_location_button = customtkinter.CTkButton(
            master=frame_bottom, text="Change Export Directory", command=self.browse_directory)
        self.select_location_button.pack(pady=10, padx=10)

        self.selected_directory_label = customtkinter.CTkLabel(
            master=frame_bottom, textvariable=self.selected_directory)
        self.selected_directory_label.pack(pady=10, padx=10)

        self.entry_5 = customtkinter.CTkEntry(
            master=frame_bottom, placeholder_text="Capture Duration [s]", width=width_bottom_frame,)
        self.entry_5.pack(pady=10, padx=10)

        self.time_remaining = customtkinter.IntVar()
        self.time_remaining.set(0)
        self.time_remaining_label = customtkinter.CTkLabel(
            master=frame_bottom, textvariable=self.time_remaining, font=("Arial", 14))
        self.time_remaining_label.pack(pady=10, padx=10)

        self.progressbar_5 = customtkinter.CTkProgressBar(
            master=frame_bottom, width=width_bottom_frame, height=20, fg_color="#333333")
        self.progressbar_5.pack(pady=2, padx=10)
        self.progressbar_5.set(1)

        self.start_button = customtkinter.CTkButton(
            master=frame_bottom, text="Start", command=self.start)
        self.start_button.pack(pady=10, padx=10)


# for i in range(4):
#     app.grid_columnconfigure(i, weight=1)

create_window = Widget()
create_window.create_syringe_pump_frame(app)
create_window.create_saleae_frame(app)
create_window.create_fluigent_frame(app)
create_window.create_sls_frame(app)
create_window.create_capture_param_frame(app)
# create_window.creat_flg_M_fram(app)

app.mainloop()
