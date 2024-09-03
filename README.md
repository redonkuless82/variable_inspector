# Variable Inspector

Variable Inspector is a powerful Python module designed to provide detailed insights into variables, objects, and data structures in Python. It offers a comprehensive way to analyze and understand the content and structure of variables, making it an invaluable tool for debugging, code analysis, and learning Python.

## Features

- Inspect any Python variable or object
- Support for nested structures (lists, dictionaries, custom objects)
- Handling of circular references
- Custom renderers for specific types
- Multiple output formats (text, JSON, YAML, tree structure)
- Metadata about the inspection process
- Configurable depth limit and sampling for large collections

## Installation

Clone this repository or copy the `variable_inspector.py` file into your project directory.

```bash
git clone https://github.com/redonkuless82/variable-inspector.git
```

## Usage

Import the main functions from the module:

```python
from variable_inspector import figure_variable, register_renderer
```

### Basic Usage

```python
my_variable = [1, 2, 3, {"a": 4, "b": 5}]
figure_variable(my_variable, "my_variable")
```

### Custom Renderer

```python
import datetime

register_renderer(datetime.datetime, lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"))
current_time = datetime.datetime.now()
figure_variable(current_time, "current_time")
```

### Advanced Usage

```python
complex_structure = {
    "list": [1, 2, 3],
    "dict": {"a": 1, "b": 2},
    "nested": [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
}
figure_variable(complex_structure, "complex_structure", max_depth={"dict": 3}, output_format="tree")
```

## Use Cases

1. **Debugging**: Quickly inspect variables to understand their content and structure during debugging sessions.
2. **Code Analysis**: Analyze complex data structures or objects returned by APIs or libraries.
3. **Learning Tool**: Understand how Python represents different data types and structures internally.
4. **Documentation**: Generate detailed representations of data structures for documentation purposes.
5. **Testing**: Verify the structure and content of variables in test assertions.

## How It's Useful

1. **Comprehensive Inspection**: Provides a detailed view of variables, including type information, nested structures, and custom object attributes.
2. **Flexibility**: Supports various output formats to suit different needs (e.g., human-readable text, machine-parseable JSON).
3. **Customization**: Allows custom renderers for specific types, enabling tailored output for complex objects.
4. **Safety**: Handles circular references and large data structures gracefully, preventing crashes or hangs.
5. **Metadata**: Includes useful metadata like timestamp and Python version, aiding in troubleshooting environment-specific issues.

## What It Can Identify

- Basic types (int, float, str, bool, None)
- Collections (list, tuple, set, dict)
- Custom objects and their attributes
- Functions and their signatures
- Classes and their methods/attributes
- Modules and their contents
- Circular references
- Nested structures (up to a configurable depth)
- Large collections (with sampling)

## Troubleshooting Code

1. **Unexpected Values**: Quickly identify if variables contain the expected values or structures.
2. **Type Errors**: Understand the exact types of objects, helping diagnose type-related issues.
3. **Attribute Errors**: For custom objects, see all available attributes, helping diagnose AttributeError issues.
4. **Data Structure Issues**: Visualize complex nested structures to understand data organization.
5. **Function Debugging**: Inspect function objects to verify their signatures and attributes.
6. **Module Exploration**: Examine the contents of imported modules to understand available functions and classes.
7. **Memory Issues**: Identify unexpectedly large data structures or circular references that might cause memory problems.

## Contributing

Contributions to improve Variable Inspector are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under GPL 3.0
