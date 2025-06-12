import numpy as np

def extract_joint_angles(frame_data):
    """Extracts knee, elbow, hip, and shoulder angles from a frame."""

    def compute_angle(joint_a, joint_b, joint_c):
        """Computes the angle between three joints, handling missing data."""
        if any(j is None or j == [-100, -100] for j in [joint_a, joint_b, joint_c]):
            return None  # Missing data
        a, b, c = np.array(joint_a), np.array(joint_b), np.array(joint_c)
        ab = a - b
        cb = c - b

        norm_ab = np.linalg.norm(ab)
        norm_cb = np.linalg.norm(cb)

        if norm_ab == 0 or norm_cb == 0:  # Avoid division by zero
            return None

        cosine_angle = np.dot(ab, cb) / (norm_ab * norm_cb)
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0)) * 180.0 / np.pi
        return angle

    knee_angle = compute_angle(
        frame_data.get("left_hip"), frame_data.get("left_knee"), frame_data.get("left_ankle")
    )
    elbow_angle = compute_angle(
        frame_data.get("left_shoulder"), frame_data.get("left_elbow"), frame_data.get("left_wrist")
    )
    hip_angle = compute_angle(
        frame_data.get("right_shoulder"), frame_data.get("left_hip"), frame_data.get("right_hip")
    )
    shoulder_angle = compute_angle(
        frame_data.get("left_elbow"), frame_data.get("left_shoulder"), frame_data.get("right_shoulder")
    )

    return knee_angle, elbow_angle, hip_angle, shoulder_angle


def compute_angle_alignment(skeleton1, skeleton2, max_offset=101):
    best_offset = 0
    min_diff = float("inf")
    offset_results = {}

    for offset in range(max_offset):
        total_diff = 0
        count = 0

        max_valid_i = min(len(skeleton1), len(skeleton2) - offset)
        if max_valid_i <= 0:
            offset_results[offset] = float("inf")
            continue

        for i in range(max_valid_i):
            frame1 = skeleton1[i]
            frame2 = skeleton2[i + offset]

            angles1 = extract_joint_angles(frame1)
            angles2 = extract_joint_angles(frame2)

            frame_diff = []
            for a1, a2 in zip(angles1, angles2):
                if a1 is not None and a2 is not None:  # Skip invalid frames
                    frame_diff.append(abs(a1 - a2))
                    total_diff += abs(a1 - a2)
                    count += 1

            offset_results[offset] = np.mean(frame_diff) if frame_diff else float("inf")

        avg_diff = total_diff / count if count > 0 else float("inf")  # Avoid division by zero

        if avg_diff < min_diff:
            min_diff = avg_diff
            best_offset = offset

    return best_offset, offset_results


# **Allow script to be executed directly**
if __name__ == "__main__":
    import json
    import os

    # Default file paths for testing (modify as needed)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    laptop_file = os.path.join(project_dir, "Skeletons/SquatFrontal1/2025-02-05_145057_apearle43@gmail.com_4875-Squat_Front_-_1738788657784.json")
    iphone_file = os.path.join(project_dir, "Skeletons/SquatFrontal1/2025-02-05_145057_apearle43@gmail.com_4875-Squat_Front_-_1738788657666.json")

    # Load JSON data
    with open(laptop_file, 'r') as f:
        skeleton_laptop = json.load(f)
    with open(iphone_file, 'r') as f:
        skeleton_iphone = json.load(f)

    # Run frame matching
    best_offset, offset_results = compute_angle_differences(skeleton_laptop, skeleton_iphone)
    print(f"✅ Best Offset Found: {best_offset} (Min Avg Angle Difference: {offset_results[best_offset]})")
