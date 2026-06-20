import pytest
from cargo_toml_generator import generate_cargo_toml, load_library_from_json, Library
import json

def test_generate_cargo_toml():
    library = Library(
        name="my_library",
        version="1.0.0",
        dependencies={"dep1": "1.0.0", "dep2": "2.0.0"}
    )
    cargo_toml = generate_cargo_toml(library)
    assert "my_library" in cargo_toml
    assert "1.0.0" in cargo_toml
    assert "dep1" in cargo_toml
    assert "dep2" in cargo_toml

def test_load_library_from_json():
    json_data = '''
    {
        "name": "my_library",
        "version": "1.0.0",
        "dependencies": {
            "dep1": "1.0.0",
            "dep2": "2.0.0"
        }
    }
    '''
    library = load_library_from_json(json_data)
    assert library.name == "my_library"
    assert library.version == "1.0.0"
    assert library.dependencies == {"dep1": "1.0.0", "dep2": "2.0.0"}

def test_generate_cargo_toml_empty_dependencies():
    library = Library(
        name="my_library",
        version="1.0.0",
        dependencies={}
    )
    cargo_toml = generate_cargo_toml(library)
    assert "my_library" in cargo_toml
    assert "1.0.0" in cargo_toml
    assert "dependencies" not in cargo_toml

def test_load_library_from_json_invalid_json():
    json_data = "invalid json"
    with pytest.raises(json.JSONDecodeError):
        load_library_from_json(json_data)
