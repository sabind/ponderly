# clamp

A tiny module that keeps a number inside a range. Run the tests with
`python3 -m unittest`.

## Command line

Clamp a value from the shell, giving the upper bound with `--high`:

```sh
python3 -m clamp.cli 150 --high 120
```

This prints `120.0`.
