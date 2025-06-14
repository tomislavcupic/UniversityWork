# connect4_mpi.py
from collections import defaultdict
from mpi4py import MPI
import numpy as np
import time

ROWS = 6
COLS = 7
PLAYER = 1
AI = 2
AGGLO_DEPTH = 2
MAX_DEPTH = 7

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def create_board():
   return np.zeros((ROWS, COLS), dtype=int)

def is_valid_location(board, col):
   return board[0][col] == 0

def get_next_open_row(board, col):
   for r in range(ROWS-1, -1, -1):
      if board[r][col] == 0:
         return r

def drop_piece(board, row, col, piece):
   board[row][col] = piece

def print_board(board):
    print("\n  0 1 2 3 4 5 6")
    print(" +-------------+")
    for r in range(ROWS):
        print(" |", end="")
        for c in range(COLS):
            cell = board[r][c]
            if cell == PLAYER:
                print("X", end=" ")
            elif cell == AI:
                print("O", end=" ")
            else:
                print(".", end=" ")
        print("|")
    print(" +-------------+\n")

def is_winning_move(board, row, col, piece):
    count = 0
    for c in range(max(0, col - 3), min(COLS, col + 4)):
        count = count + 1 if board[row][c] == piece else 0
        if count >= 4:
            return True
        if board[row][c] != piece:
            count = 0

    count = 0
    for r in range(max(0, row - 3), min(ROWS, row + 4)):
        count = count + 1 if board[r][col] == piece else 0
        if count >= 4:
            return True
        if board[r][col] != piece:
            count = 0

    count = 0
    for i in range(-3, 4):
        r, c = row - i, col + i
        if 0 <= r < ROWS and 0 <= c < COLS:
            count = count + 1 if board[r][c] == piece else 0
            if count >= 4:
                return True
        if not (0 <= r < ROWS and 0 <= c < COLS) or board[r][c] != piece:
            count = 0

    count = 0
    for i in range(-3, 4):
        r, c = row + i, col + i
        if 0 <= r < ROWS and 0 <= c < COLS:
            count = count + 1 if board[r][c] == piece else 0
            if count >= 4:
                return True
        if not (0 <= r < ROWS and 0 <= c < COLS) or board[r][c] != piece:
            count = 0

    return False

def get_valid_locations(board):
   return [c for c in range(COLS) if is_valid_location(board, c)]

def generate_tasks(board, depth, piece):
    tasks = []
    valid_cols = get_valid_locations(board)

    winning_moves = []
    for col in valid_cols:
        temp_board = board.copy()
        row = get_next_open_row(temp_board, col)
        drop_piece(temp_board, row, col, AI)
        if is_winning_move(temp_board, row, col, AI):
            winning_moves.append([col])

    if winning_moves:
        return winning_moves

    def recurse(b, d, moves, last_row=None, last_col=None, last_piece=None):
        if last_row is not None and last_col is not None:
            if is_winning_move(b, last_row, last_col, last_piece):
                if last_piece == AI:
                    tasks.append(moves)
                return

        if d == 0:
            tasks.append(moves)
            return

        valid_cols = get_valid_locations(b)
        if d == depth:
            danger_cols = []
            for col in valid_cols:
                r = get_next_open_row(b, col)
                temp_board = b.copy()
                drop_piece(temp_board, r, col, PLAYER)
                if is_winning_move(temp_board, r, col, PLAYER):
                    danger_cols.append(col)

            if danger_cols:
                valid_cols = danger_cols

        for col in valid_cols:
            b_copy = b.copy()
            row = get_next_open_row(b_copy, col)
            curr_piece = piece if d % 2 == depth % 2 else (AI if piece == PLAYER else PLAYER)
            drop_piece(b_copy, row, col, curr_piece)
            recurse(b_copy, d - 1, moves + [col], last_row=row, last_col=col, last_piece=curr_piece)

    recurse(board, depth, [])
    #print(f"Generirani taskovi: {tasks} poteza", flush=True)
    return tasks

def evaluate_agglomerated_path(moves, board, final_score):
    b_copy = board.copy()
    last_score = final_score

    for i in reversed(range(len(moves))):
        col = moves[i]
        if not is_valid_location(b_copy, col):
            last_score = 0
            continue

        row = get_next_open_row(b_copy, col)
        piece = AI if i % 2 == 0 else PLAYER
        drop_piece(b_copy, row, col, piece)

        if is_winning_move(b_copy, row, col, piece):
            last_score = 1 if piece == AI else -1
        else:
            if piece == AI:
                if last_score == 1:
                    last_score = 1
                elif last_score == -1:
                    last_score = -1 if all(s == -1 for s in [last_score]) else 0
                else:
                    last_score = last_score
            else:
                if last_score == -1:
                    last_score = -1
                elif last_score == 1:
                    last_score = 1 if all(s == 1 for s in [last_score]) else 0
                else:
                    last_score = last_score

    return last_score

def minimax(board, depth, maximizing_player, last_move_row=None, last_move_col=None, last_piece=None, alpha=float('-inf'), beta=float('inf')):
    if last_move_row is not None and last_move_col is not None:
        if is_winning_move(board, last_move_row, last_move_col, last_piece):
            return 1 if last_piece == AI else -1

    valid_moves = get_valid_locations(board)
    if depth == 0 or len(valid_moves) == 0:
        return 0

    values = []
    for col in valid_moves:
        b_copy = board.copy()
        row = get_next_open_row(b_copy, col)
        piece = AI if maximizing_player else PLAYER
        drop_piece(b_copy, row, col, piece)
        score = minimax(
            b_copy,
            depth - 1,
            not maximizing_player,
            last_move_row=row,
            last_move_col=col,
            last_piece=piece,
            alpha=alpha,
            beta=beta
        )
        values.append(score)

        if maximizing_player and score == 1:
            return 1
        if not maximizing_player and score == -1:
            return -1

        # if maximizing_player:
        #     alpha = max(alpha, score)
        # else:
        #     beta = min(beta, score)
        # if alpha >= beta:
        #     break

    if all(v == 1 for v in values):
        return 1
    if all(v == -1 for v in values):
        return -1

    return sum(values) / len(values) if values else 0

if rank == 0:
   board = create_board()
   game_over = False

   while not game_over:
      print_board(board)
      while True:
         try:
            col = int(input("Unesi potez (0-6): "))
            if col in [0, 1, 2, 3, 4, 5, 6]:
               break
            else:
               print("netocan unos. unesi broj izmedu 0 i 6.")
         except ValueError:
            print("netocan unos. unesi broj izmedu 0 i 6.")
      if not is_valid_location(board, col):
         print("Kolona nije dostupna. Pokusaj ponovno.")
         continue
      row = get_next_open_row(board, col)
      drop_piece(board, row, col, PLAYER)

      if is_winning_move(board, row, col, PLAYER):
         print_board(board)
         print("Ti si pobijedio!")
         break

      start = time.time()
      tasks = generate_tasks(board, AGGLO_DEPTH, AI)

      if size == 1:
         all_results = []
         for moves in tasks:
            b_copy = board.copy()
            valid = True
            last_row = None
            last_col = None
            last_piece = None
            for i, col in enumerate(moves):
               if is_valid_location(b_copy, col):
                  row = get_next_open_row(b_copy, col)
                  piece = AI if i % 2 == 0 else PLAYER
                  drop_piece(b_copy, row, col, piece)
                  last_row = row
                  last_col = col
                  last_piece = piece
               else:
                  valid = False
                  break
            if valid:
               if is_winning_move(b_copy, last_row, last_col, last_piece):
                  score = 1 if last_piece == AI else -1
               else:
                  score = minimax(
                     b_copy,
                     MAX_DEPTH - len(moves),
                     False,
                     last_move_row=last_row,
                     last_move_col=last_col,
                     last_piece=last_piece
                  )
               evaluated_score = evaluate_agglomerated_path(moves, board, score)
               all_results.append((moves[0], evaluated_score))

      else:
         n_workers = size - 1
         chunk_size = (len(tasks) + n_workers - 1) // n_workers
         chunks = [tasks[i*chunk_size:(i+1)*chunk_size] for i in range(n_workers)]
         for i, task_chunk in enumerate(chunks):
            comm.send((board, list(task_chunk)), dest=i+1)

         all_results = []
         for _ in range(1, size):
            result = comm.recv(source=MPI.ANY_SOURCE)
            all_results.extend(result)

      end = time.time()
      print(f"Racunalo je razmislilo {len(all_results)} poteza u {end - start:.2f} sekundi.")
      col_scores = defaultdict(list)
      for col, score in all_results:
         col_scores[col].append(score)
      col_min_scores = {col: min(scores) for col, scores in col_scores.items()}
      best_move = max(col_min_scores.items(), key=lambda x: x[1])[0]
      row = get_next_open_row(board, best_move)
      drop_piece(board, row, best_move, AI)

      if is_winning_move(board, row, best_move, AI):
         print_board(board)
         print("Racunalo je pobijedilo!")
         break

else:
   while True:
      data = comm.recv(source=0)
      if data is None:
         break
      board, tasks = data
      result = []
      for moves in tasks:
         b_copy = board.copy()
         valid = True
         last_row = None
         last_col = None
         last_piece = None
         for i, col in enumerate(moves):
            if is_valid_location(b_copy, col):
               row = get_next_open_row(b_copy, col)
               piece = AI if i % 2 == 0 else PLAYER
               drop_piece(b_copy, row, col, piece)
               last_row = row
               last_col = col
               last_piece = piece
            else:
               valid = False
               break
         if valid:
            if is_winning_move(b_copy, last_row, last_col, last_piece):
               score = 1 if last_piece == AI else -1
            else:
               score = minimax(
                  b_copy,
                  MAX_DEPTH - AGGLO_DEPTH,
                  False,
                  last_move_row=last_row,
                  last_move_col=last_col,
                  last_piece=last_piece
               )
            evaluated_score = evaluate_agglomerated_path(moves, board, score)
            result.append((moves[0], evaluated_score))
      comm.send(result, dest=0)