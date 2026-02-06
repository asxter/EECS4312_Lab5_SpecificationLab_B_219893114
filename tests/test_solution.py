"""
Public test suite for the resource allocation feasibility exercise.

Run:
pytest test_solution.py
"""

from solution2 import is_allocation_feasible
import pytest
import math


def test_basic_feasible_single_resource():
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 3}]
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_infeasible_one_overloaded():
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_resource_in_availability():
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_non_dict_request_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # malformed request
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# -------------------------
# Additional student tests
# -------------------------

def test_empty_requests_is_feasible():
    resources = {'cpu': 0, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_with_empty_requests_is_feasible():
    resources = {}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_with_positive_request_is_infeasible():
    resources = {}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_entry_in_request_treated_as_zero():
    # request doesn't mention 'mem' => treated as 0 for mem, still feasible
    resources = {'cpu': 5, 'mem': 5}
    requests = [{'cpu': 2}, {'mem': 5}]
    assert is_allocation_feasible(resources, requests) is True


def test_none_amount_in_request_treated_as_zero():
    resources = {'cpu': 5}
    requests = [{'cpu': None}, {'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_capacity_raises():
    resources = {'cpu': -1}
    requests = [{'cpu': 0}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_request_amount_raises():
    resources = {'cpu': 10}
    requests = [{'cpu': -2}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_capacity_raises():
    resources = {'cpu': "10"}  # invalid type
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_request_amount_raises():
    resources = {'cpu': 10}
    requests = [{'cpu': "2"}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_nan_or_inf_raises():
    resources = {'cpu': 10}
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, [{'cpu': math.nan}])
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, [{'cpu': math.inf}])


def test_float_amounts_supported():
    resources = {'cpu': 1.5}
    requests = [{'cpu': 0.5}, {'cpu': 1.0}]
    assert is_allocation_feasible(resources, requests) is True


def test_resource_names_must_be_strings():
    resources = {123: 10}  # invalid key type
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_requests_must_be_list():
    resources = {'cpu': 10}
    requests = {'cpu': 1}  # not a list
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)
