import json
from dataclasses import dataclass
from typing import List

@dataclass
class TestResult:
    test_name: str
    passed: bool
    message: str

class RustScout:
    def __init__(self, code_coverage: float, e2e_tests: List[str]):
        self.code_coverage = code_coverage
        self.e2e_tests = e2e_tests
        self.test_results = []

    def run_unit_tests(self) -> List[TestResult]:
        # Simulate running unit tests
        results = []
        for i in range(10):
            results.append(TestResult(f"unit_test_{i}", True, "Passed"))
        self.test_results.extend(results)
        return results

    def run_e2e_tests(self) -> List[TestResult]:
        # Simulate running e2e tests
        results = []
        for test in self.e2e_tests:
            results.append(TestResult(test, True, "Passed"))
        self.test_results.extend(results)
        return results

    def check_code_coverage(self) -> bool:
        return self.code_coverage >= 0.8

    def check_e2e_tests(self) -> bool:
        required_tests = ["search", "detail_page", "subscription_flow"]
        return all(test in self.e2e_tests for test in required_tests)

    def run_all_tests(self) -> List[TestResult]:
        self.test_results = []
        unit_test_results = self.run_unit_tests()
        e2e_test_results = self.run_e2e_tests()
        return self.test_results

    def check_all_tests_passed(self) -> bool:
        return all(result.passed for result in self.test_results)
