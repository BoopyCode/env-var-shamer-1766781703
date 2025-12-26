#!/usr/bin/env python3
"""ENV Var Shamer - Because your secrets deserve better than hardcoding."""

import re
import sys
from pathlib import Path

# The usual suspects - patterns that scream "I should be an env var!"
SUSPICIOUS_PATTERNS = [
    r'\b(api[_-]?key|secret|password|token|auth)\s*[=:]\s*["\'][^"\']{8,}["\']',  # Long strings after key-ish names
    r'\b[A-Z0-9_]{10,}\s*[=:]\s*["\'][^"\']+["\']',  # ALL_CAPS_SUSPICIOUS_THINGS
    r'\b(https?:\/\/)[^"\'\s]+@',  # URLs with credentials (shame!)
    r'\b(aws_|azure_|google_)[a-z_]*\s*[=:]\s*["\'][^"\']{5,}["\']',  # Cloud shame
]

# Files we should probably ignore (unless you're extra naughty)
IGNORE_EXTENSIONS = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip'}

def shame_file(filepath):
    """Publicly shame a file for its hardcoding sins."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        
        shame_found = False
        for i, line in enumerate(lines, 1):
            for pattern in SUSPICIOUS_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    if not shame_found:
                        print(f"\n🔴 {filepath} is blushing:")
                        shame_found = True
                    print(f"   Line {i}: {line.strip()[:60]}...")
                    print(f"     ^ Your secret wants to be $SECRET, not a string!")
        
        return shame_found
    except Exception as e:
        print(f"Couldn't read {filepath}: {e}")
        return False

def main():
    """Shame all the files!"""
    if len(sys.argv) < 2:
        print("Usage: python env_shamer.py <directory>")
        print("Example: python env_shamer.py .  # Shame current dir")
        sys.exit(1)
    
    target_dir = Path(sys.argv[1])
    if not target_dir.exists():
        print(f"Directory '{target_dir}' not found. Can't shame what doesn't exist!")
        sys.exit(1)
    
    print("🔍 Scanning for hardcoded secrets (the shame begins)...")
    
    any_shame = False
    for filepath in target_dir.rglob('*'):
        if filepath.is_file() and filepath.suffix not in IGNORE_EXTENSIONS:
            if shame_file(filepath):
                any_shame = True
    
    if any_shame:
        print("\n💀 Found hardcoded values! Use environment variables like a grown-up.")
        print("   Your future self (and security team) will thank you!")
        sys.exit(1)
    else:
        print("\n✅ No shame detected! Your code is environmentally conscious!")

if __name__ == "__main__":
    main()
