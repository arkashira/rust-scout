import argparse
import json
from dataclasses import dataclass
from typing import List

@dataclass
class Crate:
    name: str
    version: str
    description: str
    link: str

def search_crates(query: str) -> List[Crate]:
    # Simulate searching for crates
    crates = [
        Crate("crate1", "1.0.0", "A short description", "https://crates.io/crate1"),
        Crate("crate2", "2.0.0", "Another short description", "https://crates.io/crate2"),
        Crate("crate3", "3.0.0", "Yet another short description", "https://crates.io/crate3"),
    ]
    return [crate for crate in crates if query.lower() in crate.name.lower()]

def add_crate(crate_name: str, cargo_toml: str) -> None:
    # Simulate adding a crate to Cargo.toml
    with open(cargo_toml, "a") as f:
        f.write(f"[dependencies]\n{crate_name} = \"1.0.0\"\n")

def main() -> None:
    parser = argparse.ArgumentParser(description="Rust Scout CLI tool")
    subparsers = parser.add_subparsers(dest="command")
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query", help="Search query")
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("crate", help="Crate name")
    add_parser.add_argument("--cargo-toml", default="Cargo.toml", help="Path to Cargo.toml")
    args = parser.parse_args()
    if args.command == "search":
        crates = search_crates(args.query)
        for crate in crates[:5]:
            print(json.dumps(crate.__dict__))
    elif args.command == "add":
        add_crate(args.crate, args.cargo_toml)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
