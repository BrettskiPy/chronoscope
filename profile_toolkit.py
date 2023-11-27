import cProfile
import pstats
import os
import datetime


def func_profile(
    output_dir=".",
    filename=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
    sorter="cumulative",
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
                ps = pstats.Stats(pr, stream=f).sort_stats(sorter)
                ps.print_stats()

            return result

        return wrapper

    return decorator


# Test Function
@func_profile(output_dir="profiles", sorter="cumulative")
def foo():
    for _ in range(100):
        len('foo')

foo()