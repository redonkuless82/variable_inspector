# File: variable_inspector.py (Part 1)

import logging
import inspect
from typing import Any, Dict, Optional, Set, Type, Callable
from collections.abc import Iterable
import datetime
import json
import asyncio
import random
import platform
import sys
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

custom_renderers: Dict[Type, Callable] = {}

def register_renderer(type_: Type, renderer: Callable) -> None:
    custom_renderers[type_] = renderer

def get_type_info(obj: Any) -> Dict[str, str]:
    """Get detailed type information for an object."""
    obj_type = type(obj)
    type_info = {
        "type_name": obj_type.__name__,
        "module": obj_type.__module__
    }
    if callable(obj):
        try:
            signature = str(inspect.signature(obj))
            type_info["signature"] = signature
        except ValueError:
            type_info["signature"] = "Unable to determine signature"
    return type_info

def print_structure(structure: Dict[str, Any], indent: str = "") -> None:
    """Print the inspection result as plain text to console."""
    name = structure.get("name", "unnamed")
    type_info = structure.get("type_info", {})
    print(f"{indent}{name} ({type_info.get('type_name', 'unknown type')} from {type_info.get('module', 'unknown module')})")

    if "circular_reference" in structure:
        print(f"{indent}  <circular reference>")
        return
    if "max_depth_reached" in structure:
        print(f"{indent}  <max depth reached>")
        return

    if "value" in structure:
        if isinstance(structure["value"], dict):
            for k, v in structure["value"].items():
                print(f"{indent}  {k}:")
                print_structure(v, indent + "    ")
        elif isinstance(structure["value"], list):
            for i, item in enumerate(structure["value"]):
                print(f"{indent}  [{i}]:")
                print_structure(item, indent + "    ")
        else:
            print(f"{indent}  Value: {structure['value']}")

    if "module_contents" in structure:
        print(f"{indent}  Module contents:")
        for item_name, item_type in structure["module_contents"].items():
            print(f"{indent}    {item_name}: {item_type['type_name']}")

    if "class_contents" in structure:
        print(f"{indent}  Class contents:")
        for item_name, item_type in structure["class_contents"].items():
            print(f"{indent}    {item_name}: {item_type['type_name']}")

    if "signature" in structure:
        print(f"{indent}  Signature: {structure['signature']}")

    if "attributes" in structure:
        print(f"{indent}  Attributes:")
        for attr, value in structure["attributes"].items():
            print_structure(value, indent + "    ")

    if "coroutine_info" in structure:
        print(f"{indent}  Coroutine info: {structure['coroutine_info']}")

    if "custom_rendering" in structure:
        print(f"{indent}  Custom rendering: {structure['custom_rendering']}")

def print_tree_structure(structure: Dict[str, Any], indent: str = "") -> None:
    """Print the inspection result as a tree-like structure to console."""
    name = structure.get("name", "unnamed")
    type_info = structure.get("type_info", {})
    print(f"{indent}├─ {name} ({type_info.get('type_name', 'unknown type')})")

    if "circular_reference" in structure:
        print(f"{indent}│  └─ <circular reference>")
        return
    if "max_depth_reached" in structure:
        print(f"{indent}│  └─ <max depth reached>")
        return

    if "value" in structure:
        if isinstance(structure["value"], dict):
            for k, v in structure["value"].items():
                print(f"{indent}│  ├─ {k}:")
                print_tree_structure(v, indent + "│  │  ")
        elif isinstance(structure["value"], list):
            for i, item in enumerate(structure["value"]):
                print(f"{indent}│  ├─ [{i}]:")
                print_tree_structure(item, indent + "│  │  ")
        else:
            print(f"{indent}│  └─ Value: {structure['value']}")

    if "module_contents" in structure:
        print(f"{indent}│  └─ Module contents:")
        for item_name, item_type in structure["module_contents"].items():
            print(f"{indent}│     └─ {item_name}: {item_type['type_name']}")

    if "class_contents" in structure:
        print(f"{indent}│  └─ Class contents:")
        for item_name, item_type in structure["class_contents"].items():
            print(f"{indent}│     └─ {item_name}: {item_type['type_name']}")

    if "signature" in structure:
        print(f"{indent}│  └─ Signature: {structure['signature']}")

    if "attributes" in structure:
        print(f"{indent}│  └─ Attributes:")
        for attr, value in structure["attributes"].items():
            print_tree_structure(value, indent + "│     ")

    if "coroutine_info" in structure:
        print(f"{indent}│  └─ Coroutine info: {structure['coroutine_info']}")

    if "custom_rendering" in structure:
        print(f"{indent}│  └─ Custom rendering: {structure['custom_rendering']}")

def get_inspection_metadata() -> Dict[str, str]:
    """Get metadata about the inspection process."""
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "python_version": sys.version,
        "platform": platform.platform()
    }
# File: variable_inspector.py (Part 2)

def inspect_any(variable: Any, variable_name: str = "unnamed_variable", max_depth: Optional[Dict[type, int]] = None,
                print_to_console: bool = True, output_format: str = "text", include_private: bool = False,
                sample_size: int = 100) -> Dict[str, Any]:
    """
    Inspect any type of variable, handling nested structures and providing detailed information.

    Args:
        variable (Any): The variable to be inspected.
        variable_name (str): The name of the variable for reference.
        max_depth (Optional[Dict[type, int]]): Maximum depth for nested structure traversal, per type.
        print_to_console (bool): Whether to print the output to console.
        output_format (str): Output format for console printing ('text', 'json', 'yaml', or 'tree').
        include_private (bool): Whether to include private attributes in the inspection.
        sample_size (int): Maximum number of items to process in large collections.

    Returns:
        Dict[str, Any]: A dictionary containing the structured information about the variable.
    """
    if max_depth is None:
        max_depth = {dict: 5, list: 5, tuple: 5, set: 5}

    def safe_repr(obj: Any) -> str:
        """Safely convert any object to a string representation."""
        try:
            return repr(obj)
        except Exception:
            return f"<unprintable object of type {type(obj).__name__}>"

    def should_include_attribute(attr_name: str) -> bool:
        """Determine if an attribute should be included in the inspection."""
        if not include_private and attr_name.startswith('_'):
            return False
        return attr_name not in {'__dict__', '__weakref__', '__module__'}

    def sample_large_collection(collection: Iterable) -> Iterable:
        """Sample a large collection to a manageable size."""
        if isinstance(collection, (list, tuple, set)) and len(collection) > sample_size:
            return random.sample(list(collection), sample_size)
        return collection

    def calculate_dynamic_max_depth(var: Any) -> int:
        """Calculate a dynamic max depth based on the variable's complexity."""
        if isinstance(var, (dict, list, tuple, set)):
            return min(10, max(1, 7 - len(var) // 100))
        return 5

    def inspect_recursive(var: Any, name: str, current_depth: int = 0, seen: Optional[Set[int]] = None) -> Dict[str, Any]:
        if seen is None:
            seen = set()

        if id(var) in seen:
            return {"circular_reference": True, "name": name}
        seen.add(id(var))

        var_type = type(var)
        type_max_depth = max_depth.get(var_type, calculate_dynamic_max_depth(var))
        if current_depth > type_max_depth:
            return {"max_depth_reached": True, "name": name, "type": str(var_type)}

        result = {
            "name": name,
            "type_info": get_type_info(var)
        }

        if var_type in custom_renderers:
            result["custom_rendering"] = custom_renderers[var_type](var)

        if isinstance(var, dict):
            result["value"] = {safe_repr(k): inspect_recursive(v, f"{name}[{safe_repr(k)}]", current_depth + 1, seen)
                               for k, v in sample_large_collection(var.items())}
        elif isinstance(var, (list, tuple, set)):
            result["value"] = [inspect_recursive(item, f"{name}[{i}]", current_depth + 1, seen)
                               for i, item in enumerate(sample_large_collection(var))]
        elif inspect.ismodule(var):
            result["module_contents"] = {item_name: get_type_info(item)
                                         for item_name, item in inspect.getmembers(var)
                                         if should_include_attribute(item_name)}
        elif inspect.isclass(var):
            result["class_contents"] = {item_name: get_type_info(item)
                                        for item_name, item in inspect.getmembers(var)
                                        if should_include_attribute(item_name)}
        elif inspect.isfunction(var) or inspect.ismethod(var):
            result["signature"] = str(inspect.signature(var))
        elif asyncio.iscoroutine(var) or asyncio.iscoroutinefunction(var):
            result["coroutine_info"] = {
                "type": "coroutine" if asyncio.iscoroutine(var) else "coroutine function",
                "name": var.__name__ if hasattr(var, "__name__") else "unnamed"
            }
        elif hasattr(var, '__dict__'):
            result["attributes"] = {attr: inspect_recursive(value, attr, current_depth + 1, seen)
                                    for attr, value in vars(var).items()
                                    if should_include_attribute(attr)}
        elif isinstance(var, (int, float, str, bool, type(None))):
            result["value"] = var
        elif isinstance(var, (datetime.datetime, datetime.date, datetime.time)):
            result["value"] = var.isoformat()
        else:
            result["value"] = safe_repr(var)

        return result

    try:
        inspection_result = inspect_recursive(variable, variable_name)
        inspection_result["metadata"] = get_inspection_metadata()

        if print_to_console:
            if output_format == "text":
                print_structure(inspection_result)
            elif output_format == "json":
                print(json.dumps(inspection_result, indent=2, default=str))
            elif output_format == "yaml":
                print(yaml.dump(inspection_result, default_flow_style=False))
            elif output_format == "tree":
                print_tree_structure(inspection_result)
            else:
                print(f"Unsupported output format: {output_format}")

        return inspection_result
    except Exception as e:
        error_msg = f"Error occurred while inspecting {variable_name}: {str(e)}"
        logging.error(error_msg)
        if print_to_console:
            print(error_msg)
        return {"error": error_msg, "variable_name": variable_name}

def figure_variable(variable: Any, variable_name: str = "unnamed_variable",
                    max_depth: Optional[Dict[type, int]] = None,
                    output_format: str = "text",
                    include_private: bool = False,
                    sample_size: int = 100) -> None:
    """
    Analyze and print information about a variable based on its type.

    Args:
        variable (Any): The variable to be analyzed.
        variable_name (str): The name of the variable for reference.
        max_depth (Optional[Dict[type, int]]): Maximum depth for nested structure traversal, per type.
        output_format (str): Output format for console printing ('text', 'json', 'yaml', or 'tree').
        include_private (bool): Whether to include private attributes in the inspection.
        sample_size (int): Maximum number of items to process in large collections.
    """
    result = inspect_any(variable, variable_name, max_depth, False, output_format, include_private, sample_size)

    print(f"\nAnalysis of variable '{variable_name}':")
    print(f"Type: {type(variable).__name__}")

    if isinstance(variable, (int, float, str, bool, type(None))):
        print(f"Value: {variable}")
    elif isinstance(variable, (list, tuple, set)):
        print(f"Length: {len(variable)}")
        print(f"First few elements: {list(variable)[:5]}")
    elif isinstance(variable, dict):
        print(f"Number of keys: {len(variable)}")
        print(f"Keys: {list(variable.keys())[:5]}")
    elif inspect.isfunction(variable) or inspect.ismethod(variable):
        print(f"Signature: {inspect.signature(variable)}")
    elif inspect.isclass(variable):
        print("Class attributes:")
        for name, value in inspect.getmembers(variable):
            if not name.startswith("__"):
                print(f"  {name}: {type(value).__name__}")
    elif inspect.ismodule(variable):
        print("Module contents:")
        for name, value in inspect.getmembers(variable):
            if not name.startswith("__"):
                print(f"  {name}: {type(value).__name__}")

    print("\nDetailed inspection result:")
    if output_format == "text":
        print_structure(result)
    elif output_format == "json":
        print(json.dumps(result, indent=2, default=str))
    elif output_format == "yaml":
        print(yaml.dump(result, default_flow_style=False))
    elif output_format == "tree":
        print_tree_structure(result)
    else:
        print(f"Unsupported output format: {output_format}")

    if "circular_reference" in result:
        print("Note: Circular reference detected in the structure.")

    print("\nMetadata:")
    print(json.dumps(result.get("metadata", {}), indent=2))

# This block allows the module to be run as a script for testing purposes
if __name__ == "__main__":
    # Example usage
    example_var = {"a": 1, "b": [2, 3, 4], "c": {"d": 5}}
    figure_variable(example_var, "example_var")
