automatically load and switch between configs across your system

example installation: git clone this to a USB

example use: add all your config file paths to a new template, save them with `save <template>`, plug your USB into another system, type `load <template>`


```
list: lists all templates and their tracked paths
save <template>: saves configs from all tracked locations on the current machine
load <template>: loads to all locations in the machine

track <template> <path>: tracks a new <path> in your machine
    track all <path>: adds <path> to all templates
    untrack all <path>: removes tracked <path> from all templates

new <template>: creates a new template
rm <template>: removes a template
clone <oldtemplate> <newtemplate>: clones a template
```

example template:

```
templates/
    arch/
        template.json
        tracked_files/
            hyprland.config
```

```template.json
{
    "description"   : "config for my arch machine",
    "tracked_files" : [
        {
            "path" : "~/.config/hypr/hyprland.config",
            "content_location" : "hyprland.config",
        },
    ]
}
```


