import json
from rust_scout import search_crates, add_crate, Crate
import pytest
from unittest.mock import patch, MagicMock
from tempfile import TemporaryDirectory

def test_search_crates():
    crates = search_crates("crate")
    assert len(crates) == 3
    for crate in crates:
        assert isinstance(crate, Crate)

def test_search_crates_empty_query():
    crates = search_crates("")
    assert len(crates) == 3

def test_add_crate():
    with TemporaryDirectory() as tmpdir:
        cargo_toml = f"{tmpdir}/Cargo.toml"
        add_crate("crate1", cargo_toml)
        with open(cargo_toml, "r") as f:
            contents = f.read()
            assert "[dependencies]" in contents
            assert "crate1 = \"1.0.0\"" in contents

def test_add_crate_invalid_crate_name():
    with TemporaryDirectory() as tmpdir:
        cargo_toml = f"{tmpdir}/Cargo.toml"
        with patch("builtins.open", side_effect=IOError("Invalid crate name")):
            with pytest.raises(IOError):
                add_crate("invalid_crate", cargo_toml)

def test_main_search():
    with patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(command="search", query="crate")):
        with patch("rust_scout.search_crates", return_value=[Crate("crate1", "1.0.0", "A short description", "https://crates.io/crate1")]):
            with patch("sys.stdout.write") as mock_write:
                from rust_scout import main
                main()
                mock_write.assert_called()

def test_main_add():
    with patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(command="add", crate="crate1", cargo_toml="Cargo.toml")):
        with TemporaryDirectory() as tmpdir:
            cargo_toml = f"{tmpdir}/Cargo.toml"
            with patch("rust_scout.add_crate") as mock_add_crate:
                from rust_scout import main
                main()
                mock_add_crate.assert_called_with("crate1", "Cargo.toml")
