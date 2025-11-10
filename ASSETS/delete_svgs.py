#!/usr/bin/env python3
"""
Script to delete all .svg files in the current directory.
Use with caution - this will permanently delete files!
Also resets the consent for SVG conversion in the AssetsLibrary.
"""

import os
import sys
import json

def delete_svg_files():
    current_dir = os.getcwd()
    svg_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.svg')]

    if not svg_files:
        print("No .svg files found in the current directory.")
        return

    print(f"Found {len(svg_files)} .svg files:")
    for file in svg_files:
        print(f"  - {file}")

    # Ask for confirmation
    response = input(f"\nAre you sure you want to delete all {len(svg_files)} .svg files? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("Operation cancelled.")
        return

    deleted_count = 0
    for file in svg_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    print(f"\nSuccessfully deleted {deleted_count} .svg files.")

def find_vault_root(start_path=None):
    """Find the Obsidian vault root by looking for .obsidian folder."""
    if start_path is None:
        start_path = os.getcwd()

    current_path = os.path.abspath(start_path)

    # Traverse up the directory tree
    while current_path != os.path.dirname(current_path):  # Stop at root
        obsidian_path = os.path.join(current_path, '.obsidian')
        if os.path.isdir(obsidian_path):
            return current_path
        current_path = os.path.dirname(current_path)

    return None

def reset_consent():
    """Reset the consent file for SVG conversion in AssetsLibrary."""
    vault_root = find_vault_root()
    if not vault_root:
        print("Could not find Obsidian vault root (.obsidian folder not found)")
        return

    consent_path = os.path.join(vault_root, ".datacore", "image-gallery", "consent.json")

    try:
        if os.path.exists(consent_path):
            os.remove(consent_path)
            print(f"Removed consent file: {consent_path}")
        else:
            print(f"Consent file not found: {consent_path}")
    except Exception as e:
        print(f"Error resetting consent: {e}")

if __name__ == "__main__":
    delete_svg_files()
    reset_consent()