"""
test_solution.py

Run:
pytest -q
"""

import math
import pytest

from solution2 import is_allocation_feasible


# ==================================================
# Core feasibility + >=1 remaining rule
# ==================================================

def test_single_resource_pass_exactly_one_left():
    # resources={'cpu':10}, requests=[{'cpu':9}] -> remaining=1
    # PASS: at least one resource has >= 1 remaining
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 9}]) is True


def test_single_resource_fail_zero_left():
    # resources={'cpu':10}, requests=[{'cpu':10}] -> remaining=0
    # FAIL: no resource has >= 1 remaining
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 10}]) is False


def test_single_resource_fail_less_than_one_left():
    # resources={'cpu':10}, requests=[{'cpu':9.8}] -> remaining=0.2
    # FAIL: remaining < 1
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 9.8}]) is False


def test_two_resources_pass_if_one_has_one_left():
    # cpu=0, gpu=1
    # PASS: gpu has >= 1 remaining
    assert is_allocation_feasible(
        {"cpu": 10, "gpu": 10},
        [{"cpu": 10, "gpu": 9}]
    ) is True


def test_two_resources_fail_if_all_zero():
    # cpu=0, gpu=0
    # FAIL: none >= 1
    assert is_allocation_feasible(
        {"cpu": 10, "gpu": 10},
        [{"cpu": 10, "gpu": 10}]
    ) is False


def test_two_resources_pass_float_mix():
    # cpu=0.2, gpu=1.2
    # PASS: gpu >= 1
    assert is_allocation_feasible(
        {"cpu": 10, "gpu": 10},
        [{"cpu": 9.8, "gpu": 8.8}]
    ) is True


def test_two_resources_fail_all_less_than_one():
    # cpu=0.2, gpu=0.8
    # FAIL: no resource >= 1
    assert is_allocation_feasible(
        {"cpu": 10, "gpu": 10},
        [{"cpu": 9.8, "gpu": 9.2}]
    ) is False


def test_aggregate_requests_pass():
    # total=9 -> remaining=1
    # PASS: >=1 remaining
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 3}, {"cpu": 6}]) is True


def test_aggregate_requests_fail_over_capacity():
    # total=11 > capacity
    # FAIL: exceeds capacity
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 3}, {"cpu": 8}]) is False


# ==================================================
# Case-insensitive behavior
# ==================================================

def test_case_insensitive_match():
    # resources={'CPU':10}, requests={'cpu':9}
    # PASS: same resource after normalization + remaining=1
    assert is_allocation_feasible({"CPU": 10}, [{"cpu": 9}]) is True


def test_case_insensitive_unknown():
    # request references 'gpu' not in resources
    # FAIL: missing resource
    assert is_allocation_feasible({"CPU": 10}, [{"gpu": 1}]) is False


def test_duplicate_after_casefold_raises():
    # 'CPU' and 'cpu' collide
    # FAIL: ambiguous resource definition -> ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"CPU": 10, "cpu": 5}, [])


# ==================================================
# None / missing entries
# ==================================================

def test_none_treated_as_zero():
    # total=9 -> remaining=1
    # PASS: None counted as zero demand
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": None}, {"cpu": 9}]) is True


def test_missing_entry_zero():
    # cpu=0, gpu=10
    # PASS: gpu >= 1
    assert is_allocation_feasible(
        {"cpu": 10, "gpu": 10},
        [{"cpu": 10}]
    ) is True


# ==================================================
# Empty structures (STRICT RULE)
# ==================================================

def test_empty_resources_empty_requests_fail():
    # no resources exist
    # FAIL: impossible to have >= 1 remaining
    assert is_allocation_feasible({}, []) is False


def test_empty_resources_with_request_fail():
    # unknown resource
    # FAIL: resource missing
    assert is_allocation_feasible({}, [{"cpu": 1}]) is False


def test_empty_requests_pass_if_any_cap_ge_one():
    # remaining 0.5, 1.0
    # PASS: gpu >= 1
    assert is_allocation_feasible({"cpu": 0.5, "gpu": 1.0}, []) is True


def test_empty_requests_fail_if_all_lt_one():
    # remaining 0.5, 0.9
    # FAIL: none >= 1
    assert is_allocation_feasible({"cpu": 0.5, "gpu": 0.9}, []) is False


# ==================================================
# Structural validation
# ==================================================

def test_resources_not_dict():
    # invalid type
    # FAIL: structural error -> ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible([("cpu", 10)], [])


def test_requests_not_list():
    # invalid type
    # FAIL: structural error -> ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, {"cpu": 1})


def test_request_not_dict():
    # malformed request entry
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": 1}, ["cpu", 2]])


# ==================================================
# Resource validation
# ==================================================

def test_resource_key_not_string():
    # invalid key
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({1: 10}, [])


def test_capacity_none():
    # invalid capacity
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": None}, [])


def test_capacity_negative():
    # invalid capacity
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": -1}, [])


def test_capacity_non_numeric():
    # invalid type
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": "10"}, [])


def test_capacity_nan_inf():
    # invalid numeric
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": math.nan}, [])
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": math.inf}, [])


def test_capacity_bool_rejected():
    # bool forbidden
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": True}, [])


# ==================================================
# Request validation
# ==================================================

def test_request_key_not_string():
    # invalid key
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{1: 2}])


def test_request_negative_amount():
    # invalid demand
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": -2}])


def test_request_non_numeric():
    # invalid type
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": "2"}])


def test_request_nan_inf():
    # invalid numeric
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": math.nan}])
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": math.inf}])


def test_request_bool_rejected():
    # bool forbidden
    # FAIL: ValueError
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": False}])
