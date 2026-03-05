"""Access to the generated SHACL shapes."""

from importlib.resources import files

SHACL_PATH = files("ckn_schema.shacl").joinpath("ckn_schema.shacl.ttl")
