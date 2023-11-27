import cProfile
import pstats
import os
import datetime
import enum


class SortKey(enum.Enum):
    CALLS = "calls"
    CUMULATIVE = "cumulative"
    FILENAME = "filename"
    LINE = "line"
    MODULE = "module"
    NAME = "name"
    NFL = "nfl"
    PCALLS = "pcalls"
    STDNAME = "stdname"
    TIME = "time"


def func_profile(
    output_dir=".",
    filename=datetime.datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S", sort_by=SortKey.CUMULATIVE
    ),
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            profile_filename = f"{func.__name__}_profile_{filename}.txt"
            full_path = os.path.join(output_dir, profile_filename)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            pr = cProfile.Profile()
            
            # Start profiling
            pr.enable()
            # Function to profile
            result = func(*args, **kwargs)
            # Stop profiling
            pr.disable()

            with open(full_path, "w") as f:
                ps = pstats.Stats(pr, stream=f).sort_stats("cumulative")
                ps.print_stats()

            return result
        return wrapper
    return decorator
