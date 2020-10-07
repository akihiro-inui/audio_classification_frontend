import pyaudio
import argparse


def get_available_mics() -> dict:
    """
    Retrieve available microphones
    :return: Available microphones as dictionary {device_index: device name}
    """
    p = pyaudio.PyAudio()
    mics = {}
    for device_index in range(0, p.get_host_api_info_by_index(0).get('deviceCount')):
        if (p.get_device_info_by_host_api_device_index(0, device_index).get('maxInputChannels')) > 0:
            mics[device_index] = p.get_device_info_by_host_api_device_index(0, device_index).get('name')
    return mics


def select_mic():
    """
    Present available microphones, select microphone from console
    :return: Selected microphone index
    """
    # Extract available microphones
    available_devices = get_available_mics()
    for device_index, device_name in available_devices.items():
        print(f"Device Index: {device_index}, Device Name: {device_name}")

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mic", help="Select microphone")
    args = parser.parse_args()

    try:
        if args.mic:
            selected_device_index = int(args.mic)
            print(f"User selected mic: {selected_device_index}")
        else:
            selected_device_index = int(input(f"Select device index: "))
            print(f"Selected microphone: {available_devices[selected_device_index]}")
            return selected_device_index
    except KeyError:
        print("This is not valid device")
        exit()
    except Exception as err:
        print(f"Error while selecting microphone: {err}")
        exit()


if __name__ == "__main__":
    print(select_mic())
