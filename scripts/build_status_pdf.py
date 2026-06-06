"""Build the status PDF from docs/STATUS_REPORT.md.

Embeds the report images as base64 data URIs (so the make-pdf renderer does not
need local file access), then renders via the gstack make-pdf binary. Regenerate
the images first: validate_chen2020.py, run_demo.py, make_diagrams.py.
"""

import base64
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
md = (ROOT / "docs/STATUS_REPORT.md").read_text()


def _embed(m):
    alt, path = m.group(1), m.group(2)
    data = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    return f"![{alt}](data:image/png;base64,{data})"


build = re.sub(r"!\[([^\]]*)\]\(([^)]+\.png)\)", _embed, md)
build_path = pathlib.Path("/tmp/status_build.md")
build_path.write_text(build)

pdf_bin = pathlib.Path.home() / ".claude/skills/gstack/make-pdf/dist/pdf"
out = str(ROOT / "Cell_Design_Engine_Status.pdf")
if pdf_bin.exists():
    subprocess.run(
        [str(pdf_bin), "generate", "--cover", "--toc",
         "--author", "Ayush Garg & Rohan Prasad", "--title", "Custom Cell Design Engine",
         str(build_path), out],
        check=True,
    )
    print("wrote", out)
else:
    print(f"make-pdf binary not found at {pdf_bin}; embedded build at {build_path}")
