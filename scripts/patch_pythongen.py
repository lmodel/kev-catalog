#!/usr/bin/env python3
"""Post-process a `gen-python` (`pythongen`) output file in place.

Works around three upstream LinkML defects:

1. https://github.com/linkml/linkml/issues/3572 — the generator emits a
   "Class references" section near the top of the module containing
   wrapper classes like

       class FIXDatatypeDatatypeName(FIXDatatypeName):
           pass

   when an `identifier: true` slot has an enum range. The base class
   is defined much later in the same file, so importing the module
   raises `NameError` at the wrapper definition.

   Fix: relocate the entire "Class references" block to immediately
   after the "Enumerations" block so the bases resolve.

2. `EnumDefinitionMeta.__contains__` / `__getitem__` ignore the MRO,
   so the empty wrappers `class W(E): pass` (where `E` is an enum)
   raise `ValueError: Unknown W enumeration code: ...` when
   instantiated.

   Fix: replace each such wrapper with a module-level alias `W = E`.
   The wrapper name still resolves for annotations and `isinstance`
   checks, while routing membership tests to the parent enum.

3. `PermissibleValue` instances are unhashable (`__hash__ = None`)
   and `__eq__` is not text-comparable to strings, so enum values
   cannot be used as dict keys or compared directly to string codes.

   Fix: inject a small module-level monkey-patch that adds a
   `text`-based `__hash__` and widens `__eq__` to accept `str`.

Usage:
    python scripts/patch_pythongen.py <path-to-generated.py>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CLASS_REFS_MARKER = "# Class references"
ENUMS_MARKER = "# Enumerations"


def _find_section_start(lines: list[str], marker: str) -> int:
    for i, line in enumerate(lines):
        if line.rstrip() == marker:
            return i
    raise SystemExit(f"marker {marker!r} not found")


def _find_next_section_start(lines: list[str], start: int) -> int:
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.startswith("# ") and not line.startswith("# - "):
            if i > 0 and lines[i - 1].strip() == "":
                return i
    return len(lines)


def reorder(text: str) -> str:
    lines = text.splitlines(keepends=True)

    refs_start = _find_section_start(lines, CLASS_REFS_MARKER)
    enums_start = _find_section_start(lines, ENUMS_MARKER)

    if refs_start > enums_start:
        return text

    refs_end = _find_next_section_start(lines, refs_start)
    while refs_end > refs_start and lines[refs_end - 1].strip() == "":
        refs_end -= 1

    refs_block = lines[refs_start:refs_end]
    remaining = lines[:refs_start] + lines[refs_end:]

    enums_start_new = _find_section_start(remaining, ENUMS_MARKER)
    insertion_point = _find_next_section_start(remaining, enums_start_new)

    if refs_block and refs_block[-1].strip() != "":
        refs_block.append("\n")
    if refs_block and refs_block[0].strip() != "":
        refs_block.insert(0, "\n")

    patched = remaining[:insertion_point] + refs_block + remaining[insertion_point:]
    return "".join(patched)


_ENUM_BASE_RE = re.compile(
    r"^class\s+([A-Za-z_][A-Za-z_0-9]*)\(EnumDefinitionImpl\)\s*:\s*\n",
    re.MULTILINE,
)
_WRAPPER_RE = re.compile(
    r"^class\s+([A-Za-z_][A-Za-z_0-9]*)\(([A-Za-z_][A-Za-z_0-9]*)\)\s*:\s*\n"
    r"\s+pass\s*\n",
    re.MULTILINE,
)


_PV_PATCH_MARKER = "# fix-protocol patch: enum hash/eq"
_PV_PATCH_BLOCK = f'''{_PV_PATCH_MARKER}
from linkml_runtime.linkml_model.meta import PermissibleValue as _PV
from linkml_runtime.utils.enumerations import EnumDefinitionImpl as _EDI
if not getattr(_PV, "_fix_protocol_patched", False):
    _orig_pv_eq = _PV.__eq__
    def _pv_eq(self, other):
        if isinstance(other, str):
            return self.text == other
        return _orig_pv_eq(self, other)
    _PV.__eq__ = _pv_eq
    _PV.__hash__ = lambda self: hash(self.text)
    _PV._fix_protocol_patched = True
if not getattr(_EDI, "_fix_protocol_patched", False):
    _orig_edi_eq = _EDI.__eq__
    def _edi_eq(self, other):
        if isinstance(other, str):
            return str(self) == other
        return _orig_edi_eq(self, other)
    # Bypass EnumDefinitionMeta.__setattr__, which routes assignments on
    # enum subclasses through PermissibleValue handling.
    type.__setattr__(_EDI, "__eq__", _edi_eq)
    type.__setattr__(_EDI, "__hash__", lambda self: hash(str(self)))
    type.__setattr__(_EDI, "_fix_protocol_patched", True)
'''


def inject_permissible_value_patch(text: str) -> str:
    """Inject a module-level monkey-patch that makes PermissibleValue
    hashable and str-comparable. Idempotent via _PV_PATCH_MARKER."""
    if _PV_PATCH_MARKER in text:
        return text
    anchor = "\nmetamodel_version = "
    idx = text.find(anchor)
    if idx == -1:
        raise SystemExit("anchor 'metamodel_version = ' not found")
    return text[: idx + 1] + _PV_PATCH_BLOCK + "\n" + text[idx + 1 :]


def alias_enum_wrappers(text: str) -> str:
    enum_names = {m.group(1) for m in _ENUM_BASE_RE.finditer(text)}
    if not enum_names:
        return text

    def _sub(match: re.Match[str]) -> str:
        wrapper, base = match.group(1), match.group(2)
        if base in enum_names:
            return f"{wrapper} = {base}\n"
        return match.group(0)

    return _WRAPPER_RE.sub(_sub, text)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <path-to-generated.py>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8")
    new_text = inject_permissible_value_patch(alias_enum_wrappers(reorder(text)))
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"patched {path}")
    else:
        print(f"no change needed for {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
