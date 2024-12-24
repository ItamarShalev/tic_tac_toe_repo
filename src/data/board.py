from __future__ import annotations

from src.data.exceptions import InvalidSymbolBoard, InvalidLinesSize, InvalidIndexBoard, OccupiedCell, InvalidBoard
from src.data.exceptions import GameOver
from src.data.piece import Piece


class Board:

    DEFAULT_LINES = 3
    DEFAULT_COLUMNS = 3

    def __init__(
            self,
            board: list[list[str]] | None = None,
            lines: int | None = None,
            columns: int | None = None,
            victory_sequence: int | None = None
    ):
        lines = lines or Board.DEFAULT_LINES
        columns = columns or Board.DEFAULT_COLUMNS
        board = board or [[' '] * columns for _ in range(lines)]
        self._board, self._lines, self._columns = self._init_board(board)
        max_victory_sequence = min(self._lines, self._columns)
        self._victory_sequence = victory_sequence or max_victory_sequence
        if 2 > self._victory_sequence > min(self._lines, self._columns):
            raise InvalidBoard(f"victory_sequence must be between (2, {max_victory_sequence})")
        self._winner = self._search_winner()

    @property
    def winner(self) -> Piece | None:
        return self._winner

    @staticmethod
    def _init_board(board_data: list[list[str]]) -> tuple[list[list[Piece]], int, int]:
        try:
            board = [[Piece.from_str(symbol) for symbol in row] for row in board_data]
        except KeyError as exception:
            raise InvalidSymbolBoard(f"Invalid symbol in the board: {str(exception)}") from None

        count_x_pieces = sum(piece is Piece.X for row in board for piece in row)
        count_o_pieces = sum(piece is Piece.O for row in board for piece in row)

        if abs(count_x_pieces - count_o_pieces) > 1:
            raise InvalidBoard(f"Invalid numbers of pieces: X={count_x_pieces}, O={count_o_pieces}")

        columns_sizes = list({len(line) for line in board})
        lines = len(board)
        columns = columns_sizes[0]

        if len(columns_sizes) != 1:
            raise InvalidLinesSize(f"Got different sizes: {columns_sizes}")

        return board, lines, columns

    def player_must_to_start(self) -> Piece | None:
        count_x_pieces = sum(piece is Piece.X for row in self._board for piece in row)
        count_o_pieces = sum(piece is Piece.O for row in self._board for piece in row)
        if count_o_pieces == count_x_pieces:
            return None
        return Piece.O if count_x_pieces > count_o_pieces else Piece.X

    def raw(self) -> list[list[str]]:
        return [[str(piece) for piece in row] for row in self._board]

    def copy(self) -> Board:
        return Board(self.raw(), self._lines, self._columns, self._victory_sequence)

    def __copy__(self) -> Board:
        return self.copy()

    def _search_winner(self) -> Piece | None:
        winners = set()
        for index in range(self._lines * self._columns):
            winners.add(self._winner_at(index))
        winners = winners - {None, Piece.EMPTY}
        if len(winners) > 1:
            raise InvalidBoard("There is more than one winner.")
        return winners.pop() if winners else None

    def is_full(self) -> bool:
        return all(self[index] is not Piece.EMPTY for index in range(self._lines * self._columns))

    def _winner_at(self, index: int) -> Piece | None:
        delta_functions = {
            'main_diagonal': (lambda step: (step * 1, step * 1)),
            'sub_diagonal': (lambda step: (step * 1, step * -1)),
            'vertical': (lambda step: (step * 1, 0)),
            'horizontal': (lambda step: (0, step * 1)),
        }

        row, column = self._line_column(index)

        for delta_fn in delta_functions.values():
            sequence = 1
            for direction in (1, -1):
                for i in range(max(self._lines, self._columns)):
                    step_x, step_y = delta_fn(i * direction)
                    new_row = row + step_x
                    new_column = column + step_y
                    valid_row = 0 <= new_row < self._lines
                    valid_column = 0 <= new_row < self._columns
                    valid_cell = valid_row and valid_column
                    new_index = self._columns * new_row + new_column
                    if not valid_cell or self[new_index] is not self[index]:
                        break
                    sequence += 1

            if sequence >= self._victory_sequence:
                return self[index]

        return None


    def _line_column(self, index: int) -> tuple[int, int]:
        line = index // self._columns
        column = index % self._columns
        return line, column

    def _valid_index(self, index: int) -> bool:
        return 0 <= index < self._lines * self._columns

    def __getitem__(self, index: int) -> Piece:
        if not self._valid_index(index):
            raise InvalidIndexBoard()
        line, column = self._line_column(index)
        return self._board[line][column]

    def __setitem__(self, index: int, piece: Piece | str):
        if not self._valid_index(index):
            raise InvalidIndexBoard()
        if self._winner:
            raise GameOver(f"The game is over, {self._winner} already won.")
        line, column = self._line_column(index)
        value = self._board[line][column]
        if value is not Piece.EMPTY:
            raise OccupiedCell()
        self._board[line][column] = Piece.from_str(piece)
        self._winner = self._winner_at(index)
