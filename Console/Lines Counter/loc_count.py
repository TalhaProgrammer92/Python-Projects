from enum import Enum
from pathlib import Path
import re


class CodeFile(Enum):
    # Python
    Python = ".py"

    # C / C-family
    C = ".c"
    CHeader = ".h"
    Cpp = ".cpp"
    CppHeader = ".hpp"
    CSharp = ".cs"
    Java = ".java"

    # JavaScript / TypeScript
    JavaScript = ".js"
    JavaScriptModule = ".mjs"
    TypeScript = ".ts"
    TypeScriptReact = ".tsx"
    JavaScriptReact = ".jsx"

    # Web
    HTML = ".html"
    XHTML = ".xhtml"
    CSS = ".css"
    SCSS = ".scss"
    SASS = ".sass"
    Less = ".less"

    # Microsoft / .NET
    VisualBasic = ".vb"
    FSharp = ".fs"
    FSharpSignature = ".fsi"

    # JVM
    Kotlin = ".kt"
    KotlinScript = ".kts"
    Scala = ".scala"
    Groovy = ".groovy"

    # Systems / scripting
    Rust = ".rs"
    Go = ".go"
    Swift = ".swift"
    ObjectiveC = ".m"
    ObjectiveCHeader = ".mm"
    Dart = ".dart"
    Lua = ".lua"
    Perl = ".pl"
    R = ".r"

    # Shell / command
    Shell = ".sh"
    Bash = ".bash"
    PowerShell = ".ps1"
    Batch = ".bat"
    Command = ".cmd"

    # Other
    Ruby = ".rb"
    PHP = ".php"
    SQL = ".sql"
    GDScript = ".gd"
    MATLAB = ".m"
    XAML = ".xaml"


# Comment syntax used by the supported languages.
COMMENT_RULES = {
    # // and /* */
    ".c": (("//",), ("/*", "*/")),
    ".h": (("//",), ("/*", "*/")),
    ".cpp": (("//",), ("/*", "*/")),
    ".hpp": (("//",), ("/*", "*/")),
    ".cs": (("//",), ("/*", "*/")),
    ".java": (("//",), ("/*", "*/")),
    ".js": (("//",), ("/*", "*/")),
    ".mjs": (("//",), ("/*", "*/")),
    ".ts": (("//",), ("/*", "*/")),
    ".tsx": (("//",), ("/*", "*/")),
    ".jsx": (("//",), ("/*", "*/")),
    ".go": (("//",), ("/*", "*/")),
    ".rust": (("//",), ("/*", "*/")),
    ".rs": (("//",), ("/*", "*/")),
    ".swift": (("//",), ("/*", "*/")),
    ".kt": (("//",), ("/*", "*/")),
    ".kts": (("//",), ("/*", "*/")),
    ".scala": (("//",), ("/*", "*/")),
    ".groovy": (("//",), ("/*", "*/")),
    ".dart": (("//",), ("/*", "*/")),
    ".php": (("//", "#"), ("/*", "*/")),

    # #
    ".py": (("#",), ()),
    ".rb": (("#",), ()),
    ".pl": (("#",), ()),
    ".r": (("#",), ()),
    ".lua": (("--",), ("--[[", "]]")),
    ".gd": (("#",), ()),
    ".sh": (("#",), ()),
    ".bash": (("#",), ()),

    # SQL
    ".sql": (("--",), ("/*", "*/")),

    # HTML / XML
    ".html": ((), ("<!--", "-->")),
    ".xhtml": ((), ("<!--", "-->")),

    # CSS
    ".css": ((), ("/*", "*/")),
    ".scss": (("//",), ("/*", "*/")),
    ".sass": (("//",), ("/*", "*/")),
    ".less": (("//",), ("/*", "*/")),

    # Visual Basic
    ".vb": (("'", "REM "), (),),

    # F#
    ".fs": (("//",), ("(*", "*)")),
    ".fsi": (("//",), ("(*", "*)")),

    # PowerShell
    ".ps1": (("#",), ("<#", "#>")),

    # Batch
    ".bat": (("REM ", "::"), ()),
    ".cmd": (("REM ", "::"), ()),

    # MATLAB / Objective-C
    ".m": (("%", "//"), ("/*", "*/")),
    ".mm": (("//",), ("/*", "*/")),
    ".xaml": ((), ("<!--", "-->"))
}


def get_supported_extensions():
    return {language.value for language in CodeFile}


def is_inside_string(line, index):
    """
    Determines whether a character at `index` is inside a quoted string.

    This handles common single, double and backtick quoted strings.
    """

    quote = None
    escaped = False

    for i, char in enumerate(line[:index]):
        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if quote is None:
            if char in ("'", '"', "`"):
                quote = char
        elif char == quote:
            quote = None

    return quote is not None


def remove_comments(file_path):
    """
    Reads a source file and returns the number of non-empty,
    non-comment lines.

    Both single-line and multiline comments are ignored.
    """

    extension = file_path.suffix.lower()

    single_line_comments, multiline_comments = COMMENT_RULES.get(
        extension,
        ((), ())
    )

    loc = 0
    inside_multiline_comment = False
    multiline_end = None

    try:
        with file_path.open(
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            for line in file:
                remaining = line

                while remaining:
                    # Currently inside /* ... */ or equivalent
                    if inside_multiline_comment:
                        end_index = remaining.find(multiline_end)

                        if end_index == -1:
                            remaining = ""
                            continue

                        remaining = remaining[
                            end_index + len(multiline_end):
                        ]

                        inside_multiline_comment = False
                        multiline_end = None

                        continue

                    # Find earliest single-line or multiline comment.
                    candidates = []

                    for marker in single_line_comments:
                        index = remaining.find(marker)

                        if index != -1 and not is_inside_string(
                            remaining,
                            index
                        ):
                            candidates.append(
                                (index, "single", marker)
                            )

                    for start, end in multiline_comments:
                        index = remaining.find(start)

                        if index != -1 and not is_inside_string(
                            remaining,
                            index
                        ):
                            candidates.append(
                                (index, "multi", (start, end))
                            )

                    # No comments found in the remaining text.
                    if not candidates:
                        if remaining.strip():
                            loc += 1

                        remaining = ""
                        continue

                    # Pick the comment occurring first.
                    index, comment_type, marker = min(
                        candidates,
                        key=lambda item: item[0]
                    )

                    # Keep the code before the comment.
                    code_before_comment = remaining[:index]

                    if comment_type == "single":
                        if code_before_comment.strip():
                            loc += 1

                        remaining = ""

                    else:
                        # Multiline comment.
                        start, end = marker

                        if code_before_comment.strip():
                            loc += 1

                        remaining = remaining[
                            index + len(start):
                        ]

                        inside_multiline_comment = True
                        multiline_end = end

        return loc

    except (OSError, UnicodeError):
        return 0


def get_language_from_extension(extension):
    for language in CodeFile:
        if language.value == extension:
            return language.name

    return None


def main():
    print("=== Code LOC Scanner ===\n")

    location = input("Enter folder location: ").strip()
    extension = input(
        "Enter file extension (e.g. .cs, .py, .js): "
    ).strip().lower()

    if not extension.startswith("."):
        extension = "." + extension

    print("\nScanning the location...")

    folder = Path(location)

    if not folder.exists():
        print("\nError: The specified location does not exist.")
        return

    if not folder.is_dir():
        print("\nError: The specified location is not a folder.")
        return

    supported_extensions = get_supported_extensions()

    if extension not in supported_extensions:
        print(f"\nError: '{extension}' is not a supported code file.")
        print("\nSupported extensions:")

        for language in CodeFile:
            print(f"  {language.name:<25} {language.value}")

        return

    language = get_language_from_extension(extension)

    files = list(folder.rglob(f"*{extension}"))

    total_files = len(files)
    total_loc = sum(remove_comments(file) for file in files)

    print("\n--- Scan Result ---")
    print(f"Language        : {language}")
    print(f"Extension       : {extension}")
    print(f"Files found     : {total_files}")
    print(f"LOC             : {total_loc}")


if __name__ == "__main__":
    main()