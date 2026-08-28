import re
import sys
from pathlib import Path

COMMIT_TYPES = (
    "feat",
    "fix",
    "docs",
    "refactor",
    "test",
    "chore",
    "ci",
    "perf",
    "build",
)

COMMIT_MESSAGE_PATTERN = re.compile(
    rf"^(?:{'|'.join(COMMIT_TYPES)})(?:\([a-z0-9_-]+\))?: .+$"
)


def print_usage() -> None:
    print("Invalid commit message.")
    print()
    print("Expected format:")
    print("  <type>(<scope>): <description>")
    print("  <type>: <description>")
    print()
    print("Allowed types:")
    print(f"  {', '.join(COMMIT_TYPES)}")
    print()
    print("Examples:")
    print("  feat(auth): add user registration")
    print("  fix(api): handle invalid request body")
    print("  docs(architecture): document service layer")
    print("  chore: update gitignore")


def main() -> int:
    if len(sys.argv) < 2:
        print("Error: commit message file was not provided.")
        return 1

    commit_message_file = Path(sys.argv[1])

    if not commit_message_file.is_file():
        print(f"Error: commit message file not found: {commit_message_file}")
        return 1

    lines = commit_message_file.read_text(encoding="utf-8").splitlines()

    if not lines:
        print("Error: commit message cannot be empty.")
        return 1

    commit_message = lines[0].strip()

    if not COMMIT_MESSAGE_PATTERN.fullmatch(commit_message):
        print_usage()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
