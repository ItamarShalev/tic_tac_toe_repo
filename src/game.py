from src.data.board import Board
from src.data.exceptions import InvalidTurn
from src.data.piece import Piece
from src.data.state import State


class Game:

    DEFAULT_PLAYER = 'X'

    def __init__(
            self,
            board: list[list[str]] | None = None,
            lines: int | None = None,
            columns: int | None = None,
            victory_sequence: int | None = None,
            current_player: str | None = None,
    ):
        self._board = Board(board, lines, columns, victory_sequence)
        self._current_player = Piece.from_str(current_player or Game.DEFAULT_PLAYER)
        player = self._board.player_must_to_start()
        if player and player is not self._current_player:
            raise InvalidTurn(f"The player must to start is: {player}")

    def play(self, index: int):
        self._board[index] = self._current_player
        self._current_player = Piece.X if self._current_player is Piece.O else Piece.O

    @property
    def current_player(self) -> Piece:
        return self._current_player

    def game_over(self) -> bool:
        return self.state.game_over()

    @property
    def state(self) -> State:
        if winner := self._board.winner:
            return State.O_WIN if winner is Piece.O else State.X_WIN
        if self._board.is_full():
            return State.DRAW
        return State.O_TURN if self._current_player is Piece.O else State.X_TURN

    def board(self) -> Board:
        return self._board.copy()
