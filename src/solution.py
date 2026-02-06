"""
Stub file for the is_allocation_feasible exercise.

Implement the function `is_allocation_feasible` to determine whether a set of resource requests
can be satisfied given limited capacities.
"""

from __future__ import annotations

from typing import Dict, List, Union
import math

Number = Union[int, float]


def _is_valid_number(x) -> bool:
    """True for int/float (not bool), finite, and not NaN."""
    if isinstance(x, bool):
        return False
    if not isinstance(x, (int, float)):
        return False
    return math.isfinite(x)


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    Interpretation used (matches public tests):
    - Allocation is feasible iff, for every resource key in `resources`,
      the SUM of all request amounts for that resource <= capacity.
    - If any request references a resource not present in `resources`, infeasible (False).
    - Missing resource entries inside a request are treated as 0 (no demand).
    - A request value of None is treated as 0 (null -> no demand), per user contingency request.
    - Negative capacities or negative demands are invalid -> ValueError.
    - Non-dict requests, non-dict resources, or non-numeric values -> ValueError.
    - NaN/Inf are invalid -> ValueError.

    Returns:
        True if feasible, False otherwise.
    """
    # Structural validation
    if not isinstance(resources, dict):
        raise ValueError("resources must be a dict[str, number].")
    if not isinstance(requests, list):
        raise ValueError("requests must be a list[dict[str, number]].")

    # Validate resources: keys must be str, values must be finite numbers >= 0
    for k, cap in resources.items():
        if not isinstance(k, str):
            raise ValueError("resource names must be strings.")
        if cap is None:
            raise ValueError(f"capacity for resource '{k}' cannot be None.")
        if not _is_valid_number(cap):
            raise ValueError(f"capacity for resource '{k}' must be a finite number.")
        if cap < 0:
            raise ValueError(f"capacity for resource '{k}' cannot be negative.")

    # Aggregate demand per resource
    demand: Dict[str, float] = {k: 0.0 for k in resources.keys()}

    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            raise ValueError(f"request at index {idx} must be a dict[str, number].")

        for rname, amount in req.items():
            if not isinstance(rname, str):
                raise ValueError(f"resource name in request at index {idx} must be a string.")

            # If request references unavailable resource -> infeasible
            if rname not in resources:
                return False

            # "null" contingency: treat None as 0 demand
            if amount is None:
                continue

            if not _is_valid_number(amount):
                raise ValueError(
                    f"amount for resource '{rname}' in request at index {idx} must be a finite number."
                )
            if amount < 0:
                raise ValueError(
                    f"amount for resource '{rname}' in request at index {idx} cannot be negative."
                )

            demand[rname] += float(amount)

            # Early exit if already exceeded
            if demand[rname] > float(resources[rname]):
                return False

    return True
