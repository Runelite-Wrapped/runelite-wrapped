# loads in sqlite db and lists the tables

import json
import sqlite3
from testmodule import testfunction


def main():
    testfunction()

    conn = sqlite3.connect("/stats.db")

    c = conn.cursor()

    c.execute(
        """
    SELECT JSON_EXTRACT(JSON(data), '$.timestamp', '$.data.energy') FROM game_tick
    """
    )

    result = [json.loads(x[0]) for x in c.fetchall()]

    timestamps = [int(x[0]) for x in result]
    run_energy = [int(x[1]) / 100 for x in result]

    # TODO: find a way to pass data between without having
    #   to (de)serialize
    return json.dumps(
        {
            "timestamps": timestamps,
            "runEnergy": run_energy,
        }
    )


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
