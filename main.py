import json
import os
from VisualizingSkeleton import visualize_skeletons
from PeakAlignment import PeakAlignment
from AngleAlignment import compute_angle_alignment
Laptop = "SkeletonFiles/skeleton-dev-tool_2025-06-11_160519_ec07a639f22bf8_na_3f7102e31cd7d5_1749672319100.json"
Iphone = "SkeletonFiles/skeleton-dev-tool_2025-06-11_160520_b0d629a2b65078_na_689882f6bcef4a_1749672320851.json"
project_dir = os.path.dirname(os.path.abspath(__file__))
laptop_file = os.path.join(project_dir, Laptop)
iphone_file = os.path.join(project_dir, Iphone)
with open(laptop_file, 'r') as f:
    laptop_data = json.load(f)
with open(iphone_file, 'r') as f:
    iphone_data = json.load(f)
offset1 = PeakAlignment(laptop_data, iphone_data)
print(f"Peak Alignment:  {offset1}")
offset2 = compute_angle_alignment(laptop_data, iphone_data)
print(f"Angle Alignment:  {offset2[0]}")
visualize_skeletons(laptop_data, iphone_data, manual_offset=offset1)
#blue: 160(-50.71, 160), 209(-57.93, 207), 260(-58.23, 255)