#!/usr/bin/env python3
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data"
SCHEMA_PATH = ROOT / ".agents" / "skills" / "user-json-memory" / "user.schema.json"


def load_json(path: Path):
    with path.open() as handle:
        return json.load(handle)


def validate_ref(schema, value, ref):
    ref_schema = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        "$ref": ref,
    }
    jsonschema.validate(value, ref_schema)


def main():
    schema = load_json(SCHEMA_PATH)
    index_path = DATA / "user" / "index.json"
    index = load_json(index_path)
    jsonschema.validate(index, schema)

    user_dir = index_path.parent
    files = index["files"]

    validate_ref(schema, load_json(user_dir / files["profile"]), "#/$defs/profileFile")
    validate_ref(schema, load_json(user_dir / files["skills"]), "#/$defs/skillsFile")
    validate_ref(schema, load_json(user_dir / files["resume_preferences"]), "#/$defs/resumePreferencesFile")
    validate_ref(schema, load_json(user_dir / files["projects"]), "#/$defs/projectsFile")
    validate_ref(schema, load_json(user_dir / files["education"]), "#/$defs/educationFile")
    validate_ref(schema, load_json(user_dir / files["certifications"]), "#/$defs/certificationsFile")

    for role_file in files["experience"]:
        validate_ref(schema, load_json(user_dir / role_file), "#/$defs/experienceRoleFile")

    print("user memory schema ok")


if __name__ == "__main__":
    main()
