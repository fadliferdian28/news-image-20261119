#!/usr/bin/env python3
"""news-image-20261119 entry runner (standard library only).

Copies the pre-rendered entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR
(or the script's own directory when unset, for local runs) and verifies
the copy with a sha256 comparison. No image work happens here: the
front page was rendered offline by the build script.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not SRC.is_file():
        print(f"missing source image: {SRC}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    # When MAKEFUN_OUTPUT_DIR is set, the copy goes there and never into
    # this repo directory (the grader mounts the repo read-only).
    dest_dir = Path(out_dir) if out_dir else HERE
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    if dest.resolve() != SRC.resolve():
        shutil.copyfile(SRC, dest)
    src_hash = sha256_of(SRC)
    dst_hash = sha256_of(dest)
    if src_hash != dst_hash:
        print(f"hash mismatch: {src_hash} != {dst_hash}", file=sys.stderr)
        return 1
    print(f"wrote {dest}")
    print(f"sha256 {dst_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
