# Requirements Document

## Introduction

A visit counter for the calc package: it counts how many times each page is visited, so the team can see which pages are used.

## Glossary

- **VisitCounter**: The class in `calc/visits.py` that counts Visits per page.
- **Visit**: One event reported to the VisitCounter, identified by an `event_id`.
- **System**: The VisitCounter.

## Requirements

### Requirement 1: Count visits

**User Story:** As a team member, I want each page's visits counted, so that I can see which pages are used.

#### Acceptance Criteria

1. WHEN a Visit is recorded for a page, THE System SHALL add one to that page's count.
2. WHILE a page has no recorded Visits, THE System SHALL report a count of 0.

### Requirement 2: Ignore repeated events

**User Story:** As a team member, I want a repeated event ignored, so that a retried event is not counted twice.

#### Acceptance Criteria

1. IF a Visit is recorded with an `event_id` that was already recorded, THEN THE System SHALL leave the count unchanged.
