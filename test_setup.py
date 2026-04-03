#!/usr/bin/env python3
"""
test_setup.py
Improved environment validation script for the warm-up assignment
"""

import sys
import importlib
import subprocess
import platform
import shutil
import os

MIN_PYTHON = (3, 9)

def print_header(title):
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")

def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version >= MIN_PYTHON:
        print("PASS: Python version is compatible")
        return True
    else:
        print(f"FAIL: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required")
        return False

def get_pip_command():
    """Find a working pip command"""
    for cmd in ["pip", "pip3", sys.executable + " -m pip"]:
        if isinstance(cmd, str) and shutil.which(cmd.split()[0]):
            return cmd
    return None

def check_required_packages():
    """Check if all required packages are installed"""
    required_packages = {
        'flask': 'flask',
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'nltk': 'nltk',
        'dotenv': 'python-dotenv'
    }

    print("\nChecking required packages...")
    all_installed = True
    missing = []

    for module, pip_name in required_packages.items():
        try:
            importlib.import_module(module)
            print(f"PASS: {module}")
        except ImportError:
            print(f"FAIL: {module}")
            missing.append(pip_name)
            all_installed = False

    if missing:
        pip_cmd = get_pip_command() or "pip"
        print("\nInstall missing packages with:")
        print(f"{pip_cmd} install {' '.join(missing)}")

    return all_installed

def check_environment():
    """Detect environment type"""
    print("\nEnvironment Info:")
    print(f"Platform: {platform.system()} {platform.release()}")

    if os.getenv("CODESPACE_NAME"):
        print("Running in GitHub Codespaces")
    else:
        print("Running locally")

    return True

def test_basic_functionality():
    """Test basic functionality of key libraries"""
    print("\nTesting basic functionality...")

    try:
        import requests
        from flask import Flask

        app = Flask(__name__)

        text = "Hello, World! This is a test."
        words = text.lower().split()

        assert len(words) > 0

        print("PASS: requests working")
        print("PASS: Flask app creation working")
        print(f"PASS: Text processing working ({len(words)} words)")

        return True

    except Exception as e:
        print(f"FAIL: Functionality test failed:\n   {e}")
        return False

def test_project_gutenberg_access():
    """Test access to Project Gutenberg"""
    print("\nTesting Project Gutenberg access...")

    try:
        import requests

        url = "https://www.gutenberg.org/files/1342/1342-0.txt"
        response = requests.head(url, timeout=10)

        if response.ok:
            print("PASS: Project Gutenberg reachable")
            return True
        else:
            print(f"WARNING: Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        print("WARNING: Timeout - network may be slow")
        return False
    except requests.exceptions.RequestException as e:
        print(f"WARNING: Network error: {e}")
        return False

def run_tests():
    """Run all tests and summarize results"""
    print_header("CSE 510 Warm-Up - Environment Setup Test")

    tests = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Environment", check_environment),
        ("Basic Functionality", test_basic_functionality),
        ("Project Gutenberg Access", test_project_gutenberg_access)
    ]

    results = []

    for name, test in tests:
        print(f"\n--- {name} ---")
        result = test()
        results.append((name, result))

    print_header("SETUP TEST SUMMARY")

    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{status:<6} {name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("ENVIRONMENT SETUP COMPLETE")
        print("You are ready to start the assignment.\n")
    else:
        print("SETUP INCOMPLETE")
        print("Fix the issues above before continuing.\n")

    return all_passed

def main():
    success = run_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()