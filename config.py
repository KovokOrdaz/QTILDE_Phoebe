
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#LIB AUTOSTART
import os
import subprocess

from libqtile import bar, layout, widget, hook, drawer
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()
color_nav = "#171717"
size_nav = 28
font_nav = "VictorMono"
size_font = 12
size_icon = 18
foreground_icon = "#177117"
color_active = "#0877ff"
color_inactive = "#d5eff7"
color_current = "#711711"
color_warning = "#ec7425"
color_info = "#085ac1"
color_tokken = "#1aba56"
color_colmax = "#c4150d"
device_network = "wlan0"

def separator():
    return widget.Sep(
        linewidth = 0,
        padding = 6,
        foreground = "#000000"
    )

def border_box(color, type):
    if type == 0:
        icon = ""
    else:
        icon = ""
    return widget.TextBox( 
        text = icon,
        fontsize = 24,
        foreground = color,
        #background = color_inactive
        padding = 0
    )

def icon_box(color, icon):
    return widget.TextBox( 
        text = icon,
        fontsize = size_font,
        foreground = color_inactive,
        background = color
    )

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    #Key Custom
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Show Rofi"),
    
    #Key Special
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Up Volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Down Volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Un/Mute Volume"),
    Key([mod], "s", lazy.spawn("scrot"), desc="Capqture Screen"),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s"), desc="Capture Screen"),
]

groups = [Group(i) for i in [
    "  ",
    "  ", 
    "  ",
    "  ", 
    "  ",
    "  ",
    "  "
    ]]

for i, group in enumerate(groups):
    number_desktop = str(i+1) 
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                number_desktop,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                number_desktop,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=font_nav,
    fontsize=size_font,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active = color_active,
                    inactive = color_inactive,
                    disable_drag = True, 
                    border_width = 1, 
                    fontsize= size_icon, 
                    foreground = foreground_icon, 
                    highlight_method = 'text',
                    margin_x = 0,
                    margin_y = 5,
                    other_screen_border = color_current,
                    this_current_screen_border = color_current,
                    padding_x = 3,
                    padding_y = 10
                    ),
                separator(),
                widget.Prompt(),
                widget.WindowName(
                    foreground = color_active,
                ),
                separator(),
                widget.Systray(
                    icon_size = 18,
                ),

                separator(),
                border_box(color_warning, 0),
                icon_box(color_warning, ""),
                widget.ThermalSensor(
                    foreground = color_inactive,
                    background = color_warning,
                    threshold = 50,
                    tag_sensor = "Core 0",
                    fmt = 'T0:  {}'
                ),
                widget.ThermalSensor(
                    foreground = color_inactive,
                    background = color_warning,
                    threshold = 50,
                    tag_sensor = "Core 1",
                    fmt = 'T1:  {}'
                ),
                icon_box(color_warning, ""),
                widget.Memory(
                    Foreground = color_inactive,
                    background = color_warning,
                ),
                border_box(color_warning, 1),
                separator(),

                border_box(color_info, 0),
                icon_box(color_info, "痢"),
                widget.CheckUpdates(
                    background = color_info,
                    colour_have_updates = color_inactive,
                    colour_no_updates = color_inactive,
                    no_update_string = '',
                    display_format = "{updates}",
                    update_intervale = 18000,
                    distro = "Arch"
                ),
                icon_box(color_info, "龍"),
                widget.Net(
                    foreground = color_inactive,
                    background = color_info,
                    format = " {up}       {down}",
                    interface = device_network,
                    use_bits = 'true'
                ),
                border_box(color_info, 1),
                separator(),

                border_box(color_tokken, 0),
                widget.Clock(
                    foreground = color_inactive,
                    background = color_tokken,
                    format = "%Y/%m/%d %I:%M %p"
                    ),
                icon_box(color_tokken, ""),
                widget.PulseVolume(
                    foreground = color_inactive,
                    background = color_tokken,
                    fontsize = size_font,
                    limit_max_volume = True
                ),
                border_box(color_tokken, 1),
                separator(),

                border_box(color_colmax, 0),
                widget.CurrentLayoutIcon(
                    background = color_colmax,
                    scale = 0.6
                ),
                widget.CurrentLayout(
                    background = color_colmax
                ),
                border_box(color_colmax, 1),
                #widget.QuickExit(),
            ],
            size_nav,
            background = color_nav,
            #opacity = 0,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])