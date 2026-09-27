from pathlib import Path


def count_lines(file_path):
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for _ in file)
    except (OSError, UnicodeError):
        return 0


def main():
    location = input("Enter folder location: ").strip()
    extension = input("Enter file extension (e.g. .cs, .py, .js): ").strip()

    if not extension.startswith("."):
        extension = "." + extension

    folder = Path(location)

    if not folder.exists():
        print("Error: The specified location does not exist.")
        return

    if not folder.is_dir():
        print("Error: The specified location is not a folder.")
        return

    files = list(folder.rglob(f"*{extension}"))

    total_files = len(files)
    total_lines = sum(count_lines(file) for file in files)

    print("\n--- Scan Result ---")
    print(f"Extension       : {extension}")
    print(f"Files found     : {total_files}")
    print(f"Total lines     : {total_lines}")


if __name__ == "__main__":
    main()
