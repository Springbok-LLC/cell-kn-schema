"""Access to the raw LinkML YAML schema."""

from importlib.resources import files

SCHEMA_PATH = files("ckn_schema.schema").joinpath("ckn_schema.yaml")
