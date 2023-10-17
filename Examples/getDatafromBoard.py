import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets


def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.ENOPHONE_BOARD, params)

    board.prepare_session()
    board.start_stream ()
    time.sleep(10)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    print(data)


if __name__ == "__main__":
    main()