import os
import json
from typing import Any, Dict
from env_variables import CLEAN_SWAGGER_FILE, SCHEMAS_DIR


def convert_to_class(name: str, properties: Dict[str, Any]) -> str:
    """
    Converts a dictionary of properties into a Python class definition with proper parameter documentation.
    """
    class_lines = [f"class {name}:"]
    if not properties:
        class_lines.append("\tpass\n")
        return "\n".join(class_lines)

    # Add class-level documentation
    class_lines.append(f'\t""" {name} class generated from schema. """\n')

    # Prepare __init__ method
    init_signature = ["\tdef __init__(\n\t\tself, "]
    init_docstring = ["\t\t\"\"\""]
    init_body = []

    # Extract required and optional properties
    required_props = {k: v for k, v in properties.items() if v.get("required", False)}
    optional_props = {k: v for k, v in properties.items() if not v.get("required", False)}

    # Add required properties to signature and docstring
    for var_name, var_info in required_props.items():
        py_type = map_json_type_to_python(var_info["type"])
        constraints = extract_constraints(var_info)
        init_signature.append(f"\t\t{var_name}: {py_type}, ")
        init_docstring.append(f"\t\t:param {var_name}: {constraints}")
        init_body.append(f"\t\tself.{var_name}: {py_type} = {var_name}")

    # Add optional properties to signature and docstring
    for var_name, var_info in optional_props.items():
        py_type = map_json_type_to_python(var_info["type"])
        constraints = extract_constraints(var_info)
        init_signature.append(f"\t\t{var_name}: {py_type} = None, ")
        init_docstring.append(f"\t\t:param {var_name}: {constraints}")
        init_body.append(f"\t\tself.{var_name}: {py_type} = {var_name}")

    # Finalize method signature and docstring
    init_signature[-1] = init_signature[-1].rstrip(", ")  # Remove trailing comma
    init_signature.append("\t):")
    init_docstring.append("\t\t\"\"\"")

    # Combine everything
    class_lines.extend(init_signature)
    class_lines.extend(init_docstring)
    class_lines.append("")  # Blank line before method body
    class_lines.extend(init_body)
    return "\n".join(class_lines) + "\n"


def map_json_type_to_python(json_type: str) -> str:
    """
    Maps JSON schema types to Python types.
    """
    if json_type == "integer":
        return "int"
    if json_type == "string":
        return "str"
    if json_type == "array":
        return "list"
    return "Any"


def extract_constraints(var_info: Dict[str, Any]) -> str:
    """
    Extracts constraints from a property's metadata for documentation.
    """
    constraints = []
    for key in ["minimum", "maximum", "minLength", "maxLength", "pattern", "enum", "example", "items"]:
        if key in var_info:
            if key == "items":  # Special handling for array properties
                constraints.append(f"{key}: {extract_array_items(var_info[key])}")
            else:
                constraints.append(f"{key}: {var_info[key]}")
    return ", ".join(constraints)


def extract_array_items(items: Dict[str, Any]) -> str:
    """
    Extracts details about the 'items' property of an array type.
    """
    if "type" in items:
        return f"type: {items['type']}, " + extract_constraints(items)
    return "Unknown"


def write_classes_to_files(schema: Dict[str, Any], output_dir: str):
    """
    Writes the schema classes to individual files in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    for class_name, class_data in schema.items():
        properties = class_data.get("properties", {})
        class_code = convert_to_class(class_name, properties)
        with open(os.path.join(output_dir, f"{class_name}.py"), "w") as f:
            f.write(class_code)


if __name__ == "__main__":
    # Load JSON schema
    with open(CLEAN_SWAGGER_FILE, "r") as file:
        schema = json.load(file)

    output_directory = SCHEMAS_DIR
    write_classes_to_files(schema, output_directory)
    print(f"Classes written to {output_directory} directory.")
