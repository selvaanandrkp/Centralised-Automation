#!/usr/bin/env python3
"""
Config-driven Loan Calculator -- PYTEST VERSION
Tests that read loan parameters from a config file and calculate EMI.
"""
import configparser
import os
import sys
import pytest


def resolve_config_path():
    """Return config path from CLI arg or CONFIG_FILE env var. No silent default."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    env_path = os.environ.get("CONFIG_FILE")
    if env_path:
        return env_path
    return None


def read_loan_config(path):
    """Read loan config file and return principal, annual_rate, years."""
    if not path:
        raise ValueError("No config file provided.")
    
    cfg = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    if not cfg.read(path):
        raise FileNotFoundError(f"Config file not found or unreadable: {path}")
    
    try:
        principal = cfg.getfloat("loan", "principal")
        annual_rate = cfg.getfloat("loan", "annual_rate")
        years = cfg.getint("loan", "years")
    except Exception as e:
        raise ValueError(f"Could not read inputs from config: {e}")
    
    return principal, annual_rate, years


def calculate_emi(principal, annual_rate, years):
    """Calculate monthly EMI based on standard formula."""
    months = years * 12
    monthly_rate = annual_rate / 100.0 / 12.0
    
    if monthly_rate == 0:
        emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)
    
    return emi, months


@pytest.fixture
def loan_config():
    """Fixture to read loan config file and calculate values."""
    config_path = resolve_config_path()
    if not config_path:
        pytest.skip("No config file provided. Set CONFIG_FILE env var or pass as CLI arg.")
    
    principal, annual_rate, years = read_loan_config(config_path)
    emi, months = calculate_emi(principal, annual_rate, years)
    total_payment = emi * months
    total_interest = total_payment - principal
    
    return {
        "path": config_path,
        "principal": principal,
        "annual_rate": annual_rate,
        "years": years,
        "emi": emi,
        "months": months,
        "total_payment": total_payment,
        "total_interest": total_interest
    }


def test_config_file_exists(loan_config):
    """Test that config file was successfully read."""
    assert loan_config["path"] is not None, "Config file path should not be None"
    assert os.path.exists(loan_config["path"]), f"Config file not found: {loan_config['path']}"


def test_loan_inputs_not_empty(loan_config):
    """Test that loan inputs are not empty."""
    assert loan_config["principal"] is not None, "Principal should not be None"
    assert loan_config["annual_rate"] is not None, "Annual rate should not be None"
    assert loan_config["years"] is not None, "Years should not be None"


def test_loan_inputs_are_valid(loan_config):
    """Test that loan inputs are valid numeric values."""
    assert isinstance(loan_config["principal"], (int, float)), f"Principal should be numeric"
    assert isinstance(loan_config["annual_rate"], (int, float)), f"Annual rate should be numeric"
    assert isinstance(loan_config["years"], int), f"Years should be integer"
    
    assert loan_config["principal"] > 0, "Principal must be positive"
    assert loan_config["annual_rate"] >= 0, "Annual rate must be non-negative"
    assert loan_config["years"] > 0, "Years must be positive"


def test_emi_calculation(loan_config):
    """Test EMI calculation."""
    assert loan_config["emi"] is not None, "EMI should not be None"
    assert loan_config["emi"] > 0, "EMI should be positive"
    print(f"EMI Calculation: {loan_config['principal']} @ {loan_config['annual_rate']}% for {loan_config['years']} years = {loan_config['emi']:.2f}/month")


def test_total_payment_calculation(loan_config):
    """Test total payment calculation."""
    assert loan_config["total_payment"] is not None, "Total payment should not be None"
    assert loan_config["total_payment"] >= loan_config["principal"], "Total payment should be >= principal"
    print(f"Total Payment: {loan_config['total_payment']:.2f}")


def test_interest_calculation(loan_config):
    """Test interest (extra amount) calculation."""
    assert loan_config["total_interest"] is not None, "Total interest should not be None"
    assert loan_config["total_interest"] >= 0, "Total interest should be non-negative"
    assert loan_config["total_interest"] == loan_config["total_payment"] - loan_config["principal"], "Interest calculation mismatch"
    print(f"Total Interest: {loan_config['total_interest']:.2f}")


def test_months_calculation(loan_config):
    """Test months calculation from years."""
    expected_months = loan_config["years"] * 12
    assert loan_config["months"] == expected_months, f"Months should be {expected_months}, got {loan_config['months']}"


def test_emi_less_than_principal_per_month(loan_config):
    """Test that monthly EMI is less than total principal (in normal cases)."""
    # For most real loans, monthly EMI should be less than principal divided by months
    assert loan_config["emi"] <= (loan_config["principal"] / loan_config["months"]) * 1.5, "EMI seems unreasonably high"


def test_all_loan_calculations(loan_config):
    """Test all loan calculations together."""
    print("=" * 50)
    print("    CONFIG-DRIVEN LOAN CALCULATOR")
    print("=" * 50)
    print(f"Config file used  : {loan_config['path']}")
    print(f"Principal (borrowed) = {loan_config['principal']:.2f}")
    print(f"Annual rate          = {loan_config['annual_rate']:.2f} %")
    print(f"Years                = {loan_config['years']}  ({loan_config['months']} months)")
    print("-" * 50)
    print(f"Monthly EMI          = {loan_config['emi']:.2f}")
    print(f"Total payment        = {loan_config['total_payment']:.2f}  (principal + interest)")
    print(f"EXTRA amount paid    = {loan_config['total_interest']:.2f}  (interest only, on top of the {loan_config['principal']:.0f} you borrowed)")
    print("=" * 50)
    
    # Assert all values are calculated
    assert loan_config["principal"] is not None
    assert loan_config["emi"] is not None
    assert loan_config["total_payment"] is not None
    assert loan_config["total_interest"] is not None


if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main([__file__, "-v", "-s"])
