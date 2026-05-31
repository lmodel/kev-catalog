#!/usr/bin/env python3
"""Wrapper around `linkml-run-examples` that applies the same in-place
patches as `scripts/patch_pythongen.py` to the python source the example
runner compiles in-process.

`linkml.workspaces.example_runner.ExampleRunner.python_module` calls
`PythonGenerator(src).compile_module()` to obtain the dataclasses used
for example loading. Without our patches the freshly generated source
hits the same upstream defects covered in `docs/about.md` (issue #3572
forward-references, enum-wrapper membership, PermissibleValue /
EnumDefinitionImpl hash and str-eq), so example validation aborts even
though the on-disk model under `src/fix_protocol/datamodel/` has long
since been patched.

This wrapper monkey-patches `PythonGenerator.compile_module` so that
the generated source is passed through the same `reorder`,
`alias_enum_wrappers` and `inject_permissible_value_patch` transforms
before `compile_python` runs. The CLI args are forwarded verbatim to
the upstream runner.

Usage (forwarded to upstream `linkml-run-examples`):
    python scripts/run_examples_patched.py \\
        --schema src/fix_protocol/schema/fix_protocol.yaml \\
        --input-directory tests/data/valid \\
        --counter-example-input-directory tests/data/invalid \\
        --output-directory examples/output \\
        --input-formats yaml --output-formats yaml
"""
from __future__ import annotations

import sys
from pathlib import Path

# Re-use the on-disk patcher's transforms — both scripts live in
# `scripts/` (no package), so add it to sys.path before importing.
sys.path.insert(0, str(Path(__file__).parent))
import patch_pythongen  # noqa: E402

from linkml.generators.pythongen import PythonGenerator  # noqa: E402
from linkml_runtime.utils.compile_python import compile_python  # noqa: E402
from linkml.workspaces.example_runner import cli  # noqa: E402


def _patched_compile_module(self, **kwargs):
    pycode = self.serialize(**kwargs)
    pycode = patch_pythongen.inject_permissible_value_patch(
        patch_pythongen.alias_enum_wrappers(
            patch_pythongen.reorder(pycode),
        )
    )
    return compile_python(pycode)


PythonGenerator.compile_module = _patched_compile_module


if __name__ == "__main__":
    cli(standalone_mode=True)
