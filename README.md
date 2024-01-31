# Chronoscope: A Simple Python Profiling Toolkit
![watch_scope](https://github.com/BrettskiPy/chrono-scope/assets/30988215/0823b05f-04c3-4421-923e-697e96350267)

Chronoscope is a Python toolkit designed to measure execution time, sort profiling results by different criteria (e.g., cumulative time, call count), and save the results in a text file for further analysis. This tool is useful for developers who need to optimize Python code by identifying performance bottlenecks.

## Requirements
- Python environment (Python 3.x recommended)
- Access to standard Python libraries such as `cProfile`, `pstats`, `os`, `datetime`, and `time`

## Installation
No specific installation is required as the tool utilizes standard Python libraries. Ensure that your Python environment is set up correctly.

## Usage Examples

### Basic Usage
Print the time taken to run a block of code:

```python
def foo():
    foo_list = [1, 2, 3]
    for _ in range(100000):
        len(foo_list)

Profiler.start_timer()
foo()
Profiler.stop_timer()
```

### Profiling with Decorators
Use the `@Profiler.profile_function()` decorator to profile an entire function:

```python
@Profiler.profile_function()
def bar():
    bar_list = [1, 2, 3]
    for _ in range(100000):
        len(bar_list)

bar()
```

### Manual Profiling Control
For manual control over the profiling start and stop:

```python
def baz():
    Profiler.start_profiling()
    baz_list = [1, 2, 3]
    for _ in range(100000):
        len(baz_list)
    Profiler.stop_profiling()

baz()
```
