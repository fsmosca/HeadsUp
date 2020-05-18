"""
headsup.py

Needed:
    Python 3.7 and up

Requirements
    Python-chess 0.31.1
"""


import sys
import configparser
import logging
from pathlib import Path

import chess
import chess.engine


APP_NAME = 'HeadsUp'
APP_VER = '0.1'
APP_AUTHOR = 'Ferdy'
STARTPOS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
MATE_SCORE = 32000


def get_piece_value(board):
    epd = board.epd()
    p = epd.split()[0]

    wp = p.count('P')
    wn = p.count('N')
    wb = p.count('B')
    wr = p.count('R')
    wq = p.count('Q')

    bp = p.count('p')
    bn = p.count('n')
    bb = p.count('b')
    br = p.count('r')
    bq = p.count('q')

    return 3*(wn+wb+bn+bb) + 5*(wr+br) + 9*(wq+bq), wp+bp


def get_move_list(pos_line):
    a = pos_line.split()
    move_index = a.index('moves')
    moves = a[move_index+1:]
    moves = ' '.join(moves)
    moves = moves.strip()

    return moves.split()


def get_fen(pos_line):
    fen = pos_line.rstrip().split()
    fen = fen[2:8]
    fen = ' '.join(fen)
    fen = fen.strip()

    return fen


def get_movetime(line):
    return [int(line.strip().split()[2].strip())]


def get_wtime_btime(line):
    """

    :param line: e.g. 'go wtime 1000 btime 1000 winc 100 binc 100'
    :return: a list of time values
    """
    tc_info = line.strip()
    logging.info(tc_info)

    is_reverse = True if tc_info.startswith('go btime ') else False

    if is_reverse:
        btime = int(tc_info.split()[2].strip())
        wtime = int(tc_info.split()[4].strip())

        # Todo: to be checked if binc is first and winc is second
        binc = int(tc_info.split()[6].strip())
        winc = int(tc_info.split()[8].strip())
    else:
        wtime = int(tc_info.split()[2].strip())
        btime = int(tc_info.split()[4].strip())
        winc = int(tc_info.split()[6].strip())
        binc = int(tc_info.split()[8].strip())

    logging.info(f'wtime: {wtime}, btime: {btime}, winc: {winc}, binc: {binc}')

    return [wtime, btime, winc, binc]


def search(engine, eng_label, board, tc_info):
    """
    Returns best move from a given board position by engine engine.

    Supported time control is time per move and Fischer.

    :param engine: the engine used to search for best move
    :param eng_label: engine name
    :param board: the position to evaluate
    :param tc_info: a list of [movetime] or [wtime, btime, winc, binc]
    :return: bm
    """
    # Divide time by 1000 because python-chess is using time in seconds.
    if len(tc_info) > 1:
        limit = chess.engine.Limit(white_clock=tc_info[0]/1000,
                                   black_clock=tc_info[1]/1000,
                                   white_inc=tc_info[2]/1000,
                                   black_inc=tc_info[3]/1000)
    else:
        limit = chess.engine.Limit(time=tc_info[0]/1000)

    result = engine.play(board, limit, info=chess.engine.Info.ALL)
    bm = result.move

    try:
        if result.info['score'].is_mate():
            score = result.info['score'].relative.score(mate_score=MATE_SCORE)
        else:
            score = result.info['score'].relative.score()
    except KeyError as err:
        score = 0
        logging.info(err)

    try:
        depth = result.info['depth']
    except KeyError as err:
        depth = 1
        logging.info(err)

    try:
        tim = int(result.info['time'] * 1000)
    except KeyError as err:
        tim = 1
        logging.info(err)

    try:
        nps = result.info['nps']
    except KeyError as err:
        nps = 1
        logging.info(err)

    try:
        uci_pv = ' '.join([str(m) for m in result.info['pv']])
    except KeyError as err:
        uci_pv = ''
        logging.info(err)

    print(f'info string search info from {eng_label}')
    print(f'info depth {depth} score cp {score} time {tim} '
          f'nps {nps} pv {uci_pv}')

    return bm


def main():
    cfg_file = 'headsup.cfg'
    board = chess.Board()

    piece_value_switch = 62  # Use engine2
    move_number_switch = 0  # Use engine2

    # Check headsup.cfg in the same dir with headsup.py or headsup.exe
    config_file_path = Path(cfg_file)
    if not config_file_path.is_file():
        print(f'{cfg_file} file is required to run {APP_NAME}! Exiting ...')
        sys.exit(1)

    is_logging = False
    engine1_file, engine2_file = None, None

    # Read config file for the engine path/filenames and headsup option
    parser = configparser.ConfigParser()
    parser.read('headsup.cfg')
    for section_name in parser.sections():
        for name, value in parser.items(section_name):
            if section_name.lower() == 'engine1':
                if name == 'enginefile':
                    engine1_file = value
            elif section_name.lower() == 'engine2':
                if name == 'enginefile':
                    engine2_file = value
            elif section_name.lower() == 'headsup option':
                if name.lower() == 'piece_value_switch':
                    piece_value_switch = int(value)
                elif name.lower() == 'move_number_switch':
                    move_number_switch = int(value)
                elif name.lower() == 'log':
                    is_logging = True if value.lower() == 'true' else False

    if is_logging:
        logging.basicConfig(
            filename='log_headsup.txt', filemode='w', level=logging.DEBUG,
            format='%(asctime)s :: %(levelname)s :: %(message)s')

    # Check engine files based on headsup.cfg
    if engine1_file is None:
        logging.info('engine1 is missing.')
        sys.exit(1)
    if engine2_file is None:
        logging.info('engine2 is missing.')
        sys.exit(1)

    engine1 = chess.engine.SimpleEngine.popen_uci(engine1_file)
    engine2 = chess.engine.SimpleEngine.popen_uci(engine2_file)

    engine1_id_name = engine1.id['name']
    engine2_id_name = engine2.id['name']

    # Get engine option names
    opt_name_engine_1 = [opt.lower() for opt in engine1.options]
    opt_name_engine_2 = [opt.lower() for opt in engine2.options]

    # Read config file to set engine options
    parser = configparser.ConfigParser()
    parser.read('headsup.cfg')
    for section_name in parser.sections():
        for name, value in parser.items(section_name):
            if section_name.lower() == 'engine1':
                if name.lower() in opt_name_engine_1:
                    engine1.configure({name: value})
            elif section_name.lower() == 'engine2':
                if name.lower() in opt_name_engine_2:
                    engine2.configure({name: value})

    while True:
        command = input('')
        command = command.strip()

        if command == 'uci':
            print(f'id name {APP_NAME} {APP_VER}')
            print(f'id author {APP_AUTHOR}')
            print(f'info string engine1 is {engine1_id_name}')
            print(f'info string engine2 is {engine2_id_name}')
            print('uciok')

        elif command == 'isready':
            print('readyok')

        elif command == 'ucinewgame':
            print(f'info string received {command}')

        elif command == 'stop':
            print(f'info string received {command}')

        elif command == 'quit':
            logging.info(f'info string quit {engine1_id_name}')
            engine1.quit()

            logging.info(f'info string quit {engine2_id_name}')
            engine2.quit()

            if is_logging:
                logging.shutdown()

            return

        elif 'position ' in command:
            if 'startpos' in command:
                board = chess.Board()

            elif 'fen ' in command:
                fen = get_fen(command)
                board = chess.Board(fen)

            if 'moves' in command:
                move_list = get_move_list(command)
                for m in move_list:
                    board.push(chess.Move.from_uci(m))

        elif 'go movetime' in command:
            tc_info = get_movetime(command)

            piece_value, _ = get_piece_value(board)
            fmvn = board.fullmove_number
            logging.info(f'fmvn: {fmvn}')

            if fmvn < move_number_switch and piece_value > piece_value_switch:
                bm = search(engine1, engine1_id_name, board, tc_info)
            else:
                bm = search(engine2, engine2_id_name, board, tc_info)

            print(f'bestmove {bm}')

        elif 'go wtime ' in command or 'go btime ' in command:
            tc_info = get_wtime_btime(command)

            piece_value, _ = get_piece_value(board)
            fmvn = board.fullmove_number
            logging.info(f'fmvn: {fmvn}')

            if fmvn < move_number_switch and piece_value > piece_value_switch:
                bm = search(engine1, engine1_id_name, board, tc_info)
            else:
                bm = search(engine2, engine2_id_name, board, tc_info)

            print(f'bestmove {bm}')

        else:
            print(f'info string command "{command}" is not supported')
            logging.info(f'info string command "{command}" is not supported')


if __name__ == "__main__":
    main()
