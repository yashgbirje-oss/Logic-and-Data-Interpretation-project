import streamlit as st

def validate_number(value, name, min_val=None, max_val=None):
    try:
        val = float(value)
        if min_val is not None and val < min_val:
            return False, f"{name} cannot be less than {min_val}."
        if max_val is not None and val > max_val:
            return False, f"{name} cannot be greater than {max_val}."
        return True, val
    except ValueError:
        return False, f"{name} must be a valid number."

def validate_int(value, name, min_val=None, max_val=None):
    try:
        val = int(value)
        if min_val is not None and val < min_val:
            return False, f"{name} cannot be less than {min_val}."
        if max_val is not None and val > max_val:
            return False, f"{name} cannot be greater than {max_val}."
        return True, val
    except ValueError:
        return False, f"{name} must be a valid integer."
