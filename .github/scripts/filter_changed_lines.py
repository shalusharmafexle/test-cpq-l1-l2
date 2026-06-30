import json
import subprocess
import sys
import os

base_branch = sys.argv[1]

# ----------------------------
# Get merge base
# ----------------------------
merge_base = subprocess.check_output(
    ["git", "merge-base", "HEAD", f"origin/{base_branch}"],
    text=True
).strip()

# ----------------------------
# Get diff (ONLY changed lines)
# ----------------------------
diff = subprocess.check_output(
    ["git", "diff", "-U0", merge_base],
    text=True
)

changed_files = {}
current_file = None
new_line = None

# ----------------------------
# Parse git diff correctly
# ----------------------------
for line in diff.splitlines():

    # File path
    if line.startswith("+++ b/"):
        current_file = line[6:].strip()
        current_file = current_file.replace("\\", "/")
        current_file = current_file.replace("a/", "").replace("b/", "")

        changed_files[current_file] = set()

    # Hunk header
    elif line.startswith("@@"):
        parts = line.split(" ")

        new_file_part = [p for p in parts if p.startswith("+")][0]
        new_line = int(new_file_part.split(",")[0][1:])

    # Added line
    elif line.startswith("+") and not line.startswith("+++"):
        if current_file:
            changed_files[current_file].add(new_line)
        new_line += 1

    # Removed line (ignored for new-line tracking)
    elif line.startswith("-") and not line.startswith("---"):
        pass

    # Context (not present in -U0 usually, but safe)
    else:
        if new_line is not None:
            new_line += 1


# ----------------------------
# Load scanner output safely
# ----------------------------
with open("results.json") as f:
    data = json.load(f)


def extract_violations(obj):
    """Recursively extract violations from any scanner format"""
    violations = []

    if isinstance(obj, dict):

        if "violations" in obj:
            violations.extend(obj["violations"])

        for v in obj.values():
            violations.extend(extract_violations(v))

    elif isinstance(obj, list):

        for item in obj:
            violations.extend(extract_violations(item))

    return violations


violations = extract_violations(data)


# ----------------------------
# Normalize file paths
# ----------------------------
def normalize(path):
    return (
        path.replace("\\", "/")
        .replace("a/", "")
        .replace("b/", "")
        .strip()
    )


# ----------------------------
# Filter ONLY violations on changed lines
# ----------------------------
matched = []

for v in violations:

    file = v.get("fileName") or v.get("file") or v.get("path") or ""
    file = normalize(file)

    line = v.get("line") or v.get("beginLine") or v.get("startLine")

    try:
        line = int(line)
    except:
        continue

    if file in changed_files and line in changed_files[file]:
        matched.append(v)


# ----------------------------
# Fail build if needed
# ----------------------------
if matched:

    print("\n❌ Violations on changed lines:\n")

    for v in matched:
        print(
            f"{v.get('fileName')}:{v.get('line')} "
            f"{v.get('ruleName') or v.get('rule')} - "
            f"{v.get('message')}"
        )

    exit(1)

print("✅ No violations on modified lines.")