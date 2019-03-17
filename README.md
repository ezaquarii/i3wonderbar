# i3 Wonderbar

A hackable `i3status` wrapper written in Python.

This script allows you to replace or extend `i3status` with your
own statuses in a clean way.

`i3status` documentation advises to wrap it in shell script
and append more data to the output, but this approach relies on
polling.

Wonderbar uses `i3status` **AND** is event-driven, thanks to `asyncio`.

# Installation

Drop `wonderbar.py` somewhere and ask `i3wm` to use it. That's all.
I do not plan to create a *dpkg* package for it, but if somebody does,
I can maintain it.

This is my config:

```
bar {
        status_command ~/bin/wonderbar.py --config ~/.config/i3/i3status.conf
        font pango: DejaVu Sans Mono, Awesome 16
}
```

# Features

1. Event-driven `i3bar` updates
2. Plugins API
3. Single file - just drop it somewhere in your `${PATH}`
4. Very hackable - so much that Doge approves
5. Depends only on Python standard library

# Plugins

There are currently 5 plugins:

1. I3Plugin - Wraps i3status and forwards all status updates to output
2. TouchpadPlugin - Listens for `xinput` updates and shows when touchpad
is disabled. It tries to guess which input device is a touchpad,
but I admit that it is not very intelligent. It works for me.
3. MemoryPlugin - shows used RAM; requires psutils
4. PowerPlugin - shows colored power status; requires psutils
5. DemoPlugin - Very minimalistic template plugin that displays a
counter. Use it to start your own plugin. *Not enabled by default*.

# FAQ

## Why did you create this?

Dell XPS 13 touchpad is very sensitive and I tend to touch it
accidentally, switching windows, selecting large portions of text, etc.

I created a shortcut to toggle the touchpad on/off, but there was
no easy way to get it's status on `i3bar`.

## How can I use it?

You can easily add your own plugins with fancy functions and enjoy
immediate, event-driven updates on your `i3bar`.

## Why not Go?

Go away.

## Why not Node.js

You too.
