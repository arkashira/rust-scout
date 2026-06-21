import pytest
from rust_scout import Library, LibraryManager
from datetime import datetime, timedelta


@pytest.fixture
def manager():
    mgr = LibraryManager()
    mgr.update_libraries()
    return mgr


def test_library_creation():
    lib = Library(
        name="TestLib",
        description="A test library",
        category="Test",
        stars=100,
        rating=4.0,
        performance_score=80,
        reviews=["Good"],
        last_updated=datetime.now()
    )
    assert lib.name == "TestLib"
    assert lib.stars == 100


def test_library_matches_search(manager):
    libs = manager.get_libraries(search_query="tokio")
    assert len(libs) == 1
    assert libs[0].name == "Tokio"
    
    # Case insensitive check
    libs = manager.get_libraries(search_query="SERDE")
    assert len(libs) == 1
    assert libs[0].name == "Serde"


def test_library_search_no_match(manager):
    libs = manager.get_libraries(search_query="nonexistentlibraryxyz")
    assert len(libs) == 0


def test_filter_by_category(manager):
    libs = manager.get_libraries(category="Web")
    assert len(libs) == 1
    assert libs[0].name == "Actix"
    
    libs = manager.get_libraries(category="Async")
    assert len(libs) == 1
    assert libs[0].name == "Tokio"


def test_filter_by_rating(manager):
    # Filter for high rating
    libs = manager.get_libraries(min_rating=4.9)
    assert len(libs) == 2
    names = {lib.name for lib in libs}
    assert "Tokio" in names
    assert "Serde" in names
    
    # Filter for very high rating (only Serde is 4.95)
    libs = manager.get_libraries(min_rating=4.94)
    assert len(libs) == 1
    assert libs[0].name == "Serde"


def test_combined_filters(manager):
    # Search for "web" framework with rating > 4.0
    libs = manager.get_libraries(search_query="web", min_rating=4.0)
    assert len(libs) == 1
    assert libs[0].name == "Actix"


def test_sort_by_stars(manager):
    libs = manager.get_libraries(sort_by_stars=True)
    assert len(libs) > 0
    # Serde has 31000, Tokio 24500, Actix 18500...
    assert libs[0].name == "Serde"
    assert libs[1].name == "Tokio"
    assert libs[2].name == "Actix"


def test_update_needed_initially():
    mgr = LibraryManager()
    assert mgr.is_update_needed() is True


def test_update_needed_after_fetch(manager):
    # Just updated, so should not be needed
    assert manager.is_update_needed() is False


def test_get_library_names(manager):
    names = manager.get_library_names()
    assert isinstance(names, list)
    assert "Tokio" in names
    assert "Serde" in names
    assert len(names) == 5


def test_edge_case_empty_query(manager):
    # Empty query should return everything (respecting other filters)
    libs = manager.get_libraries(search_query="")
    assert len(libs) == 5


def test_edge_case_rating_boundary(manager):
    # Diesel has 4.5 rating
    libs = manager.get_libraries(min_rating=4.5)
    assert len(libs) == 5 # All are >= 4.5
    
    libs = manager.get_libraries(min_rating=4.51)
    assert len(libs) == 4 # Diesel (4.5) is excluded
    assert "Diesel" not in [l.name for l in libs]
