import shutil

from autoconfig.template import Template
from autoconfig.utils import get_template_dir, list_templates


def cmd_new(name):
    if get_template_dir(name).exists():
        print(f"Template '{name}' already exists")
        return
    t = Template(name)
    t.create()
    print(f"Created template: {name}")


def cmd_rm(name):
    d = get_template_dir(name)
    if not d.exists():
        print(f"Template '{name}' does not exist")
        return
    shutil.rmtree(d)
    print(f"Removed template: {name}")


def cmd_clone(old_name, new_name):
    old_dir = get_template_dir(old_name)
    new_dir = get_template_dir(new_name)
    if not old_dir.exists():
        print(f"Template '{old_name}' does not exist")
        return
    if new_dir.exists():
        print(f"Template '{new_name}' already exists")
        return
    shutil.copytree(str(old_dir), str(new_dir))
    print(f"Cloned '{old_name}' -> '{new_name}'")


def cmd_save(name):
    if not get_template_dir(name).exists():
        print(f"Template '{name}' does not exist")
        return
    t = Template(name)
    t.save_to_disk()
    print(f"Saved template: {name}")


def cmd_load(name):
    if not get_template_dir(name).exists():
        print(f"Template '{name}' does not exist")
        return
    t = Template(name)
    t.load_to_system()
    print(f"Loaded template: {name}")


def cmd_track(name, path):
    if name == "all":
        templates = list_templates()
        if not templates:
            print("No templates exist")
            return
        for tname in templates:
            t = Template(tname)
            t.add_tracked_file(path)
    else:
        if not get_template_dir(name).exists():
            print(f"Template '{name}' does not exist")
            return
        t = Template(name)
        t.add_tracked_file(path)


def cmd_untrack(name, path):
    if name == "all":
        templates = list_templates()
        if not templates:
            print("No templates exist")
            return
        for tname in templates:
            t = Template(tname)
            t.remove_tracked_file(path)
    else:
        if not get_template_dir(name).exists():
            print(f"Template '{name}' does not exist")
            return
        t = Template(name)
        t.remove_tracked_file(path)
