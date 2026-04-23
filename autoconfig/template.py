import shutil
from pathlib import Path

from autoconfig.utils import (
    expand_path,
    get_template_dir,
    load_template_json,
    resolve_path,
    save_template_json,
    unique_filename,
)


class Template:
    def __init__(self, name):
        self.name = name
        self.dir = get_template_dir(name)
        self.tracked_files_dir = self.dir / "tracked_files"
        if self.dir.exists():
            self.data = load_template_json(name)
        else:
            self.data = {"tracked_files": []}

    @property
    def tracked_files(self):
        return self.data["tracked_files"]

    def create(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        self.tracked_files_dir.mkdir(exist_ok=True)
        save_template_json(self.name, self.data)

    def add_tracked_file(self, path):
        stored_path = resolve_path(path)
        for entry in self.tracked_files:
            if entry["abspath"] == stored_path:
                print(f"Already tracking: {stored_path}")
                return
        basename = Path(stored_path).name
        content_location = unique_filename(self.tracked_files_dir, basename)
        self.tracked_files.append({
            "abspath": stored_path,
            "content_location": content_location,
        })
        save_template_json(self.name, self.data)
        print(f"Tracking: {stored_path} -> {content_location}")

    def remove_tracked_file(self, path):
        stored_path = resolve_path(path)
        for entry in self.tracked_files:
            if entry["abspath"] == stored_path:
                stored = self.tracked_files_dir / entry["content_location"]
                if stored.exists():
                    stored.unlink()
                self.tracked_files.remove(entry)
                save_template_json(self.name, self.data)
                print(f"Untracked: {stored_path}")
                return
        print(f"Not tracked: {stored_path}")

    def save_to_disk(self):
        self.tracked_files_dir.mkdir(exist_ok=True)
        for entry in self.tracked_files:
            src = Path(expand_path(entry["abspath"]))
            dst = self.tracked_files_dir / entry["content_location"]
            if src.exists():
                shutil.copy2(str(src), str(dst))
                print(f"Saved: {entry['abspath']} -> {dst}")
            else:
                print(f"Warning: {entry['abspath']} does not exist, skipping")
        save_template_json(self.name, self.data)

    def load_to_system(self):
        for entry in self.tracked_files:
            src = self.tracked_files_dir / entry["content_location"]
            dst = Path(expand_path(entry["abspath"]))
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(dst))
                print(f"Loaded: {src} -> {entry['abspath']}")
            else:
                print(f"Warning: {src} does not exist in template, skipping")
