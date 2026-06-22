import json
from dataclasses import dataclass
from typing import List

@dataclass
class RustLibrary:
    name: str
    benchmark_score: float

class RustLibraryCurator:
    def __init__(self, libraries: List[RustLibrary]):
        self.libraries = libraries

    def get_libraries(self, sort_by: str = 'name', filter_by: str = None, filter_value: str = None):
        libraries = self.libraries
        if filter_by and filter_value:
            if filter_by == 'name':
                libraries = [lib for lib in libraries if lib.name == filter_value]
            elif filter_by == 'benchmark_score':
                libraries = [lib for lib in libraries if str(lib.benchmark_score) == filter_value]
        if sort_by == 'name':
            libraries.sort(key=lambda x: x.name)
        elif sort_by == 'benchmark_score':
            libraries.sort(key=lambda x: x.benchmark_score)
        return libraries

    def add_library(self, library: RustLibrary):
        self.libraries.append(library)

    def remove_library(self, library_name: str):
        self.libraries = [lib for lib in self.libraries if lib.name != library_name]

def load_libraries_from_json(json_data: str) -> List[RustLibrary]:
    data = json.loads(json_data)
    libraries = []
    for lib in data:
        libraries.append(RustLibrary(lib['name'], lib['benchmark_score']))
    return libraries

def main():
    json_data = '''
    [
        {"name": "lib1", "benchmark_score": 10.0},
        {"name": "lib2", "benchmark_score": 20.0},
        {"name": "lib3", "benchmark_score": 30.0}
    ]
    '''
    libraries = load_libraries_from_json(json_data)
    curator = RustLibraryCurator(libraries)
    print(curator.get_libraries(sort_by='benchmark_score'))
