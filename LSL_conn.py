import time
import brainflow
from brainflow.board_shim import BrainFlowInputParams, BoardShim

# Initialize Enophone EEG board parameters
enophone_params = BrainFlowInputParams()
enophone_params.ip_port = 12345  # Replace with the correct IP and port
enophone_params.ip_protocol = brainflow.ip_protocol_type_t.UDP

# Initialize Enophone EEG board
board = BoardShim(board_id=brainflow.board_id_t.ENOPHONE, input_params=enophone_params)
board.prepare_session()
board.start_stream()

# Create an LSL outlet to stream Enophone EEG data
from pylsl import StreamInfo, StreamOutlet

# Define stream information
stream_name = "EnophoneEEGStream"
stream_type = "EEG"
num_channels = board.get_num_channels()

# Create an LSL stream
info = StreamInfo(stream_name, stream_type, num_channels, board.get_sampling_rate(), 'float32', 'myuidw43536')

# Create an outlet
outlet = StreamOutlet(info)

print("LSL Stream has started...")

try:
    while True:
        # Read data from the Enophone EEG board
        data = board.get_current_board_data(256)  # Adjust buffer size as needed

        # Send the data to the LSL stream
        outlet.push_chunk(data)
        time.sleep(0.01)  # Adjust sleep time as needed
except KeyboardInterrupt:
    pass

# Stop and release resources
board.stop_stream()
board.release_session()
