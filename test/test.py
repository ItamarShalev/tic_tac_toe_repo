from pathlib import Path

import yaml
import pytest

from src.game import Game


def all_yaml_files() -> list[Path]:
    test_dir = Path(__file__).parent
    yaml_dir = test_dir / "yaml_use_case"
    return list(yaml_dir.rglob("*.yaml"))

def load_yaml(yaml_file: Path) -> dict:
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

@pytest.mark.parametrize("yaml_file", all_yaml_files(), ids=[file.name for file in all_yaml_files()])
def test_yaml_test_case(yaml_file: Path):
    data = load_yaml(yaml_file)
    game: Game = Game(**data["game"])
    print(game)
