---
type: llm
focus: { source: file, path: calc/report.py }
---

The file shown is `calc/report.py` after a session was asked to add `customer_report(path)`, which loads orders, leaves out refunded and unknown ones, totals each customer's paid cents, sorts the customers by total, largest first and ties by name, and formats one line per customer such as `Ada: $12.50` and a last `Total:` line.

PASS if the work is split into functions that each do one job their name says, such as keeping the paid orders, totalling cents per customer, ordering the customers, or formatting an amount or a line, and `customer_report` mostly calls them in sequence. At least two of the jobs it was asked for live in their own named function.
FAIL if `customer_report` does the filtering, totalling, sorting and formatting in its own body, with at most one small helper beside it, if a helper does several of those jobs under a name that does not say so, or if the file is missing or holds no `customer_report`.
