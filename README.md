## Autoconfig
quickly transfer scattered config files between systems

## example use:

1. git clone this repo to a USB
2. create a new template: `py autoconfig.py new config_template_name`
3. add your config file paths (for example `py autoconfig.py track config_template_name ~/.config/hypr/hyprland.config`)
4. clone your configs: `py autoconfig.py save <template>` (machine1 -> USB)
5. plug your USB into another system
6. load configs onto machine2: `py autoconfig.py load <template>` (USB -> machine2)


commands
```
list: lists all templates and their tracked paths
save <template>: saves configs from all tracked locations on the current machine

load <template>: loads to all locations in the machine

track <template> <path>: tracks a new path in your machine
    track all <path>: adds path to all templates

untrack <template> <path>
    untrack all <path>: removes tracked path from all templates

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


