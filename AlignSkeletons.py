from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

def AlignSkeletons(laptop_file, iphone_file):
    flippedLap = [-y for y in extractYValues(laptop_file)]
    flippedIphone = [-y for y in extractYValues(iphone_file)]

    lapPeaks = list(getOrderedTopPeaks(flippedLap, 6, 100, 1500))
    iphonePeaks = list(getOrderedTopPeaks(flippedIphone,6, 50, 1500))
    print("Laptop Peaks:", lapPeaks)
    print("iPhone Peaks:", iphonePeaks)
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_peaks(ax, flippedLap, lapPeaks, label="Laptop", color="blue")
    plt.title("Laptop Head Y Trajectory with Peaks")
    plt.show()
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_peaks(ax, flippedIphone, iphonePeaks, label="Iphone", color="blue")
    plt.title("Iphone Head Y Trajectory with Peaks")
    plt.show()
    lapFrames = [frame for _, frame in lapPeaks]
    iphoneFrames = [frame for _, frame in iphonePeaks]
    offsets = [i - l for l, i in zip(lapFrames, iphoneFrames)]
    avg_offset = int(round(sum(offsets) / len(offsets)))
    return avg_offset

def extractYValues(file):
    YList = []
    for frame in file:
        joint_coords = frame.get("top_of_the_head", [-100, -100])
        y = joint_coords[1]
        YList.append(y if y != -100 and y != 100 else np.nan)  # keep placeholder for missing
    return YList



def getOrderedTopPeaks(y_list, num_peaks, start_frame, end_frame):
    y_list_trimmed = y_list[start_frame:end_frame]
    peaks, _ = find_peaks(y_list_trimmed, distance=20)
    peak_values = [(y_list_trimmed[p], p + start_frame) for p in peaks]
    peak_values.sort(reverse=True, key=lambda x: x[0])
    top_peaks = peak_values[:num_peaks]
    top_peaks.sort(key=lambda x: x[1])

    return top_peaks

def plot_peaks(ax, y_list, peaks, label="", color="blue"):
    ax.plot(range(len(y_list)), y_list, label=label, color=color)
    peak_indices = [p[1] for p in peaks]
    peak_values = [p[0] for p in peaks]
    ax.scatter(peak_indices, peak_values, color="red", marker="o", s=40, label=f"{label} Peaks")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Flipped Y (Head Height)")
    ax.legend()