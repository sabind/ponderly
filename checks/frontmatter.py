"""Read a skill's or agent's frontmatter the way YAML does, for the checks that need its values.

There is no YAML parser in the standard library. This reads the subset the
plugin's frontmatter uses: top-level ``key: value`` pairs whose values are plain,
quoted or block scalars, on one line or several.
"""


def read_frontmatter(path):
    """Return the top-level ``key: value`` pairs between the leading ``---`` fences, or None if there is no block.

    Each value is the scalar YAML reads, across every line it spans: a block scalar
    (``|`` or ``>``), a quoted value or a plain value continued on indented lines.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    entries = {}
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            return {name: scalar_value(head, rest) for name, (head, rest) in entries.items()}
        starts_a_key = line[:1].strip() and ":" in line
        if starts_a_key:
            name, _, head = line.partition(":")
            key = name.strip()
            entries[key] = (head.strip(), [])
        elif key is not None:
            entries[key][1].append(line)
    return None


def scalar_value(head, continuation):
    """Return the scalar YAML reads from a key's ``head``, the text after its colon, and the lines below it."""
    if head[:1] in ("|", ">"):
        return block_scalar(head, continuation)
    text = fold([head] + [line.strip() for line in continuation])
    if len(text) >= 2 and text[0] == text[-1] == "'":
        return text[1:-1].replace("''", "'")
    if len(text) >= 2 and text[0] == text[-1] == '"':
        return text[1:-1]
    return text


def block_scalar(indicator, continuation):
    """Return a ``|`` or ``>`` block scalar's value, with its ``-`` or ``+`` chomping marker applied."""
    trailing_blank_lines = 0
    while continuation and not continuation[-1].strip():
        continuation = continuation[:-1]
        trailing_blank_lines += 1
    indents = [len(line) - len(line.lstrip()) for line in continuation if line.strip()]
    indent = min(indents, default=0)
    content = [line[indent:] for line in continuation]
    body = "\n".join(content) if indicator[0] == "|" else fold(content)
    if not body or "-" in indicator:
        return body
    if "+" in indicator:
        return body + "\n" * (1 + trailing_blank_lines)
    return body + "\n"


def fold(lines):
    """Join lines as YAML folds them: adjacent lines with a space, each blank line as a line break."""
    folded = ""
    for line in lines:
        if not line:
            folded += "\n"
        elif folded and not folded.endswith("\n"):
            folded += " " + line
        else:
            folded += line
    return folded
