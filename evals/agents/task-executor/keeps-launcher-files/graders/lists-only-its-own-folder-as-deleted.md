---
type: regex
pattern: 'deleted:(?:(?!unsure:)[\s\S])*?\n[ \t]*[-*][ \t]+`?(?!\S*scratch/executor-own(?:[/`:,)]|\s|$))\S'
match: not_contains
---
