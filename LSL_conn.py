import time
import brainflow
from brainflow.board_shim import BrainFlowInputParams, BoardShim, BoardIds

BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
board = BoardShim(BoardIds.ENOPHONE_BOARD.value, params)
board.prepare_session()
board.start_stream()


from pylsl import StreamInfo, StreamOutlet


stream_name = "EnophoneEEGStream"
stream_type = "EEG"
eeg_channels = BoardShim.get_eeg_channels(BoardIds.ENOPHONE_BOARD.value)
numChannels = len(eeg_channels)


info = StreamInfo(stream_name, stream_type, numChannels, 250, "float32", "hi")


outlet = StreamOutlet(info)

print("LSL Stream has started...")

try:
    while True:
        data = board.get_current_board_data(256)  

        # Send the data to the LSL stream
        outlet.push_chunk(data)
        time.sleep(0.01) 
except KeyboardInterrupt:
    pass


board.stop_stream()
board.release_session()
