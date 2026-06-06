"""Build the status PDF from docs/STATUS_REPORT.md.

Embeds the report images as base64 data URIs (make-pdf does not scale or reliably
load local images, so they are inlined and width-constrained here), then renders
via the gstack make-pdf binary.

Regenerate the images first (they live in results/, which is gitignored):
  python scripts/validate_chen2020.py        # results/validate_chen2020.png
  python scripts/run_demo.py                 # results/design_space.png
  python scripts/make_diagrams.py            # results/review_convergence.png
  mmdc -i docs/diagrams/pipeline.mmd -o results/pipeline.png -b white -s 3
  mmdc -i docs/diagrams/flywheel.mmd -o results/flywheel.png -b white -s 3
"""

import base64
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
md = (ROOT / "docs/STATUS_REPORT.md").read_text()

# Per-image display width (% of content box). make-pdf does not scale images to
# fit the page, so wide figures clip unless constrained here. Tuned so each fits
# within one page with its surrounding text. Default 100%.
WIDTH = {
    "pipeline.png": 57,
    "flywheel.png": 100,
    "validate_chen2020.png": 92,
    "design_space.png": 100,
    "review_convergence.png": 70,
}


def _embed(m):
    path = m.group(2)
    name = pathlib.Path(path).name
    data = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    pct = WIDTH.get(name, 100)
    # centered, width-constrained HTML img so nothing clips or overflows the page
    return (f'<div style="text-align:center"><img style="max-width:{pct}%;height:auto" '
            f'src="data:image/png;base64,{data}"></div>')


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
