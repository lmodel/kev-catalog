#!/usr/bin/env python3
"""Wrapper for linkml gen-yaml that patches SafeDumper before running.

linkml-runtime 1.11.0 (PyPI release) omits the line:
    yaml.SafeDumper.add_multi_representer(JsonObj, root_representer)
so gen-yaml raises:
    yaml.representer.RepresenterError: cannot represent an object, JsonObj(...)
for any slot whose annotations are stored as a JsonObj by the schema loader.

The fix was added between 1.11.0 and 1.11.0rc1.post104.dev0; until a patched
release is on PyPI, this wrapper registers the missing representer first.

"""

import yaml
from jsonasobj2 import JsonObj, as_dict
from linkml.generators.yamlgen import cli

# Backport fix: linkml-runtime registers root_representer only for YAMLRoot,
# so JsonObj values (e.g. slot annotations) still raise RepresenterError.
# Register a JsonObj-specific representer if one isn't already present.
if JsonObj not in getattr(yaml.SafeDumper, "yaml_multi_representers", {}):
    def _jsonobj_representer(dumper, data):
        return dumper.represent_dict(as_dict(data))
    yaml.SafeDumper.add_multi_representer(JsonObj, _jsonobj_representer)

if __name__ == "__main__":
    cli()
