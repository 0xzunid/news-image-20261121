"""News image entry for 21 November 2026.

Copies the bundled entry.png byte-for-byte to the output directory
(``$MAKEFUN_OUTPUT_DIR``, default ``/output``), then verifies the copy
by comparing its SHA-256 digest against the bundled original and
prints the size and digest.

Stdlib only; no network access.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Return (width, height) from the PNG IHDR chunk, or None."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"

    shutil.copyfile(SOURCE, destination)

    dimensions = png_dimensions(destination)
    if dimensions != (1024, 1024):
        print(f"unexpected PNG dimensions: {dimensions}, expected (1024, 1024)",
              file=sys.stderr)
        return 1

    source_digest = sha256_file(SOURCE)
    copied_digest = sha256_file(destination)
    if copied_digest != source_digest:
        print(f"sha256 mismatch: {copied_digest} != {source_digest}",
              file=sys.stderr)
        return 1

    size = destination.stat().st_size
    print(f"wrote {destination} ({size} bytes)")
    print(f"sha256: {copied_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
