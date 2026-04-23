automatically load and switch between configs across your system


save <template>: saves configs from all tracked locations on the current machine
load <template>: loads to all locations in the machine

track <template> <path>: tracks a new path in your machine
    track all <path>: adds path to all templates
    untrack all <path>: removes tracked path from all templates

new <template>: creates a new template
rm <template>: removes a template
clone <oldtemplate> <newtemplate>: clones a template




example template:

templates/
    arch/
        template.json
        tracked_files/
            hyprland.config

```template.json
{
    "description"   : "config for my arch machine",
    "tracked_files" : [
        {
            "abspath" : "/home/[user]/.config/hypr/hyprland.config",
            "content_location" : "hyprland.config",
        },
    ]
}
```



Notes:
- in commands, <path> does not have to be abspath. but abspath is always saved to config templates.
- the copies of the tracked files are stored in templates/<template>/tracked_files. if there are duplicates then the name is simply changed slightly.
- description is optional
