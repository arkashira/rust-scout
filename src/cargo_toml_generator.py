import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Library:
    name: str
    version: str
    dependencies: Dict[str, str]

def generate_cargo_toml(library: Library) -> str:
    cargo_toml = {
        "package": {
            "name": library.name,
            "version": library.version,
            "edition": "2021"
        }
    }
    if library.dependencies:
        cargo_toml["dependencies"] = library.dependencies
    return json.dumps(cargo_toml, indent=4)

def load_library_from_json(json_data: str) -> Library:
    try:
        data = json.loads(json_data)
        return Library(
            name=data["name"],
            version=data["version"],
            dependencies=data.get("dependencies", {})
        )
    except json.JSONDecodeError as e:
        raise e
