# Rotation Calculator:
A blender add-on that can be used to visualize rotations in 3 dimensions.  Useful applications include visualizing rotations on the bloch sphere corresponding to quantum operators on a single qbit.
## List of Features:

### Visualize Rotations in Real Time
![example_1.gif](example-imgs/example_1.gif)
### Automatically Render Scene Before and After Rotation
The add-on automatically renders a before and after shot of the scene, conveniently stitching them into a single image for later analysis.

![example_2.png](example-imgs/example_2.png)

The render is stored as `rotated.png` in the file location in which blender is run.
### TODO: Allow User to Set the Initial Rotation of the Vector Relative to It's Default Orientation
This feature currently exists, but rotations still follow relative axes rather than the global axes.