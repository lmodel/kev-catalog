# Example data for kev-catalog

This folder holds the examples the tests check, in subfolders:

- `valid` for data that conforms to the schema. Each entry there is a real entry of the pinned catalogue, or a real entry cut down to the keys CISA requires.
- `invalid` for counter-examples. The first line of each, `# Fails at: <pointer>`, names where the validator must report it.
- `problem/valid` for valid data that the generated dataclasses refuse under LinkML 1.12.1: a required multivalued slot treats an empty list as missing. `tests/test_data.py` validates these examples and loads them through the Pydantic model; the example runner leaves them out.
- `kev-data` for the pinned catalogue: `manifest.json` pins it by address, size and hash, `extract/` holds twelve real entries copied unchanged, and `just test-kev-data` fetches the full file into `tmp/kev-data/` and validates it.

Each file name in `valid` and `invalid` is `ClassName-anything.yaml`, and the part before the first `-` names the class the file is checked against.

In YAML, quote the values `"Yes"` and `"No"` of `forensicTriage`: unquoted, YAML reads them as booleans, and they fail. CISA's JSON has no such trap.
