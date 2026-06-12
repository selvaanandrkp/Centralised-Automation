#!/usr/bin/env python3
"""
Config-driven Loan Calculator  --  DEMO of dynamic inputs via an UPLOADED config file.

This program has NO hardcoded inputs. It reads all values from a config file.

How it finds the config file (priority order):
  1. Command-line argument : python3 loan_calc.py /path/to/config.ini
  2. Environment variable  : CONFIG_FILE=/path/to/config.ini python3 loan_calc.py

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
        print("  python3 loan_calc.py <config.ini>")
        print("  CONFIG_FILE=<config.ini> python3 loan_calc.py")
        sys.exit(1)

    cfg = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    if not cfg.read(path):
        print(f"ERROR: config file not found or unreadable: {path}")
        sys.exit(1)

    # ---- Read ALL inputs from the config (the dynamic part) ----
    try:
        principal = cfg.getfloat("loan", "principal")
        annual_rate = cfg.getfloat("loan", "annual_rate")
        years = cfg.getint("loan", "years")
    except Exception as e:
        print(f"ERROR: could not read inputs from config: {e}")
        sys.exit(1)

    # ---- Logic: standard monthly EMI calculation ----
    months = years * 12
    monthly_rate = annual_rate / 100.0 / 12.0

    if monthly_rate == 0:
        emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)

    total_payment = emi * months
    total_interest = total_payment - principal

    print("=" * 50)
    print("          CONFIG-DRIVEN LOAN CALCULATOR")
    print("=" * 50)
    print(f"Config file used  : {path}")
    print(f"Principal (borrowed) = {principal:.2f}")
    print(f"Annual rate          = {annual_rate:.2f} %")
    print(f"Years                = {years}  ({months} months)")
    print("-" * 50)
    print(f"Monthly EMI          = {emi:.2f}")
    print(f"Total payment        = {total_payment:.2f}  (principal + interest)")
    print(f"EXTRA amount paid    = {total_interest:.2f}  (interest only, on top of the {principal:.0f} you borrowed)")
    print("=" * 50)


if __name__ == "__main__":
    main()
