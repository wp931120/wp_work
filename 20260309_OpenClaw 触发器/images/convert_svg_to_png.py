#!/usr/bin/env python3
"""Convert SVG files to PNG using cairosvg"""

import cairosvg
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

svg_files = [
    'trigger_types_diagram.svg',
    'decision_tree.svg',
    'comparison_table.svg',
]

for svg_file in svg_files:
    svg_path = OUTPUT_DIR / svg_file
    png_path = OUTPUT_DIR / svg_path.stem + '.png'

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=1600,
        output_height=1200,
    )
    print(f"Created: {png_path}")

print("\nAll conversions complete!")
