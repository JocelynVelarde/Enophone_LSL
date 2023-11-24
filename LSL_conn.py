import time
import matplotlib.pyplot as plt
from brainflow.board_shim import BrainFlowInputParams, BoardShim, BoardIds
from pylsl import StreamInfo, StreamOutlet

# Enable logging for the development board
BoardShim.enable_dev_board_logger()

# Board initialization
params = BrainFlowInputParams()
board = BoardShim(BoardIds.ENOPHONE_BOARD.value, params)
board.prepare_session()
board.start_stream()

# LSL stream configuration
stream_name = "EnophoneEEGStream"
stream_type = "EEG"
eeg_channels = BoardShim.get_eeg_channels(BoardIds.ENOPHONE_BOARD.value)
numChannels = len(eeg_channels)

info = StreamInfo(stream_name, stream_type, numChannels, 250, "float32", "enoLSL")
outlet = StreamOutlet(info)

print(f"LSL Stream has started with {numChannels} channels...")

try:
    while True:
        data = board.get_current_board_data(256)

        # Send the data to the LSL stream
        outlet.push_chunk(data)

        # Plot EEG signals
        plt.clf()  # Clear the previous plot
        for i in range(numChannels):
            plt.plot(data[i])

        plt.title('EEG Signals')
        plt.xlabel('Sample Index')
        plt.ylabel('EEG Amplitude')
        plt.pause(0.01)  # Add a short pause to allow for real-time plotting

except KeyboardInterrupt:
    print("Stopping the LSL Stream...")
    pass

finally:
    board.stop_stream()
    board.release_session()
