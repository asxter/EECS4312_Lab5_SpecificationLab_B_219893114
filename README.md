# Resource Allocation Feasibility

## Student
Name: Anirudh Sundar  
Student ID: 219893114

---

## System Description

This module determines whether a collection of resource requests can be satisfied
given fixed resource capacities.

The function under test:

is_allocation_feasible(resources, requests) -> bool
evaluates whether an allocation is possible while enforcing safety,
consistency, and validation rules.

---

## Interpretation of Feasibility

An allocation is feasible if **all** of the following hold:

1. For every resource, the total requested amount does not exceed capacity.
2. Requests may omit resources → treated as zero demand.
3. A request value of `None` is treated as zero demand.
4. Resource matching is **case-insensitive**.
5. After allocation, **at least one resource must have ≥ 1 full unit remaining**.

If no resource has at least one complete unit remaining, the allocation fails.

---

## Invariants

The system maintains these invariants:

- Capacities are finite real numbers.
- Capacities are non-negative.
- Demands are finite real numbers.
- Demands are non-negative.
- Resource identifiers are strings.
- No duplicate resource names after case normalization.
- Unknown resources in a request make the allocation infeasible.

---

## Failure Modes

The function returns **False** when:

- Any request references a missing resource.
- The total demand exceeds capacity.
- After allocation, every resource has less than one unit remaining.
- There are no resources at all (cannot leave ≥ 1).

The function raises **ValueError** when:

- Structures are malformed (wrong types).
- Keys are not strings.
- Numeric values are invalid.
- Values are negative.
- NaN or infinite numbers appear.
- Case-insensitive duplicates exist in resource definitions.

---

## Examples

| Resources | Requests | Remaining | Result |
|----------|----------|-----------|--------|
| {cpu:10} | {cpu:9} | 1 | True |
| {cpu:10} | {cpu:10} | 0 | False |
| {cpu:10,gpu:10} | {cpu:10,gpu:9} | 0,1 | True |
| {cpu:10,gpu:10} | {cpu:9.8,gpu:9.2} | 0.2,0.8 | False |
| {} | {} | none | False |

---

## Test Coverage

The test suite verifies:

- Normal successful allocations  
- Boundary conditions around 1 unit remaining  
- Aggregation across multiple requests  
- Case-insensitive behavior  
- Missing resources  
- Structural validation  
- Invalid numeric types  
- NaN / infinity rejection  
- Negative values  
- Duplicate normalized keys  

---

## Complexity

Let:
- `R` = number of resources  
- `N` = number of requests  
- `K` = average resources per request  

Time complexity: **O(N × K)**  
Space complexity: **O(R)**

---

## Notes

The implementation uses early exit on overload for efficiency and
normalizes resource identifiers using `casefold()` to ensure robust matching.
