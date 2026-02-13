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


def _norm_key(k: str) -> str:
    """Case-insensitive normalization for resource names."""
    return k.casefold()


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    Base interpretation (same as before):
    - Feasible iff for every resource in `resources`, SUM(request amounts) <= capacity.
    - If any request references a resource not present in `resources`, infeasible (False).
    - Missing resource entries inside a request are treated as 0 (no demand).
    - A request value of None is treated as 0 (null -> no demand).
    - Negative capacities or negative demands are invalid -> ValueError.
    - Non-dict requests, non-dict resources, or non-numeric values -> ValueError.
    - NaN/Inf are invalid -> ValueError.

    New requirements:
    - Resource names are case-insensitive (matched using casefold()).
    - After allocation, there must exist at least one resource type with remaining capacity >= 1.
      (i.e., max_over_resources(capacity - total_demand) >= 1)
      Note: for empty resources + empty requests, still feasible (True), consistent with prior behavior.

    Returns:
        True if feasible, False otherwise.
    """
    # Structural validation
    if not isinstance(resources, dict):
        raise ValueError("resources must be a dict[str, number].")
    if not isinstance(requests, list):
        raise ValueError("requests must be a list[dict[str, number]].")

    # Normalize and validate resources
    norm_resources: Dict[str, float] = {}
    for k, cap in resources.items():
        if not isinstance(k, str):
            raise ValueError("resource names must be strings.")
        nk = _norm_key(k)

        if nk in norm_resources:
            raise ValueError(
                f"duplicate resource name after case-insensitive normalization: '{k}'."
            )

        if cap is None:
            raise ValueError(f"capacity for resource '{k}' cannot be None.")
        if not _is_valid_number(cap):
            raise ValueError(f"capacity for resource '{k}' must be a finite number.")
        if cap < 0:
            raise ValueError(f"capacity for resource '{k}' cannot be negative.")

        norm_resources[nk] = float(cap)

    # Aggregate demand per resource (normalized keys)
    demand: Dict[str, float] = {nk: 0.0 for nk in norm_resources.keys()}

    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            raise ValueError(f"request at index {idx} must be a dict[str, number].")

        for rname, amount in req.items():
            if not isinstance(rname, str):
                raise ValueError(f"resource name in request at index {idx} must be a string.")

            nr = _norm_key(rname)

            # If request references unavailable resource -> infeasible
            if nr not in norm_resources:
                return False

            # Treat None as 0 demand
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

            demand[nr] += float(amount)

            # Early exit if exceeded capacity
            if demand[nr] > norm_resources[nr]:
                return False

    # New rule: at least one resource must have remaining >= 1 after allocation
    if not norm_resources:
        return False

    max_remaining = max(norm_resources[nk] - demand.get(nk, 0.0) for nk in norm_resources.keys())
    if max_remaining < 1.0:
        return False

    return True
