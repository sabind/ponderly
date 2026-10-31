---
type: regex
pattern: '(-{4,}|#[ \t]*Averages|divider|separat|section|heading|header|banner|decorati|comment block|marker)[^\n]*\n(?:(?![ \t]*- file:)[^\n]*\n)*?[ \t]*severity:\s*(blocker|should-fix|nit)'
flags: i
match: not_contains
---
