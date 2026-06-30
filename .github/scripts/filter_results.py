import json
import sys

with open("changed_lines.json") as f:
    changed = json.load(f)

with open("results.json") as f:
    results = json.load(f)

violations = []

# Handle both array and object output formats
issues = results

if isinstance(results, dict):
    if "violations" in results:
        issues = results["violations"]
    elif "result" in results:
        issues = results["result"]

for issue in issues:

    file_path = issue.get("file") or issue.get("fileName")

    line = (
        issue.get("line")
        or issue.get("lineNumber")
        or issue.get("startLine")
    )

    if not file_path or line is None:
        continue

    if file_path in changed:
        if int(line) in changed[file_path]:
            violations.append(issue)

print("\n==============================")
print("Violations on Changed Lines")
print("==============================")

if violations:
    print(json.dumps(violations, indent=4))
    print(f"\n❌ Build failed: {len(violations)} violation(s) found.")
    sys.exit(1)
else:
    print("✅ No violations on modified lines.")
    sys.exit(0)