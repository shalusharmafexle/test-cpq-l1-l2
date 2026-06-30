#!/usr/bin/env python3

import json
import subprocess
import sys
import os

base_branch = sys.argv[1]

merge_base = subprocess.check_output(
    ["git", "merge-base", "HEAD", f"origin/{base_branch}"],
    text=True
).strip()

diff = subprocess.check_output(
    ["git", "diff", "-U0", merge_base],
    text=True
)

changed = {}

current_file = None
current_line = None

for line in diff.splitlines():

    if line.startswith("+++ b/"):
        current_file = os.path.normpath(line[6:])
        changed[current_file] = set()

    elif line.startswith("@@"):

        part = line.split()[2]

        if "," in part:
            start, count = part[1:].split(",")
            start = int(start)
            count = int(count)
        else:
            start = int(part[1:])
            count = 1

        current_line = start

    elif line.startswith("+") and not line.startswith("+++"):

        changed[current_file].add(current_line)
        current_line += 1

    elif line.startswith("-") and not line.startswith("---"):
        pass

    else:

        if current_line is not None:
            current_line += 1


def collect(obj):

    violations = []

    if isinstance(obj, dict):

        if "violations" in obj:
            violations.extend(obj["violations"])

        for value in obj.values():
            violations.extend(collect(value))

    elif isinstance(obj, list):

        for item in obj:
            violations.extend(collect(item))

    return violations


with open("results.json") as f:
    data = json.load(f)

violations = collect(data)

new_violations = []

for v in violations:

    file = (
        v.get("fileName")
        or v.get("file")
        or v.get("source")
    )

    if not file:
        continue

    file = os.path.normpath(file)

    line = (
        v.get("line")
        or v.get("beginLine")
        or v.get("startLine")
    )

    if line is None:
        continue

    try:
        line = int(line)
    except:
        continue

    if file in changed and line in changed[file]:
        new_violations.append(v)

if new_violations:

    print("\n")
    print("=" * 60)
    print("New violations found on modified lines")
    print("=" * 60)

    for v in new_violations:

        print(
            f"""
File      : {v.get('fileName') or v.get('file')}
Line      : {v.get('line') or v.get('beginLine')}
Rule      : {v.get('ruleName') or v.get('rule')}
Severity  : {v.get('severity')}
Message   : {v.get('message')}
"""
        )

    print("=" * 60)

    sys.exit(1)

print("✅ No violations introduced in modified lines.")