#!/usr/bin/env python3
"""Rename the Planet — writes one entry line to /output/entry.txt.

Deterministic: the same entry is written on every run.
"""

import hashlib
import os
import sys

ENTRY = (
    'Uranus, "The Napper": tipped 98\u00b0 on its side, each season lasts '
    "21 years, and it still won't get out of bed."
)


def verify(path: str) -> bool:
    """Read the written entry back from disk and check it is valid.

    Checks: valid UTF-8, 1-200 characters, exactly one line with no
    newline characters, no control characters, and a canonical sha256
    matching the intended entry bytes.
    """
    with open(path, "rb") as f:
        data = f.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if not 1 <= len(text) <= 200:
        return False
    if "\n" in text or "\r" in text:
        return False
    if any(ord(ch) < 0x20 for ch in text):
        return False
    return hashlib.sha256(data).hexdigest() == hashlib.sha256(
        ENTRY.encode("utf-8")
    ).hexdigest()


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    if not verify(path):
        sys.stderr.write("verification failed: entry.txt is invalid\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
