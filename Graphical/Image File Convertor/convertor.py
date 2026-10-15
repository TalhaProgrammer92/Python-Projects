from __future__ import annotations

import os
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

APP_TITLE = "ImageMagick Converter"
SUPPORTED_OUTPUT_FORMATS = [
    "png",
    "jpg",
    "jpeg",
    "webp",
    "bmp",
    "ico",
    "tif",
    "tiff",
    "gif",
    "pdf",
    "avif",
    "heic",
    "jp2",
    "jxl",
    "ps",
    "eps",
]


def find_magick() -> str | None:
    """Return the ImageMagick executable path when available."""
    return shutil.which("magick")


def run_command(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command without opening a console window on Windows."""
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creationflags,
        **kwargs,
    )


class ConverterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("650x430")
        self.root.minsize(580, 390)

        self.magick_path = find_magick()
        self.files: list[Path] = []
        self.output_dir = tk.StringVar(value=str(Path.home() / "Pictures"))
        self.output_format = tk.StringVar(value="png")
        self.ico_sizes = tk.StringVar(value="256,128,64,48,32,16")
        self.status = tk.StringVar()

        self._build_ui()
        self._update_magick_status()

        if not self.magick_path:
            self.root.after(250, self._ask_to_install)

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill="both", expand=True)

        top = ttk.Frame(outer)
        top.pack(fill="x")
        ttk.Label(
            top, text="ImageMagick Converter", font=("Segoe UI", 15, "bold")
        ).pack(side="left")
        self.magick_label = ttk.Label(top, text="Checking ImageMagick…")
        self.magick_label.pack(side="right")

        ttk.Separator(outer).pack(fill="x", pady=(10, 12))

        file_row = ttk.Frame(outer)
        file_row.pack(fill="x")
        ttk.Label(file_row, text="Input files").pack(side="left")
        ttk.Button(file_row, text="Add files…", command=self.add_files).pack(
            side="right"
        )
        ttk.Button(file_row, text="Clear", command=self.clear_files).pack(
            side="right", padx=(0, 7)
        )

        list_frame = ttk.Frame(outer)
        list_frame.pack(fill="both", expand=True, pady=(7, 12))
        self.file_list = tk.Listbox(list_frame, height=8, selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.file_list.yview
        )
        self.file_list.configure(yscrollcommand=scrollbar.set)
        self.file_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        settings = ttk.Frame(outer)
        settings.pack(fill="x")

        ttk.Label(settings, text="Output format").grid(row=0, column=0, sticky="w")
        self.format_combo = ttk.Combobox(
            settings,
            textvariable=self.output_format,
            values=SUPPORTED_OUTPUT_FORMATS,
            state="readonly",
            width=12,
        )
        self.format_combo.grid(row=1, column=0, sticky="w", pady=(4, 8))
        self.format_combo.bind("<<ComboboxSelected>>", self._format_changed)

        ttk.Label(settings, text="ICO sizes (ICO only)").grid(
            row=0, column=1, sticky="w", padx=(18, 0)
        )
        self.ico_entry = ttk.Entry(settings, textvariable=self.ico_sizes, width=23)
        self.ico_entry.grid(row=1, column=1, sticky="w", padx=(18, 0), pady=(4, 8))

        ttk.Label(settings, text="Save to").grid(row=2, column=0, sticky="w")
        dest_row = ttk.Frame(settings)
        dest_row.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(4, 8))
        ttk.Entry(dest_row, textvariable=self.output_dir).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(dest_row, text="Browse…", command=self.choose_output_dir).pack(
            side="left", padx=(7, 0)
        )
        settings.columnconfigure(1, weight=1)

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(4, 0))
        ttk.Label(bottom, textvariable=self.status).pack(
            side="left", fill="x", expand=True
        )
        self.convert_button = ttk.Button(bottom, text="Convert", command=self.convert)
        self.convert_button.pack(side="right")

        self._format_changed()

    def _update_magick_status(self):
        self.magick_path = find_magick()
        if self.magick_path:
            self.magick_label.configure(
                text="ImageMagick detected", foreground="#18794e"
            )
            self.status.set(f"Ready — {self.magick_path}")
            self.convert_button.configure(state="normal")
        else:
            self.magick_label.configure(
                text="ImageMagick not found", foreground="#b42318"
            )
            self.status.set("Install ImageMagick to enable conversion.")
            self.convert_button.configure(state="disabled")

    def _ask_to_install(self):
        if messagebox.askyesno(
            "ImageMagick required",
            "ImageMagick (magick) was not found.\n\n"
            "Would you like to try installing it with Windows Package Manager (winget)?\n"
            "This requires an internet connection and may request administrator approval.",
        ):
            self.install_magick()

    def install_magick(self):
        if not shutil.which("winget"):
            messagebox.showinfo(
                "Manual installation required",
                "Windows Package Manager (winget) was not found.\n\n"
                "Install ImageMagick from:\nhttps://imagemagick.org/script/download.php#windows\n\n"
                "During setup, enable the option to add ImageMagick to PATH. "
                "Then restart this utility.",
            )
            return

        self.convert_button.configure(state="disabled")
        self.status.set("Installing ImageMagick…")
        threading.Thread(target=self._install_worker, daemon=True).start()

    def _install_worker(self):
        try:
            result = run_command(
                [
                    "winget",
                    "install",
                    "--id",
                    "ImageMagick.ImageMagick",
                    "--exact",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ],
                timeout=900,
            )
            self.root.after(
                0,
                lambda: self._install_finished(
                    result.returncode, result.stdout, result.stderr
                ),
            )
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self._install_failed("Installation timed out."))
        except OSError as exc:
            self.root.after(0, lambda: self._install_failed(str(exc)))

    def _install_finished(self, returncode: int, stdout: str, stderr: str):
        # PATH changes made by an installer may not reach an already-running process.
        self._update_magick_status()
        if not self.magick_path:
            messagebox.showinfo(
                "Restart may be required",
                "The installer finished, but this running app still cannot find 'magick'.\n\n"
                "Close and reopen the utility. If it is still missing, verify ImageMagick is "
                "installed and added to PATH.\n\n"
                + (stderr[-1200:] if stderr else stdout[-1200:]),
            )
            self.status.set("Restart the app if ImageMagick was just installed.")
        elif returncode == 0:
            messagebox.showinfo("Installed", "ImageMagick is ready to use.")
        else:
            messagebox.showwarning(
                "Installer returned an error",
                f"winget exited with code {returncode}.\n\n{stderr[-1500:] or stdout[-1500:]}",
            )

    def _install_failed(self, error: str):
        self._update_magick_status()
        messagebox.showerror("Installation failed", error)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Choose files to convert", filetypes=[("All files", "*.*")]
        )
        known = {str(p).casefold() for p in self.files}
        for raw in paths:
            p = Path(raw)
            if str(p).casefold() not in known:
                self.files.append(p)
                self.file_list.insert(tk.END, str(p))
                known.add(str(p).casefold())
        if self.files:
            self.status.set(f"{len(self.files)} file(s) selected.")

    def clear_files(self):
        self.files.clear()
        self.file_list.delete(0, tk.END)
        self.status.set("No files selected.")

    def choose_output_dir(self):
        folder = filedialog.askdirectory(
            title="Choose output folder", initialdir=self.output_dir.get()
        )
        if folder:
            self.output_dir.set(folder)

    def _format_changed(self, _event=None):
        if self.output_format.get().lower() == "ico":
            self.ico_entry.configure(state="normal")
        else:
            self.ico_entry.configure(state="disabled")

    def convert(self):
        self._update_magick_status()
        if not self.magick_path:
            messagebox.showerror("ImageMagick missing", "Install ImageMagick first.")
            return
        if not self.files:
            messagebox.showwarning("No input files", "Add at least one input file.")
            return

        output_dir = Path(self.output_dir.get()).expanduser()
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror("Output folder error", str(exc))
            return

        fmt = self.output_format.get().strip().lower().lstrip(".")
        if fmt not in SUPPORTED_OUTPUT_FORMATS:
            messagebox.showerror("Invalid format", "Choose a supported output format.")
            return

        sizes: list[int] = []
        if fmt == "ico":
            try:
                sizes = [
                    int(part.strip())
                    for part in self.ico_sizes.get().split(",")
                    if part.strip()
                ]
                if not sizes or any(size < 1 or size > 256 for size in sizes):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Invalid ICO sizes",
                    "Enter comma-separated sizes from 1 to 256, e.g. 256,128,64,48,32,16.",
                )
                return

        jobs: list[tuple[Path, Path, list[str]]] = []
        for source in self.files:
            if not source.is_file():
                continue
            # Avoid overwriting the source if its extension already matches.
            stem = source.stem
            destination = output_dir / f"{stem}.{fmt}"
            if destination.resolve() == source.resolve():
                destination = output_dir / f"{stem}_converted.{fmt}"

            command = [self.magick_path, str(source)]
            if fmt == "ico":
                # Create multiple icon sizes in one ICO, like the command in the request.
                command += ["-define", f"icon:auto-resize={','.join(map(str, sizes))}"]
            command.append(str(destination))
            jobs.append((source, destination, command))

        if not jobs:
            messagebox.showerror(
                "No valid files", "None of the selected input files exists."
            )
            return

        self.convert_button.configure(state="disabled")
        self.status.set(f"Converting {len(jobs)} file(s)…")
        threading.Thread(target=self._convert_worker, args=(jobs,), daemon=True).start()

    def _convert_worker(self, jobs: list[tuple[Path, Path, list[str]]]):
        results: list[tuple[Path, Path, bool, str]] = []
        for source, destination, command in jobs:
            try:
                completed = run_command(command, timeout=300)
                error = (completed.stderr or completed.stdout).strip()
                results.append((source, destination, completed.returncode == 0, error))
            except subprocess.TimeoutExpired:
                results.append(
                    (
                        source,
                        destination,
                        False,
                        "Conversion timed out after 5 minutes.",
                    )
                )
            except OSError as exc:
                results.append((source, destination, False, str(exc)))
        self.root.after(0, lambda: self._conversion_finished(results))

    def _conversion_finished(self, results: list[tuple[Path, Path, bool, str]]):
        self.convert_button.configure(
            state="normal" if self.magick_path else "disabled"
        )
        successes = [item for item in results if item[2]]
        failures = [item for item in results if not item[2]]
        self.status.set(
            f"Finished: {len(successes)} succeeded, {len(failures)} failed."
        )
        if failures:
            details = []
            for source, _destination, _ok, error in failures[:5]:
                details.append(
                    f"{source.name}\n{error[-900:] or 'ImageMagick reported a conversion error.'}"
                )
            messagebox.showwarning(
                "Conversion completed with errors",
                f"{len(successes)} succeeded; {len(failures)} failed.\n\n"
                + "\n\n".join(details),
            )
        else:
            messagebox.showinfo(
                "Conversion complete",
                f"Successfully converted {len(successes)} file(s).\n\nSaved to:\n{self.output_dir.get()}",
            )


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except tk.TclError:
        pass
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
