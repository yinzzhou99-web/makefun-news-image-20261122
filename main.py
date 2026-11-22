"""Entrypoint: copy the committed front page to /output/entry.png.

Standard library only, no network. Deterministic: the same bytes on
every run, because preview.png is fixed in the repository.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    shutil.copyfile(os.path.join(HERE, "preview.png"), target)


if __name__ == "__main__":
    main()
