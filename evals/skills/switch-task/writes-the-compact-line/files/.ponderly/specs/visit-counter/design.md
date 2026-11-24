# Design Document

## Overview

`VisitCounter` in `calc/visits.py` keeps a count per page and the set of `event_id` values it has seen.

## Components and Interfaces

### VisitCounter

| Operation | Input | Output | Requirements |
|-----------|-------|--------|--------------|
| `record(page, event_id)` | a page name and an event id | none | 1.1, 2.1 |
| `count(page)` | a page name | the number of Visits, 0 when none | 1.2 |

Key decision: count with `calc.ops.add`. The counter adds one with `calc.ops.add` rather than `+`, so the arithmetic stays in one place.

Key decision: skip a repeated `event_id`. `record` returns without counting when the `event_id` was already recorded, so a retried event is counted once.

## Error Handling

| Condition | Behavior | Requirements |
|-----------|----------|--------------|
| Repeated `event_id` | Skip it; change nothing | 2.1 |
