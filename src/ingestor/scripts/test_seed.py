from typing import List
from pathlib import Path
import json

from requests import post

_script_dir = Path(__file__).parent.absolute()
_data_dir = _script_dir.parent / 'data'


def _load_data(filename) -> List[dict]:
    """Load file using json"""
    with open(filename) as f:
        return json.load(f)


def main():
    data = _load_data(_data_dir / "test_game_ticks.json")

    for tick_data in data:
        pass



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
