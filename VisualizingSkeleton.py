import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Use TkAgg to ensure animation works properly
matplotlib.use("TkAgg")

# Define skeleton connections for visualization
connections = [
    ("nose", "top_of_the_head"), ("nose", "chin"), ("chin", "neck"),
    ("neck", "left_shoulder"), ("neck", "right_shoulder"),
    ("left_shoulder", "left_elbow"), ("right_shoulder", "right_elbow"),
    ("left_elbow", "left_wrist"), ("right_elbow", "right_wrist"),
    ("neck", "left_hip"), ("neck", "right_hip"),
    ("left_hip", "left_knee"), ("right_hip", "right_knee"),
    ("left_knee", "left_ankle"), ("right_knee", "right_ankle"),
    ("left_ankle", "left_bigtoe"), ("right_ankle", "right_bigtoe"),
    ("left_ankle", "left_heel"), ("right_ankle", "right_heel"),
]

important_joints = {
    "nose": "Head", "left_wrist": "Left Hand", "right_wrist": "Right Hand",
    "left_ankle": "Left Foot", "right_ankle": "Right Foot",
    "left_hip": "Left Hip", "right_hip": "Right Hip"
}

angle_joints = {
    "Left Elbow": ("left_shoulder", "left_elbow", "left_wrist"),
    "Right Elbow": ("right_shoulder", "right_elbow", "right_wrist"),
    "Left Knee": ("left_hip", "left_knee", "left_ankle"),
    "Right Knee": ("right_hip", "right_knee", "right_ankle")
}

def plot_skeleton(ax, data, color):
    """Plots a skeleton with connections and labels important joints."""
    for joint1, joint2 in connections:
        if joint1 in data and joint2 in data:
            p1, p2 = data[joint1], data[joint2]
            if p1 != [-100, -100] and p2 != [-100, -100]:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=2)

    for joint, coord in data.items():
        if coord != [-100, -100]:
            ax.scatter(*coord, color=color, s=20)

    for joint, label_text in important_joints.items():
        if joint in data and data[joint] != [-100, -100]:
            ax.text(data[joint][0], data[joint][1], label_text, fontsize=8, color=color)

def visualize_skeletons(laptop_file, iphone_file, manual_offset):
    if manual_offset >= 0:
        laptop_frames = laptop_file
        iphone_frames = iphone_file[manual_offset:]
    else:
        laptop_frames = laptop_file[-manual_offset:]
        iphone_frames = iphone_file
    frames = min(len(laptop_frames), len(iphone_frames))
    reference_anchor = get_mid_hip(laptop_frames[0])

    fig, ax = plt.subplots(figsize=(10, 12))

    def update(frame):
        ax.clear()
        skel1 = shift_skeleton(laptop_frames[frame], reference_anchor)
        skel2 = shift_skeleton(iphone_frames[frame], reference_anchor)

        mid_x, mid_y = reference_anchor
        ax.set_xlim(mid_x - 300, mid_x + 300)
        ax.set_ylim(mid_y + 300, mid_y - 300)
        ax.set_title(f"Frame {frame + 1}: Skeleton Comparison")

        plot_skeleton(ax, laptop_frames[frame], "blue")
        plot_skeleton(ax, iphone_frames[frame], "red")

        ax.legend([
            plt.Line2D([0], [0], color="blue", lw=4),
            plt.Line2D([0], [0], color="red", lw=4)
        ], ["Laptop", "iPhone"])

    ani = animation.FuncAnimation(fig, update, frames=range(0, frames, 2), interval=5)
    plt.show()

def shift_skeleton(data, anchor):
    """Shift skeleton so the mid-hip is at the origin."""
    mid_hip = get_mid_hip(data)
    shift_x, shift_y = anchor[0] - mid_hip[0], anchor[1] - mid_hip[1]

    return {joint: [coord[0] + shift_x, coord[1] + shift_y] if coord != [-100, -100] else coord
            for joint, coord in data.items()}

def get_mid_hip(data):
    """Calculate the midpoint of the hips for anchoring."""
    left_hip = data.get("left_hip", [-100, -100])
    right_hip = data.get("right_hip", [-100, -100])

    if left_hip != [-100, -100] and right_hip != [-100, -100]:
        return [(left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2]
    elif left_hip != [-100, -100]:
        return left_hip
    elif right_hip != [-100, -100]:
        return right_hip
    else:
        return [0, 0]  # Default anchor point