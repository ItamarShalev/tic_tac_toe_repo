from pathlib import Path

import yaml
import pytest

from src.data import exceptions
from src.game import Game


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
    print(game)
