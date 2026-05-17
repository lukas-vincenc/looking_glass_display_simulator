# Looking Glass Display Simulator

A Blender Extension allowing the user to simulate and experiment 
with holographic display technology like Looking Glass Displays for 
example.

# Install from Blender Extension Store

1. Open Blender
2. `Edit` > `Preferences`
3. Select `Get Extensions` in the left sidebar
4. Search for `"Looking Glass Display Simulator"`
5. Press `"Install"`

The extension should now be ready-to-use. New tabs should appear
in the right-hand side of the main window. If nothing happened, 
make sure the checkbox is checked next to the add-on name in 
the add-ons list.

# Manual Installation

1. Download this repository as a ZIP file
2. Open Blender
3. `Edit` > `Preferences`
4. Select `Add-ons` in the left sidebar
5. In the top right corner, press the arrow icon to view a pop-up menu
6. Press `Install from Disk...`
7. In your installed files, find the downloaded ZIP and select it
8. Done

The extension should now be ready-to-use. New tabs should appear
in the right-hand side of the main window. If nothing happened, 
make sure the checkbox is checked next to the add-on name in 
the add-ons list.

# Usage

The extension introduces two main tabs - `QuiltMaker` and `LKGDisplaySim`.

The workflow should be as follows:

```
Create a scene you'd like to display
                |
                V
Use QuiltMaker to spawn cameras and 
calibrate to your liking
                |
                V
Render a quilt
                |
                V
Open new scene and the LentDisplay tab
                |
                V
Select the quilt using the file picker
                |
                V
Spawn Display and observe holographic effect
in the Rendered Viewport
            |       ^
            V       |
Play around with different lens, display
and image settings
```

Additionally, a third tab called `LensVisualization` is provided. It may be used to 
simulate a cylindrical lens and observe how it refracts light.


# Known issues

### Blender freezes when rendering the quilt.

After pressing the Render button Blender seems to freeze,
but it's working in the background. A progress bar appears
in the bottom left corner to indicate it's working. 
Once it's done, it unfreezes. So far, no solution has been found.
