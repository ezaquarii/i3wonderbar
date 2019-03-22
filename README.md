# i3 Wonderbar

A hackable `i3status` wrapper written in Python.

This script allows you to replace or extend `i3status` with your
own statuses in a clean way.

`i3status` documentation advises to wrap it in shell script
and append more data to the output, but this approach relies on
polling.

Wonderbar uses `i3status` **AND** is event-driven, thanks to `asyncio`.

![Screenshot](i3wonderbar.png)

From left to right:

1. Touchpad is disabled
2. RAM - ~43% used
3. Battery power (5h left)
4. Network status
5. i3status - volume
6. i3status - time
7. Network manager applet

# Installation

## Simple copy

Drop `src/*` contents somewhere (ex. `/opt/i3wonderbar`) and ask `i3wm`
to use it, ex. `/opt/i3wonderbar/i3wonderbar`.

You'll need to manually supply the requirements:

1. `python3-psutil`
2. `python3-networkmanager`
3. `python3-dbus`

## Package

Tested on **Ubuntu 18.04**, but it should work for any Debian-ish system.

```
$ make deb
$ sudo dpkg -i ../i3wonderbar*.deb
$ sudo apt-get install -f # installs any unmet dependencies
```

Alternatively you can use `gdebi`

```
$ make deb
$ sudo gdebi ../i3wonderbar*.deb # it handles dependencies without apt-get install -f
```

# Usage

## i3wonderbar configuration

`i3wonderbar` is configured using a simple config file. Type

```
$ i3wonderbar --print-config
```

to show current configuration file. If no file is supplied, it will
show internal default config. You can simply save the output to a file
(`i3wonderbar --print-config > config.ini`) and tune it to your needs.

If `I3StatusPlugin` is used, you probably want to supply `i3status`
config file using `--i3status-config my-i3status.conf` option.

## i3-wm configuration

Use `i3wonderbar` as `i3status` replacement in `i3wm` config.
This is my setup:

```
bar {
        status_command i3wonderbar --i3status-config ~/.i3status.conf --config ~/.i3wonderbar.conf
        font pango: DejaVu Sans Mono, Awesome 16
}
```

# Features

1. Event-driven `i3bar` updates
2. Plugins API
3. Single file - just drop it somewhere in your `${PATH}`
4. So hackable - Doge approves
5. Depends only on Python standard library

# Plugins

There are currently 6 plugins:

1. `I3StatusPlugin` - Wraps `i3status` and forwards all status updates to stdout.
2. `TouchpadPlugin` - Listens for `xinput` updates and shows when touchpad
is disabled. It tries to guess which input device is a touchpad,
but I have to admit that it is not very intelligent. It works for me. :)
3. `MemoryPlugin` - Shows used RAM; requires psutils.
4. `PowerPlugin` - Shows colored power status; requires psutils.
5. `NetworkPlugin` - shows current network.
6. `DemoPlugin` - Very minimalistic template plugin that displays a
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

## Why not Node.js?

You too.
