import os
import subprocess

scripts = [
    "douban_movie_crawler.py",
    "douban_visual_scatter_plot.py",
    "Visual_bar_chart.py",
    "Visual_pie_chart.py"
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python", script], capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    print(result.stderr)
    print(f"Finished {script}\n")
