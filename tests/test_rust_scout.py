from rust_scout import RustScout, TestResult

def test_run_unit_tests():
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    results = rust_scout.run_unit_tests()
    assert len(results) == 10
    assert all(result.passed for result in results)

def test_run_e2e_tests():
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    results = rust_scout.run_e2e_tests()
    assert len(results) == 3
    assert all(result.passed for result in results)

def test_check_code_coverage():
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    assert rust_scout.check_code_coverage()
    rust_scout = RustScout(0.7, ["search", "detail_page", "subscription_flow"])
    assert not rust_scout.check_code_coverage()

def test_check_e2e_tests():
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    assert rust_scout.check_e2e_tests()
    rust_scout = RustScout(0.8, ["search", "detail_page"])
    assert not rust_scout.check_e2e_tests()

def test_run_all_tests():
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    results = rust_scout.run_all_tests()
    assert len(results) == 13
    assert all(result.passed for result in results)

def test_check_all_tests_passed():
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    assert rust_scout.check_all_tests_passed()
    rust_scout = RustScout(0.8, ["search", "detail_page", "subscription_flow"])
    rust_scout.e2e_tests[0] = "failed_test"
    rust_scout.run_all_tests()
    rust_scout.test_results[0].passed = False
    assert not rust_scout.check_all_tests_passed()
