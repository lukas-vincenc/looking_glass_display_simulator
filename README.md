# Looking Glass Display Simulator

A Blender Extension allowing the user to simulate and experiment 
with holographic display technology like Looking Glass Displays for 
example.

# Installation

# Usage

The extension introduces two tabs - `QuiltMaker` and `LentDisplay`.

The workflow should be as follows:

```
Create a scene you'd like to display
                |
                V
Use QuiltMaker to spawn cameras and 
calibrate to your liking
                |
                V
Render Display Image (set pitch, tilt...)
                |
                V
Open new scene and the LentDisplay tab
                |
                V
Select the Display Image using the file picker
                |
                V
Calibrate aspect ratio and lens params to match the image
                |
                V
Spawn Display and observe holographic effect
in the Rendered Viewport
```


# Known issues

## Blender freezes when rendering the quilt or the display image.

After pressing the Render button Blender seems to freeze,
but it's working silently in the background. Once it's done, 
it unfreezes. So far I don't have a solution for this one, 
but I have some things to experiment with.

## Tilt is a little imprecise.

Tested out a display image render out with the tilt of 11 degrees.
The display with lens tilted exactly 11 degrees displays the image,
however it's a little imprecise. In this case, 11.05 degrees turned
out to be more precise.

At this point I don't have a solution for this, and I'm not sure 
that I'll have one. My suspicion is that that's caused by some 
rounding errors in the background.

# TODO

- Speed up the display image rendering (currently a 4K image took around 7 minutes to render on my PC)
- Correct shape of the display
- Lenses don't cover the entire screen
- Extracting pitch, tilt... from the image itself?
- Create utils for calculating lens dimensions and so on
