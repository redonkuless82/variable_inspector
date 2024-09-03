## crypt1@oven:~$ cat example_variable_inspector_usage.py

from variable_inspector import figure_variable, register_renderer
import datetime

# Your existing code here...

# Example usage of the variable inspector
my_variable = [1, 2, 3, {"a": 4, "b": 5}]
figure_variable(my_variable, "my_variable")

# If you want to use a custom renderer
register_renderer(datetime.datetime, lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"))
current_time = datetime.datetime.now()
figure_variable(current_time, "current_time")




## crypt1@oven:~$ python3 example_variable_inspector_usage.py

Analysis of variable 'my_variable':
Type: list
Length: 4
First few elements: [1, 2, 3, {'a': 4, 'b': 5}]

Detailed inspection result:
my_variable (list from builtins)
  [0]:
    my_variable[0] (int from builtins)
      Value: 1
  [1]:
    my_variable[1] (int from builtins)
      Value: 2
  [2]:
    my_variable[2] (int from builtins)
      Value: 3
  [3]:
    my_variable[3] (dict from builtins)
      'a':
        my_variable[3]['a'] (int from builtins)
          Value: 4
      'b':
        my_variable[3]['b'] (int from builtins)
          Value: 5

Metadata:
{
  "timestamp": "2024-09-03T14:30:44.428085",
  "python_version": "3.12.3 (main, Jul 31 2024, 17:43:48) [GCC 13.2.0]",
  "platform": "Linux-6.8.0-41-generic-x86_64-with-glibc2.39"
}

Analysis of variable 'current_time':
Type: datetime

Detailed inspection result:
current_time (datetime from datetime)
  Value: 2024-09-03T14:30:44.430720
  Custom rendering: 2024-09-03 14:30:44

Metadata:
{
  "timestamp": "2024-09-03T14:30:44.430814",
  "python_version": "3.12.3 (main, Jul 31 2024, 17:43:48) [GCC 13.2.0]",
  "platform": "Linux-6.8.0-41-generic-x86_64-with-glibc2.39"
