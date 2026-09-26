# parse_sysbench.py
# Parses sysbench CPU benchmark results and compares Type-1 vs Type-2 hypervisors.

results = {
    "Proxmox VE (Type-1)": {
        "execution_time_sec": ,10.0030
        "total_events":       14548,
        "events_per_sec":     1453.98,
        "latency_min_ms":     0.57,
        "latency_avg_ms":     0.69,
        "latency_max_ms":     1.24,
    },
    "VMware Workstation (Type-2)": {
        "execution_time_sec": 10.0013,
        "total_events":       6399,
        "events_per_sec":     639.70,
        "latency_min_ms":     1.19,
        "latency_avg_ms":     1.56,
        "latency_max_ms":     7.78,
    },
}

def print_result(name, data):
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    print(f"  Execution Time   : {data['execution_time_sec']} sec")
    print(f"  Total Events     : {data['total_events']}")
    print(f"  Events / sec     : {data['events_per_sec']}")
    print(f"  Min Latency      : {data['latency_min_ms']} ms")
    print(f"  Avg Latency      : {data['latency_avg_ms']} ms")
    print(f"  Max Latency      : {data['latency_max_ms']} ms")

for name, data in results.items():
    print_result(name, data)

t1 = results["Proxmox VE (Type-1)"]
t2 = results["VMware Workstation (Type-2)"]

def delta(t1_val, t2_val, higher_is_better=True):
    diff = t1_val - t2_val
    pct  = (diff / t2_val) * 100
    if higher_is_better:
        winner = "Proxmox VE" if diff > 0 else "VMware"
    else:
        winner = "Proxmox VE" if diff < 0 else "VMware"
    return diff, pct, winner

print(f"\n\n{'='*50}")
print(f"  PERFORMANCE COMPARISON")
print(f"{'='*50}")

metrics = [
    ("Total Events",         "total_events",       True),
    ("Events per Second",    "events_per_sec",      True),
    ("Min Latency (ms)",     "latency_min_ms",      False),
    ("Avg Latency (ms)",     "latency_avg_ms",      False),
    ("Max Latency (ms)",     "latency_max_ms",      False),
]

for label, key, higher_is_better in metrics:
    diff, pct, winner = delta(t1[key], t2[key], higher_is_better)
    sign = "+" if diff > 0 else ""
    print(f"\n  {label}")
    print(f"    Proxmox VE : {t1[key]}")
    print(f"    VMware     : {t2[key]}")
    print(f"    Delta      : {sign}{diff:.2f}  ({sign}{pct:.2f}%)")
    print(f"    Winner     : {winner}")

print(f"\n{'='*50}")
print(f"  CONCLUSION")
print(f"{'='*50}")
eps_gain = ((t1['events_per_sec'] - t2['events_per_sec']) / t2['events_per_sec']) * 100
lat_gain = ((t2['latency_avg_ms'] - t1['latency_avg_ms']) / t2['latency_avg_ms']) * 100
print(f"\n  Proxmox VE (Type-1) achieved {eps_gain:.2f}% higher throughput")
print(f"  and {lat_gain:.2f}% lower average latency than VMware Workstation (Type-2).\n")
