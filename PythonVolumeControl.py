import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

def display_volumes():
    # Set audio device en interface thingy!
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Get master volume (system-wide)
    system_volume = volume.GetMasterVolumeLevelScalar()  # Iets tussen 0 en 1 
    print(f"\nSystem-Wide Volume: {system_volume * 100:.2f}%\n")

    # Get all audio sessies
    sessions = AudioUtilities.GetAllSessions()

    print("Audio Sessions and Current Volume Levels:\n")
    for session in sessions:
        # Get the simple audio volume for the session
        simple_audio_volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        
        # Check if the session has an associated process
        if session.Process:
            process_name = session.Process.name()
            
            # Get the current volume level for the session
            current_volume = simple_audio_volume.GetMasterVolume()
            
            # process and current volume level
            print(f"Process: {process_name} | Volume Level: {current_volume * 100:.2f}%")
    print("-" * 40) 

# Loopdyloop
try:
    while True:
        display_volumes()
        time.sleep(0.5)  # Waiting Game
except KeyboardInterrupt:
    print("Exiting...")  # Dont you dare touch the button!
