import pytest
from rust_scout import calculate_star_trend_score, calculate_performance_score, calculate_security_score, calculate_composite_score, rank_crates, load_crates

def test_calculate_star_trend_score():
    assert calculate_star_trend_score(100, 120) == 20.0
    assert calculate_star_trend_score(0, 100) == 0

def test_calculate_performance_score():
    assert calculate_performance_score(90) == 100
    assert calculate_performance_score(80) == 80

def test_calculate_security_score():
    assert calculate_security_score(0) == 100
    assert calculate_security_score(1) == 90
    assert calculate_security_score(10) == 0

def test_calculate_composite_score():
    assert calculate_composite_score(20, 100, 90) == (20 * 0.4) + (100 * 0.35) + (90 * 0.25)

def test_rank_crates():
    crates_data = [
        {'name': 'crate1', 'stars': 100, 'stars_30_days_ago': 80, 'performance_score': 90, 'security_score': 100, 'cves': 0},
        {'name': 'crate2', 'stars': 120, 'stars_30_days_ago': 100, 'performance_score': 80, 'security_score': 90, 'cves': 1},
    ]
    crates = load_crates(crates_data)
    ranked_crates = rank_crates(crates)
    assert ranked_crates[0][0] == 'crate1'

def test_load_crates():
    crates_data = [
        {'name': 'crate1', 'stars': 100, 'stars_30_days_ago': 80, 'performance_score': 90, 'security_score': 100, 'cves': 0},
        {'name': 'crate2', 'stars': 120, 'stars_30_days_ago': 100, 'performance_score': 80, 'security_score': 90, 'cves': 1},
    ]
    crates = load_crates(crates_data)
    assert len(crates) == 2
    assert crates[0].name == 'crate1'
