import subprocess

# List of scripts to run in sequence
scripts = [
    "scripts/scraper_final.py",
    "scripts/preprocessing.py",
    "scripts/combine.py",
    "scripts/split_by_type.py",
]

for script in scripts:
    print(f"🚀 Running {script}...")
    subprocess.run(["python", script], check=True)
    print(f"✅ Finished {script}\n")
