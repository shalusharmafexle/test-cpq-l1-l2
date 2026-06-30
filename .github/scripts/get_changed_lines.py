import subprocess
import re
import json
import sys

BASE_BRANCH = "origin/main"

try:
    diff = subprocess.check_output(
        ["git", "diff", f"{BASE_BRANCH}...HEAD", "--unified=0"],
        text=True
    )
except subprocess.CalledProcessError as e:
    print(f"Error running git diff: {e}")
    sys.exit(1)

changed_lines = {}

current_file = None

for line in diff.splitlines():

    if line.startswith("+++ b/"):
        current_file = line[6:]

        # Only Apex files
        if current_file.endswith(".cls") or current_file.endswith(".trigger"):
            changed_lines[current_file] = set()
        else:
            current_file = None

    elif line.startswith("@@") and current_file:

        match = re.search(r"\+(\d+)(?:,(\d+))?", line)

        if match:
            start = int(match.group(1))
            count = int(match.group(2) or 1)

            for i in range(start, start + count):
                changed_lines[current_file].add(i)

# Convert sets to sorted lists
output = {
    file: sorted(list(lines))
    for file, lines in changed_lines.items()
}

with open("changed_lines.json", "w") as f:
    json.dump(output, f, indent=4)

print(json.dumps(output, indent=4))