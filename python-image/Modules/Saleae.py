import os
import csv
import subprocess
import json
import sys

from saleae import automation

def gb_string_to_mb(gb_string):
    try:
        gb_value = int(gb_string.split()[0])
        mb_value = gb_value * 1000
        return mb_value
    except ValueError:
        # Handle the case where the input string cannot be converted to a float
        return None


def process_saleae(dict_parameters):
    # def process_saleae(exp_folder, voltages_path, pressure_path, total_seconds):
    print("Saleae processing started")
    master_folder_path = dict_parameters['master_folder_path']
    exp_folder = dict_parameters['experiment_folder']
    calibration_subfolder = dict_parameters['calibration_subfolder']
    voltages_subfolder = dict_parameters['voltages_subfolder']
    voltages_analog_subfolder = dict_parameters['voltages_analog_subfolder']
    total_seconds = dict_parameters['total_seconds']

    for subfolder_path in [exp_folder+'/'+calibration_subfolder, exp_folder+'/'+voltages_subfolder]:
    # for subfolder_path in [exp_folder+'/'+voltages_subfolder]:
        if not os.path.exists(exp_folder+'/'+subfolder_path):
            os.mkdir(subfolder_path)
            print(f"Subfolder {subfolder_path} created successfully.")
        else:
            print(f"Subfolder {subfolder_path} already exists.")

    analog_channels = []
    saleae_channels = dict_parameters['saleae_channels']
    if saleae_channels == 'Channel 0-1-2-3':
        analog_channels=[0, 1, 2, 3]
    if saleae_channels == 'Channel 4-5-6-7':
        analog_channels=[4, 5, 6, 7]

    saleae_buffer_size = gb_string_to_mb(dict_parameters['saleae_buffer_size'])
    saleae_sampling_rate = int(dict_parameters['saleae_sampling_rate'])
    analog_voltages_path = os.path.join(
        os.getcwd(), master_folder_path+'/'+voltages_analog_subfolder)


    logic_capture = LogicCapture(duration_seconds=total_seconds)

    try:
        saleae_buffer_size
    except NameError:
        raise AssertionError("Choose a Saleae Buffer Size")

    try:
        saleae_sampling_rate
    except NameError:
        raise AssertionError("Choose a Saleae Sampling Rate")

    try:
        analog_channels 
    except NameError:
        raise AssertionError("Choose a Saleae Channel")

    print("All Selected")
    logic_capture.start_capture(
        analog_voltages_path, saleae_buffer_size, saleae_sampling_rate, analog_channels)
    

class LogicCapture:
    def __init__(self, duration_seconds=5.0):
        self.duration_seconds = duration_seconds

    def add_offset(self, filename, offset):
        print("add offset")

    def volt_to_mbar(self, sensor, volt_signal, volt_source):
        cdict = {'25kPa': 0.018, '7kPa': 0.057, '2kPa': 0.2}
        pressure = (volt_signal / volt_source - 0.5) / cdict[sensor] * 10
        return pressure

    # Function to process the CSV file and create a new CSV with pressures
    def process_csv(self, input_file, output_file):
        os.makedirs(output_file)
        try:
            with open(input_file, 'r', newline='') as input_file:
                with open(output_file, 'w', newline='') as output_file:
                    reader = csv.reader(input_file)
                    writer = csv.writer(output_file)

                    # Example: Copying the content from the input file to the output file
                    for row in reader:
                        writer.writerow(row)

                    # You can add your data processing logic here if needed
                    # For example, manipulating the data or performing calculations.

            print("CSV processing complete. Output file created successfully.")

        except FileNotFoundError:
            print("Error: Input file not found.")
        except Exception as e:
            print("An error occurred during CSV processing:", e)

        # with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        #     reader = csv.DictReader(infile)
        #     fieldnames = ['s', '25kPa', '2kPa', '7kPa', 'V_source']  # Define the fieldnames for the output CSV
        #     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        #     writer.writeheader()

        #     for row in reader:
        #         new_row = {
        #             's': row['Time [s]'],
        #             'V_source': row['Channel 7'],
        #             '25kPa': self.volt_to_mbar(float(row['Channel 4']), 5.0, "25kPa"),  # Replace 5.0 with the actual voltage source value
        #             # '2kPa': volt_to_mbar(float(row['Channel 5']), 5.0, "2kPa"),
        #             # '7kPa': volt_to_mbar(float(row['Channel 6']), 5.0, "7kPa"),
        #         }

        #         writer.writerow(new_row)

    def change_file_permission(self, file_path, permissions='Everyone:(R,W)'):
        try:
            # Use icacls command to change permissions
            subprocess.run(
                ['icacls', file_path, '/grant', permissions], check=True)
            print(f"Permissions changed for {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to change permissions for {file_path}")
            print(e)

    def start_capture(self, output_dir, saleae_buffer_size, saleae_sampling_rate, analog_channels):
        with automation.Manager.connect(port=10430) as manager:
            device_configuration = automation.LogicDeviceConfiguration(
                enabled_analog_channels=analog_channels,
                analog_sample_rate=saleae_sampling_rate
                # sample rates <= 31250 are currently unsupported from the automation API
            )

            capture_configuration = automation.CaptureConfiguration(
                capture_mode=automation.TimedCaptureMode(
                    self.duration_seconds),
                buffer_size_megabytes=saleae_buffer_size,
            )

            with manager.start_capture(
                    device_id='624C439C76D52E8B',
                    device_configuration=device_configuration,
                    capture_configuration=capture_configuration) as capture:

                print(f"Starting Capture {self.duration_seconds} seconds")
                capture.wait()

                os.makedirs(output_dir)

                capture.export_raw_data_csv(
                    directory=output_dir, analog_channels=analog_channels, analog_downsample_ratio=10000
                )
                # self.change_file_permission(output_dir)
                print("Finished Capture")

                # Make a file system that copies this raw data and analyzes it to something different.

                # capture_filepath = os.path.join(
                #     output_dir, 'example_capture.sal')
                # capture.save_capture(filepath=capture_filepath)


if __name__ == "__main__":
    print("MultiScripting Saleae")
    param_dict = json.loads(sys.argv[1])
    process_saleae(param_dict)
