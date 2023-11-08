"""This module contains utility functions for the project."""

# standard library
from datetime import datetime
from functools import wraps
import json
import os
from pathlib import Path
import pickle
import random
import sys
from typing import Literal

# Python package index
import numpy as np

# custom local modules
## note to self: utils is at the very bottom of the hierarchy and hence should
## not import any other custom modules in order to avoid circular import errors


def parse_arguments():
    arguments = {}

    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            key_value = arg.split("=")
            key = key_value[0][2:]
            value = key_value[1] if len(key_value) > 1 else True
            arguments[key] = value

    return arguments


# Remove the script name from the list of arguments
arguments = parse_arguments()


if "no-debug" in arguments:
    debug = False
else:
    debug = True

ROOT_PATH = Path(__file__).parent.parent


def read_json(path):
    """Reads a json file and returns a dictionary."""
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def load_json(path):
    """alias for read_json"""
    contents = read_json(path)

    return contents


def dump_json(obj, path):
    """dumps a json file with a path as input"""

    json_str = (
        json.dumps(obj, indent=2) + "\n"
    )  # best practice: new line at the end of the file

    with open(path, "w", encoding="utf8") as file:
        file.write(json_str)


def is_probability(num):
    if 0 <= num <= 1:
        return True
    else:
        return False


def timestamp(
    resolution: Literal[
        "minutes", "seconds", "milliseconds", "microseconds"
    ] = "minutes"
):
    now = datetime.now()
    if resolution == "minutes":
        timestamp_unformatted = "%Y-%m-%d_%H-%M"
    elif resolution == "seconds":
        timestamp_unformatted = "%Y-%m-%d_%H-%M-%S"
    elif resolution == "milliseconds":
        milliseconds = round(now.microsecond / 1_000)
        timestamp_unformatted = f"%Y-%m-%d_%H-%M-%S-{milliseconds}"
    elif resolution == "microseconds":
        timestamp_unformatted = "%Y-%m-%d_%H-%M-%S-%f"
    else:
        raise ValueError(
            f"You passed an unknown option as the 'resolution'\
                         argument: {resolution}"
        )

    timestamp = now.strftime(timestamp_unformatted)
    return timestamp


def split_dataframe(df, k: int, randomize=False) -> tuple:
    """split a pandas dataframe into several parts

    If `len(df) % k` unequal 0 (i.e. if given this k the dataframe cannot be
    split into equal-sized parts), the last split will be larger than the rest.

    Parameters
    ----------
    df : pandas dataframe
        the dataframe to be split
    k : int
        number of splits
    randomize : bool
        whether to shuffle the dataframe before splitting

    Returns
    -------
    splits : tuple
        tuple containing each of the split parts

    """
    if randomize:
        index = list(df.index)
        random.shuffle(index)
        df = df.loc[index, :]

    splits = []
    n_split = len(df) // k
    for i in range(k):
        if i == k - 1:
            split = df.iloc[i * n_split :, :]
        else:
            split = df.iloc[i * n_split : (i + 1) * n_split, :]
        splits.append(split)

    return splits


def ensure_directory_exists(path):
    if not path.exists():
        os.mkdir(path)


# %% decorators
def log_start_and_end(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        dashes = 5 * "-"
        print(f"{dashes} START of {function.__name__} {dashes}")
        output = function(*args, **kwargs)
        print(f"{dashes} END of {function.__name__} {dashes}")

        return output

    return wrapper


def time_function(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        t0 = datetime.now()

        output = function(*args, **kwargs)

        t1 = datetime.now()
        delta = str(t1 - t0)
        hours_minutes_seconds = delta.split(".")[0]
        hours_minutes = hours_minutes_seconds[:-3]
        print(f"The function took {hours_minutes} hours to compute")

        return output

    return wrapper


def save_seed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        seed = np.random.get_state()
        path = ROOT_PATH / f"results/{function.__name__}/seeds"
        ensure_directory_exists(path)
        with open(path / f"{kwargs['partial_fname']}_seed.pkl", "wb") as file:
            pickle.dump(seed, file)
        output = function(*args, **kwargs)
        return output

    return wrapper


if __name__ == "__main__":
    print("debug:", debug)
