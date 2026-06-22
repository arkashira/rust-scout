import pytest
from rust_libraries import RustLibrary, RustLibraryCurator, load_libraries_from_json

def test_load_libraries_from_json():
    json_data = '''
    [
        {"name": "lib1", "benchmark_score": 10.0},
        {"name": "lib2", "benchmark_score": 20.0},
        {"name": "lib3", "benchmark_score": 30.0}
    ]
    '''
    libraries = load_libraries_from_json(json_data)
    assert len(libraries) == 3
    assert libraries[0].name == 'lib1'
    assert libraries[0].benchmark_score == 10.0

def test_rust_library_curator_get_libraries():
    libraries = [RustLibrary('lib1', 10.0), RustLibrary('lib2', 20.0), RustLibrary('lib3', 30.0)]
    curator = RustLibraryCurator(libraries)
    result = curator.get_libraries(sort_by='benchmark_score')
    assert len(result) == 3
    assert result[0].name == 'lib1'
    assert result[0].benchmark_score == 10.0

def test_rust_library_curator_get_libraries_filter_by_name():
    libraries = [RustLibrary('lib1', 10.0), RustLibrary('lib2', 20.0), RustLibrary('lib3', 30.0)]
    curator = RustLibraryCurator(libraries)
    result = curator.get_libraries(filter_by='name', filter_value='lib2')
    assert len(result) == 1
    assert result[0].name == 'lib2'
    assert result[0].benchmark_score == 20.0

def test_rust_library_curator_add_library():
    libraries = [RustLibrary('lib1', 10.0), RustLibrary('lib2', 20.0)]
    curator = RustLibraryCurator(libraries)
    curator.add_library(RustLibrary('lib3', 30.0))
    assert len(curator.libraries) == 3
    assert curator.libraries[2].name == 'lib3'
    assert curator.libraries[2].benchmark_score == 30.0

def test_rust_library_curator_remove_library():
    libraries = [RustLibrary('lib1', 10.0), RustLibrary('lib2', 20.0), RustLibrary('lib3', 30.0)]
    curator = RustLibraryCurator(libraries)
    curator.remove_library('lib2')
    assert len(curator.libraries) == 2
    assert curator.libraries[0].name == 'lib1'
    assert curator.libraries[1].name == 'lib3'
