import subprocess
import sys


def main():
    args = sys.argv[1:]

    if "--fix" in args or not args:
        print("--- ruff check ---")
        subprocess.run(["ruff", "check", "--fix"], check=False)

        print("\n--- ruff format ---")
        subprocess.run(["ruff", "format"], check=False)

        print("\n--- ty check ---")
        subprocess.run(["ty", "check", "src/"], check=False)

    if "--check" in args:
        print("--- ruff check ---")
        subprocess.run(["ruff", "check"], check=False)

        print("\n--- ruff format --check ---")
        subprocess.run(["ruff", "format", "--check"], check=False)

        print("\n--- ty check ---")
        subprocess.run(["ty", "check", "src/"], check=False)


if __name__ == "__main__":
    main()
