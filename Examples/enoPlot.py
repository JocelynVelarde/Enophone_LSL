import time
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter
import matplotlib.pyplot as plt

# Function to update the real-time plot
def update_real_time_plot(data, lines):
    for i, line in enumerate(lines):
        line.set_ydata(data[:, i])
    plt.pause(0.01)

def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    # agregar mac address si aparece error
    board = BoardShim(BoardIds.ENOPHONE_BOARD.value, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start streaming in the main thread')
    
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.ENOPHONE_BOARD.value)
    
    plt.ion()  # Enable interactive mode for Matplotlib
    plt.figure(figsize=(10, 6))
    
    num_samples = 200  # Number of samples to display at a time
    
    # Initialize empty lines for each EEG channel
    lines = [plt.plot([], label=f'Channel {i}')[0] for i in range(len(eeg_channels))]
    
    plt.legend(loc='upper right')
    plt.title('Real-time EEG Signal Plot')
    
    while True:
        data = board.get_current_board_data(num_samples)
        
        if data.shape[1] != len(eeg_channels):
            continue  # Skip if data doesn't match the expected channel count
        
        # Update the real-time plot
        update_real_time_plot(data, lines)
    
        board.stop_stream()
        board.release_session()

if __name__ == "__main__":
    main()
