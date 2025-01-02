from abc import ABC, abstractmethod
from pathlib import Path

import yaml
import pytest

from src.data import exceptions
from src.data.state import State
from src.game import Game


class Action(ABC):


    @abstractmethod
    def __call__(self, game: Game):
        pass


class Move(Action):

    def __init__(self, index: int, error: str = ""):
        self.index = index
        self.error = error


    def __call__(self, game: Game):
        if self.error:
            exception = getattr(exceptions, title_case(self.error))
            with pytest.raises(exception):
                game.play(self.index)
        else:
            game.play(self.index)

class CheckState(Action):

    def __init__(self, state: str):
        self.state = State.from_str(state)

    def __call__(self, game: Game):
        assert game.state is self.state


def all_yaml_files() -> list[Path]:
    test_dir = Path(__file__).parent
    yaml_dir = test_dir / "yaml_use_case"
    return list(yaml_dir.rglob("*.yaml"))

def load_yaml(yaml_file: Path) -> dict:
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def title_case(value: str) -> str:
    """
    invalid_board -> InvalidBoard
    :param value:
    :return:
    """
    return value.replace("_", " ").title().replace(" ", "")

def init_game(data: dict) -> Game | None:
    if error := data.get("game", {}).get("error", ""):
        del data["game"]["error"]
        exception = getattr(exceptions, title_case(error))
        with pytest.raises(exception):
            Game(**data["game"])
        return None
    return Game(**data.get("game", {}))


@pytest.mark.parametrize("yaml_file", all_yaml_files(), ids=[file.name for file in all_yaml_files()])
def test_yaml_test_case(yaml_file: Path):
    data = load_yaml(yaml_file)
    game: Game | None = init_game(data)
    if not game:
        return

    for action_data in data.get("actions", []):
        print(f"Action data: {action_data}")
        action_type = title_case(action_data["type"])
        del action_data["type"]
        action = globals()[action_type](**action_data)
        action(game)
