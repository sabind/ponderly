# Implementation Plan

## Overview

Build `VisitCounter` in `calc/visits.py`, counting with `calc.ops.add` and skipping a repeated `event_id`.

## Tasks

- [ ] 1. Implement VisitCounter
  - [ ] 1.1 Add `calc/visits.py` with `record` and `count`, counting with `calc.ops.add`
    - _Requirements: 1.1, 1.2_
  - [ ] 1.2 Skip a repeated `event_id` in `record`
    - _Requirements: 2.1_

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] }
  ]
}
```
