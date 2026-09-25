import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

# ---------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------
output_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------------------
# Benchmark Data
# ---------------------------------------------------------------
labels       = ['Proxmox VE\n(Type-1)', 'VMware Workstation\n(Type-2)']
colors       = ['#2ca02c', '#1f77b4']
eps          = [1716.69, 1364.78]
total_events = [17169,   13650]
lat_min      = [0.57,    0.67]
lat_avg      = [0.58,    0.73]
lat_p95      = [0.65,    0.89]
lat_max      = [2.78,    4.06]

# ---------------------------------------------------------------
# Helper: add value labels on bars
# ---------------------------------------------------------------
def label_bars(ax, bars, fmt='{:.2f}', pad=0.02):
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + pad,
            fmt.format(h),
            ha='center', va='bottom',
            fontweight='bold', fontsize=10
        )

# ---------------------------------------------------------------
# Chart 1 — CPU Throughput (Events per Second)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, eps, color=colors, width=0.4, edgecolor='black', linewidth=0.7)
label_bars(ax, bars, fmt='{:.2f}', pad=10)
ax.set_title('CPU Throughput Comparison (Events per Second)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Events per Second')
ax.set_ylim(0, max(eps) * 1.2)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'events_per_second_comparison.png'), dpi=150)
plt.close()
print("✔ Saved: events_per_second_comparison.png")

# ---------------------------------------------------------------
# Chart 2 — Total Events Processed
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, total_events, color=colors, width=0.4, edgecolor='black', linewidth=0.7)
label_bars(ax, bars, fmt='{:.0f}', pad=100)
ax.set_title('Total Events Processed (in 10 seconds)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Total Events')
ax.set_ylim(0, max(total_events) * 1.2)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'total_events_comparison.png'), dpi=150)
plt.close()
print("✔ Saved: total_events_comparison.png")

# ---------------------------------------------------------------
# Chart 3 — Latency Comparison (Min, Avg, 95th, Max)
# ---------------------------------------------------------------
x = np.arange(len(labels))
width = 0.18
fig, ax = plt.subplots(figsize=(10, 6))

b1 = ax.bar(x - 1.5*width, lat_min, width, label='Min Latency',    color='#ff7f0e', edgecolor='black', linewidth=0.7)
b2 = ax.bar(x - 0.5*width, lat_avg, width, label='Avg Latency',    color='#d62728', edgecolor='black', linewidth=0.7)
b3 = ax.bar(x + 0.5*width, lat_p95, width, label='95th Percentile',color='#9467bd', edgecolor='black', linewidth=0.7)
b4 = ax.bar(x + 1.5*width, lat_max, width, label='Max Latency',    color='#8c564b', edgecolor='black', linewidth=0.7)

for bars in [b1, b2, b3, b4]:
    label_bars(ax, bars, fmt='{:.2f}', pad=0.03)

ax.set_title('CPU Latency Comparison (Milliseconds)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Latency (ms)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, max(lat_max) * 1.35)
ax.legend(loc='upper right')
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'latency_comparison.png'), dpi=150)
plt.close()
print("✔ Saved: latency_comparison.png")

# ---------------------------------------------------------------
# Chart 4 — Overall Performance Dashboard (2x2 grid)
# ---------------------------------------------------------------
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Hypervisor Performance Dashboard\nProxmox VE (Type-1) vs VMware Workstation (Type-2)',
             fontsize=16, fontweight='bold', y=0.98)
gs = gridspec.GridSpec(2, 2, hspace=0.45, wspace=0.35)

# Panel 1: Throughput
ax1 = fig.add_subplot(gs[0, 0])
b = ax1.bar(labels, eps, color=colors, edgecolor='black', linewidth=0.7)
label_bars(ax1, b, fmt='{:.2f}', pad=10)
ax1.set_title('Events per Second', fontweight='bold')
ax1.set_ylabel('Events/sec')
ax1.set_ylim(0, max(eps) * 1.25)
ax1.grid(axis='y', linestyle='--', alpha=0.6)
ax1.spines[['top', 'right']].set_visible(False)

# Panel 2: Total Events
ax2 = fig.add_subplot(gs[0, 1])
b = ax2.bar(labels, total_events, color=colors, edgecolor='black', linewidth=0.7)
label_bars(ax2, b, fmt='{:.0f}', pad=100)
ax2.set_title('Total Events Processed', fontweight='bold')
ax2.set_ylabel('Total Events')
ax2.set_ylim(0, max(total_events) * 1.25)
ax2.grid(axis='y', linestyle='--', alpha=0.6)
ax2.spines[['top', 'right']].set_visible(False)

# Panel 3: Avg Latency
ax3 = fig.add_subplot(gs[1, 0])
b = ax3.bar(labels, lat_avg, color=['#2ca02c', '#1f77b4'], edgecolor='black', linewidth=0.7)
label_bars(ax3, b, fmt='{:.2f}', pad=0.01)
ax3.set_title('Average Latency (ms)', fontweight='bold')
ax3.set_ylabel('Latency (ms)')
ax3.set_ylim(0, max(lat_avg) * 1.4)
ax3.grid(axis='y', linestyle='--', alpha=0.6)
ax3.spines[['top', 'right']].set_visible(False)

# Panel 4: Full Latency Breakdown
ax4 = fig.add_subplot(gs[1, 1])
x = np.arange(len(labels))
w = 0.18
b1 = ax4.bar(x - 1.5*w, lat_min, w, label='Min',    color='#ff7f0e', edgecolor='black', linewidth=0.7)
b2 = ax4.bar(x - 0.5*w, lat_avg, w, label='Avg',    color='#d62728', edgecolor='black', linewidth=0.7)
b3 = ax4.bar(x + 0.5*w, lat_p95, w, label='95th',   color='#9467bd', edgecolor='black', linewidth=0.7)
b4 = ax4.bar(x + 1.5*w, lat_max, w, label='Max',    color='#8c564b', edgecolor='black', linewidth=0.7)
ax4.set_title('Latency Breakdown (ms)', fontweight='bold')
ax4.set_ylabel('Latency (ms)')
ax4.set_xticks(x)
ax4.set_xticklabels(labels)
ax4.set_ylim(0, max(lat_max) * 1.4)
ax4.legend(loc='upper right', fontsize=8)
ax4.grid(axis='y', linestyle='--', alpha=0.6)
ax4.spines[['top', 'right']].set_visible(False)

plt.savefig(os.path.join(output_dir, 'overall_performance_dashboard.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✔ Saved: overall_performance_dashboard.png")

print(f"\n✅ All graphs saved in: {os.path.abspath(output_dir)}")
