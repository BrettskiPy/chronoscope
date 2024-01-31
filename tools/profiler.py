import cProfile
import datetime
import os
import pstats
import time


class InvalidSorterError(Exception):
    pass


class Profiler:
    VALID_SORTERS = [
        "calls",
        "cumulative",
        "file",
        "line",
        "module",
        "name",
        "nfl",
        "pcalls",
        "stdname",
        "time",
        "tottime",
    ]
    profile = None
    output_dir = "profiled_results"
    filename = None
    sorter = "cumulative"
    start_time = None
    end_time = None

    @classmethod
    def create_output_dir(cls):
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)

    @classmethod
    def write_profile_results(cls, profile):
        if cls.filename:
            profile_filename = f"{cls.filename}.txt"
        else:
            datetime_suffix = datetime.datetime.now().strftime("%H_%M_%S_%f")
            profile_filename = f"profile_{datetime_suffix}.txt"

        full_path = os.path.join(cls.output_dir, profile_filename)
        with open(full_path, "w") as f:
            ps = pstats.Stats(profile, stream=f).sort_stats(cls.sorter)
            ps.print_stats()

    @classmethod
    def start_profiling(cls, output_dir=None, filename=None, sorter=None):
        if sorter and sorter not in cls.VALID_SORTERS:
            raise InvalidSorterError(
                f"Invalid sorter: '{sorter}'. Valid sorters are: {', '.join(cls.VALID_SORTERS)}"
            )
        cls.output_dir = output_dir or cls.output_dir
        cls.filename = filename
        cls.sorter = sorter or cls.sorter
        cls.create_output_dir()
        cls.profile = cProfile.Profile()
        cls.profile.enable()

    @classmethod
    def stop_profiling(cls):
        if cls.profile is not None:
            cls.profile.disable()
            cls.write_profile_results(cls.profile)
            cls.profile = None
        else:
            print("No active profiling session found.")

    @classmethod
    def profile_function(
        cls, output_dir="profiled_results", filename=None, sorter="cumulative"
    ):
        def decorator(func):
            profiler_instance = cls(output_dir, filename, sorter)
            return profiler_instance(func)

        return decorator

    @classmethod
    def start_timer(cls):
        """Start the timer for measuring execution time."""
        cls.start_time = time.time()

    @classmethod
    def stop_timer(cls):
        """Stop the timer and print the elapsed time."""
        cls.end_time = time.time()
        elapsed_time = cls.end_time - cls.start_time
        print(f"Elapsed time: {elapsed_time:.10f} seconds")

    def __init__(
        self, output_dir="profiled_results", filename=None, sorter="cumulative"
    ):
        self.output_dir = output_dir
        self.filename = filename
        self.sorter = sorter

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            Profiler.start_profiling(self.output_dir, self.filename, self.sorter)
            result = func(*args, **kwargs)
            Profiler.stop_profiling()
            return result

        return wrapper