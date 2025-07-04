#!/usr/bin/env python3
"""
Release script for spy-bot
Automates the release process with version bumping and tagging
"""

import re
import subprocess  # nosec
import sys


def run_command(command, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, shell=True, check=check, capture_output=True, text=True
        )  # nosec
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def get_current_version():
    """Get current version from pyproject.toml"""
    with open("pyproject.toml", "r") as f:
        content = f.read()
        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def update_version(new_version):
    """Update version in pyproject.toml"""
    with open("pyproject.toml", "r") as f:
        content = f.read()

    content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)

    with open("pyproject.toml", "w") as f:
        f.write(content)

    print(f"Updated version to {new_version}")


def bump_version(version_type):
    """Bump version based on type (major, minor, patch)"""
    current = get_current_version()
    major, minor, patch = map(int, current.split("."))

    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        raise ValueError("Version type must be major, minor, or patch")

    return f"{major}.{minor}.{patch}"


def create_release(version_type):
    """Create a new release"""
    print("🚀 Starting release process...")

    # Check if working directory is clean
    status = run_command("git status --porcelain")
    if status:
        print("❌ Working directory is not clean. Please commit or stash changes.")
        sys.exit(1)

    # Bump version
    new_version = bump_version(version_type)
    print(f"📦 Bumping version to {new_version}")
    update_version(new_version)

    # Run pre-commit hooks
    print("🔍 Running pre-commit hooks...")
    run_command("pre-commit run --all-files")

    # Commit version bump
    print("💾 Committing version bump...")
    run_command("git add pyproject.toml")
    run_command(f'git commit -m "chore: bump version to {new_version}"')

    # Create tag
    print("🏷️ Creating tag...")
    run_command(f'git tag -a v{new_version} -m "Release v{new_version}"')

    # Push changes and tag
    print("📤 Pushing changes and tag...")
    run_command("git push origin main")
    run_command(f"git push origin v{new_version}")

    print(f"✅ Release v{new_version} created successfully!")
    print(f"🎉 You can now create a release on GitHub for tag v{new_version}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/release.py <major|minor|patch>")
        sys.exit(1)

    version_type = sys.argv[1]
    if version_type not in ["major", "minor", "patch"]:
        print("Version type must be major, minor, or patch")
        sys.exit(1)

    create_release(version_type)


if __name__ == "__main__":
    main()
