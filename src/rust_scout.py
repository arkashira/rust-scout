import dataclasses
from datetime import datetime, timedelta
from typing import List, Optional


@dataclasses.dataclass
class Library:
    """Represents a Rust library with its metrics and reviews."""
    name: str
    description: str
    category: str
    stars: int
    rating: float
    performance_score: int  # 0-100
    reviews: List[str]
    last_updated: datetime

    def matches_search(self, query: str) -> bool:
        """Checks if the library matches the search query (case-insensitive)."""
        q = query.lower()
        return q in self.name.lower() or q in self.description.lower()

    def passes_filters(self, category: Optional[str], min_rating: Optional[float]) -> bool:
        """Checks if the library passes category and rating filters."""
        if category and self.category.lower() != category.lower():
            return False
        if min_rating is not None and self.rating < min_rating:
            return False
        return True


class LibraryManager:
    """Manages the collection of Rust libraries, handling updates and queries."""
    
    def __init__(self):
        self._libraries: List[Library] = []
        self._last_fetch_date: Optional[datetime] = None

    def _fetch_mock_data(self) -> List[Library]:
        """
        Simulates fetching data from an external API (e.g., crates.io or GitHub).
        In a real scenario, this would perform HTTP requests.
        """
        now = datetime.now()
        return [
            Library(
                name="Tokio",
                description="A runtime for writing reliable asynchronous applications with Rust.",
                category="Async",
                stars=24500,
                rating=4.9,
                performance_score=98,
                reviews=["Essential for async rust", "Great documentation"],
                last_updated=now
            ),
            Library(
                name="Serde",
                description="A framework for serializing and deserializing Rust data structures.",
                category="Encoding",
                stars=31000,
                rating=4.95,
                performance_score=95,
                reviews=["The standard for serialization", "Very flexible"],
                last_updated=now
            ),
            Library(
                name="Actix",
                description="A powerful, pragmatic, and extremely fast web framework for Rust.",
                category="Web",
                stars=18500,
                rating=4.7,
                performance_score=99,
                reviews=["Blazing fast", "Actor model is interesting"],
                last_updated=now
            ),
            Library(
                name="Clap",
                description="A full featured, fast Command Line Argument Parser.",
                category="CLI",
                stars=12500,
                rating=4.8,
                performance_score=90,
                reviews=["Easy to use", "Derive macros are great"],
                last_updated=now
            ),
            Library(
                name="Diesel",
                description="A safe, extensible ORM and Query Builder for Rust.",
                category="Database",
                stars=11000,
                rating=4.5,
                performance_score=85,
                reviews=["Compile time checks are awesome", "Steep learning curve"],
                last_updated=now
            )
        ]

    def update_libraries(self) -> None:
        """Updates the internal list of libraries. Simulates a daily fetch."""
        self._libraries = self._fetch_mock_data()
        self._last_fetch_date = datetime.now()

    def is_update_needed(self) -> bool:
        """Checks if the library list needs updating (simulated 24h check)."""
        if self._last_fetch_date is None:
            return True
        return datetime.now() - self._last_fetch_date > timedelta(hours=24)

    def get_libraries(
        self, 
        search_query: str = "", 
        category: Optional[str] = None, 
        min_rating: Optional[float] = None,
        sort_by_stars: bool = False
    ) -> List[Library]:
        """
        Retrieves libraries based on search and filter criteria.
        
        Args:
            search_query: String to match against name or description.
            category: Specific category to filter by.
            min_rating: Minimum rating (0.0 to 5.0).
            sort_by_stars: If True, sorts results by star count descending.
            
        Returns:
            A list of Library objects matching the criteria.
        """
        results = []
        for lib in self._libraries:
            if lib.matches_search(search_query) and lib.passes_filters(category, min_rating):
                results.append(lib)
        
        if sort_by_stars:
            results.sort(key=lambda x: x.stars, reverse=True)
            
        return results

    def get_library_names(self) -> List[str]:
        """Returns a simple list of all library names currently loaded."""
        return [lib.name for lib in self._libraries]
