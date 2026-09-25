import matplotlib.pyplot as plt
import os
import numpy as np

# Ensure the output directory 'images/' exists in the parent folder
output_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
os.makedirs(output_dir, exist_ok=True)

# Data based on the Lab Results
hypervisors = ['Proxmox VE (Type-1)', 'VMware Workstation (Type-2)']
eps = [1716.69, 1364.78]
total_events = [17169, 13650]

latency_min = [0.57, 0.67]
latency_avg = [0.58, 0.73]
latency_max = [2.78, 4.06]

# 1. CPU Throughput (Events per Second)
plt.figure(figsize=(8, 5))
bars = plt.bar(hypervisors, eps, color=['#2ca02c', '#1f77b4'])
plt.title('CPU Throughput Comparison (Events per Second)')
plt.ylabel('Events per Second')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 20, round(yval, 2), ha='center', va='bottom', fontweight='bold')
plt.savefig(os.path.join(output_dir, 'events_per_second_comparison.png'), bbox_inches='tight')
plt.close()

# 2. Total Events Processed
plt.figure(figsize=(8, 5))
bars = plt.bar(hypervisors, total_events, color=['#2ca02c', '#1f77b4'])
plt.title('Total Events Processed (in 10 seconds)')
plt.ylabel('Total Events')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, yval, ha='center', va='bottom', fontweight='bold')
plt.savefig(os.path.join(output_dir, 'total_events_comparison.png'), bbox_inches='tight')
plt.close()

# 3. Latency Metrics Comparison
x = np.arange(len(hypervisors))
width = 0.25

plt.figure(figsize=(10, 6))
bar1 = plt.bar(x - width, latency_min, width, label='Min Latency', color='#ff7f0e')
bar2 = plt.bar(x, latency_avg, width, label='Avg Latency', color='#d62728')
bar3 = plt.bar(x + width, latency_max, width, label='Max Latency', color='#9467bd')

plt.title('CPU Latency Comparison (Milliseconds)')
plt.ylabel('Latency (ms)')
plt.xticks(x, hypervisors)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

autolabel(bar1)
autolabel(bar2)
autolabel(bar3)

plt.savefig(os.path.join(output_dir, 'latency_comparison.png'), bbox_inches='tight')
plt.close()

print(f"Graphs successfully generated and saved in: {os.path.abspath(output_dir)}")
