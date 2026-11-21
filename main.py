#!/usr/bin/env python3
"""Entry for make.fun news-image-20261121: sum up 21 November's world news
in one image.

The deliverable is entry.png, a 1024x1024 newspaper front page drawn with
Pillow (crisp baked-in headline text, no AI-image text garbling). It sums up
Saturday 21 November 2026: Russian missiles and a suspected drone crashing
in Poland during Moscow's biggest attack on Ukraine this year; Wall Street
sliding into correction as the AI trade melts down; Russia's biggest barrage
of the year on Ukraine hours after the Shenzhen summit; the UK and EU sealing
food, carbon and youth-mobility deals; Erasca's ERAS-0015 pill shrinking
pancreatic tumours in an early trial; plus the Palisades Fire conviction,
Cyclone Akvan, Voyager 1's one-light-day milestone and the US–Iran standoff
in one "Also today" strip.

This script just copies the bundled image to the grader's output directory.
It is stdlib only and makes no network calls.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy landed byte for byte: a truncated or partial image
    # would silently grade as a broken front page.
    if sha256_of(src) != sha256_of(dst):
        print("error: copied entry.png does not match the bundled image",
              file=sys.stderr)
        return 1
    print("wrote", dst, "(%d bytes, sha256 %s)"
          % (os.path.getsize(dst), sha256_of(dst)))


if __name__ == "__main__":
    sys.exit(main())
