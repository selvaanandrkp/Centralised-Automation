#!/usr/bin/env python3
"""
Config-driven Calculator  --  DEMO of dynamic inputs via an UPLOADED config file.

This program has NO hardcoded inputs. It reads a and b from a config file.

How it finds the config file (priority order):
  1. Command-line argument : python3 calc_dynamic.py /path/to/config.ini
  2. Environment variable  : CONFIG_FILE=/path/to/config.ini python3 calc_dynamic.py

If NO config is provided, the program ERRORS OUT on purpose.
This proves the inputs truly came from the uploaded file (no hidden default).

In Jenkins we feed the UPLOADED file via the CONFIG_FILE env var.
"""
import configparser
import os
import sys


def resolve_config_path():
    """Return config path from CLI arg or CONFIG_FILE env var. No silent default."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    env_path = os.environ.get("CONFIG_FILE")
    if env_path:
        return env_path
    return None


def main():
    path = resolve_config_path()

    if not path:
        print("ERROR: no config file provided.")
        print("This program needs a config file. Pass it one of these ways:")
        print("  python3 calc_dynamic.py <config.ini>")
        print("  CONFIG_FILE=<config.ini> python3 calc_dynamic.py")
        sys.exit(1)

    cfg = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    if not cfg.read(path):
        print(f"ERROR: config file not found or unreadable: {path}")
        sys.exit(1)

    # ---- Read ALL inputs from the config (the dynamic part) ----
    try:
        a = cfg.getfloat("inputs", "a")
        b = cfg.getfloat("inputs", "b")
    except Exception as e:
        print(f"ERROR: could not read inputs from config: {e}")
        sys.exit(1)

    # ---- Logic ----
    print("=" * 40)
    print("        CONFIG-DRIVEN CALCULATOR")
    print("=" * 40)
    print(f"Config file used : {path}")
    print(f"a = {a}")
    print(f"b = {b}")
    print("-" * 40)
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    if b != 0:
        print(f"a / b = {a / b}")
    else:
        print("a / b = cannot divide by zero")
    print("=" * 40)


if __name__ == "__main__":
    main()
