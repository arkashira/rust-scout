import json
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Crate:
    name: str
    stars: int
    performance_score: float
    security_score: float

def calculate_star_trend_score(stars_30_days_ago, current_stars):
    if stars_30_days_ago == 0:
        return 0
    return ((current_stars - stars_30_days_ago) / stars_30_days_ago) * 100

def calculate_performance_score(benchmark_score):
    if benchmark_score >= 90:
        return 100
    else:
        return benchmark_score

def calculate_security_score(cves):
    return max(0, 100 - (cves * 10))

def calculate_composite_score(star_trend_score, performance_score, security_score):
    return (star_trend_score * 0.4) + (performance_score * 0.35) + (security_score * 0.25)

def rank_crates(crates):
    ranked_crates = []
    for crate in crates:
        star_trend_score = calculate_star_trend_score(crate.stars_30_days_ago, crate.stars)
        performance_score = calculate_performance_score(crate.performance_score)
        security_score = calculate_security_score(crate.cves)
        composite_score = calculate_composite_score(star_trend_score, performance_score, security_score)
        ranked_crates.append((crate.name, composite_score))
    return sorted(ranked_crates, key=lambda x: x[1], reverse=True)

def load_crates(data):
    crates = []
    for crate_data in data:
        crate = Crate(
            name=crate_data['name'],
            stars=crate_data['stars'],
            performance_score=crate_data['performance_score'],
            security_score=crate_data['security_score']
        )
        crate.stars_30_days_ago = crate_data['stars_30_days_ago']
        crate.cves = crate_data['cves']
        crates.append(crate)
    return crates
