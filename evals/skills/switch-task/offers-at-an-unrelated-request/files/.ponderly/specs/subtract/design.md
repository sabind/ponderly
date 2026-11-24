# Design Document

## Overview

`subtract(a, b)` is a plain function in `calc/ops.py`, beside `add` and `multiply`.

## Components and Interfaces

| Operation | Input | Output | Requirements |
|-----------|-------|--------|--------------|
| `subtract(a, b)` | two numbers | `a - b` | 1.1 |

## Testing Strategy

One example test in `tests/test_ops.py` checks that `subtract(5, 3)` returns 2.
