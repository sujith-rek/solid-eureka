import json
from env_variables import CLEAN_SWAGGER_FILE, SWAGGER_FILE


def get_attributes(schemas: dict) -> dict:
    return {schema: schemas[schema] for schema in schemas if
            "type" in schemas[schema] and "properties" not in schemas[schema]}


def delete_attributes(schemas: dict) -> None:
    updates = [schema for schema in schemas if "type" in schemas[schema] and "properties" not in schemas[schema]]
    for schema in updates:
        del schemas[schema]


def replace_refs_with_types(data: dict, typ: dict) -> None:
    if isinstance(data, dict):
        updates = []
        for key, value in data.items():
            if key == "$ref" and value.startswith("#/components/schemas/"):
                ref_key = value.split("/")[-1]
                if ref_key in typ:
                    updates.append((key, typ[ref_key]))
            else:
                replace_refs_with_types(value, typ)
        for key, new_value in updates:
            data.update(new_value)
            del data[key]
    elif isinstance(data, list):
        for item in data:
            replace_refs_with_types(item, typ)


def deal_required_properties(schemas: dict) -> None:
    updates = []
    for schema in schemas:
        if "required" in schemas[schema]:
            for required in schemas[schema]["required"]:
                if required in schemas[schema]["properties"]:
                    schemas[schema]["properties"][required]["required"] = True
            updates.append(schema)
    for schema in updates:
        del schemas[schema]["required"]


def resolve_all_of(schema: dict, schemas: dict) -> dict:
    resolved = {"properties": {}}
    for item in schema.get("allOf", []):
        if "$ref" in item:
            ref_key = item["$ref"].split("/")[-1]
            if ref_key in schemas:
                resolved["properties"].update(resolve_all_of(schemas[ref_key], schemas).get("properties", {}))
        else:
            resolved["properties"].update(item.get("properties", {}))
    if "allOf" not in schema:
        resolved["properties"].update(schema.get("properties", {}))
    return resolved


def deal_all_of_properties_and_required(schemas: dict) -> None:
    for schema_name, schema in schemas.items():
        if "allOf" in schema:
            resolved_schema = resolve_all_of(schema, schemas)
            schemas[schema_name] = resolved_schema
            if "required" in resolved_schema:
                for required in resolved_schema["required"]:
                    if required in resolved_schema["properties"]:
                        resolved_schema["properties"][required]["required"] = True
                del resolved_schema["required"]


def deal_with_remaining_refs(schemas: dict) -> None:
    for schema_name, schema in schemas.items():
        replace_refs_with_types(schema, schemas)


def remove_type_object(data: dict) -> None:
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == "type" and value == "object":
                del data[key]
            else:
                remove_type_object(value)
    elif isinstance(data, list):
        for item in data:
            remove_type_object(item)


def get_all_types(data: dict) -> set:
    types = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "type":
                types.add(value)
            else:
                types.update(get_all_types(value))
    elif isinstance(data, list):
        for item in data:
            types.update(get_all_types(item))
    return types


def main():
    with open(SWAGGER_FILE, "r") as file:
        data = json.load(file)

    schemas = data["components"]["schemas"]
    typ = get_attributes(schemas)
    replace_refs_with_types(data, typ)
    delete_attributes(schemas)
    deal_required_properties(schemas)
    deal_all_of_properties_and_required(schemas)
    deal_with_remaining_refs(schemas)
    remove_type_object(schemas)

    with open(CLEAN_SWAGGER_FILE, "w") as file:
        json.dump(schemas, file, indent=2)


if __name__ == "__main__":
    main()
