"""
Script to replace invalid m4a files with repaired ones
"""

import os
import shutil

# Copy files from `repaired_files` to paths described in `invalid_files.txt`
with open("./invalid_files.txt", "r", encoding="utf-8") as f:
    for line in f:
        original_path = line.strip("\n")
        repaired_path = f"./repaired_files/{os.path.basename(original_path)}"
        shutil.copy(repaired_path, original_path)
        print(f"Repaired file copied to {original_path}")
