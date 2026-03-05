"""Access to the generated JSON Schema."""

from importlib.resources import files

JSON_SCHEMA_PATH = files("ckn_schema.jsonschema").joinpath("ckn_schema.json")
