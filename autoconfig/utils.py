import json
import os
from pathlib import Path


def get_root_dir():
    return Path(__file__).resolve().parent.parent


def get_templates_dir():
    d = get_root_dir() / "templates"
    d.mkdir(exist_ok=True)
    return d


def get_template_dir(template_name):
    return get_templates_dir() / template_name


def resolve_path(path):
    expanded = Path(path).expanduser().resolve()
    home = Path.home()
    try:
        return "~/" + str(expanded.relative_to(home))
    except ValueError:
        return str(expanded)


def expand_path(path):
    return str(Path(path).expanduser().resolve())


def unique_filename(directory, basename):
    target = Path(directory) / basename
    if not target.exists():
        return basename
    i = 2
    while True:
        candidate = f"{basename}_{i}"
        if not (Path(directory) / candidate).exists():
            return candidate
        i += 1


def load_template_json(template_name):
    path = get_template_dir(template_name) / "template.json"
    with open(path) as f:
        return json.load(f)


def save_template_json(template_name, data):
    path = get_template_dir(template_name) / "template.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def list_templates():
    templates_dir = get_templates_dir()
    return [d.name for d in templates_dir.iterdir() if d.is_dir()]
