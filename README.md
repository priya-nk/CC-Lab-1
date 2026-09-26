# Cloud Computing - Lab 1: Hypervisor Performance Analysis

---

## Table of Contents
1. [Project Objectives](#1-project-objectives)
2. [Hypervisor Architectural Comparison](#2-hypervisor-architectural-comparison)
3. [Virtual Machine Specifications](#3-virtual-machine-specifications)
4. [Experimental Procedure & Pre-Setups](#4-experimental-procedure--pre-setups)
5. [Sysbench Screenshot Comparison](#5-sysbench-screenshot-comparison)
6. [Performance Comparison Table](#6-performance-comparison-table)
7. [Graphs](#7-graphs)
8. [Takeaway & Conclusion](#8-takeaway--conclusion)
9. [Repository Structure](#9-repository-structure)

---

## 1. Project Objectives
The primary objectives of this Cloud Computing laboratory experiment are:
1. **Deployment**: Provision two identical Ubuntu Virtual Machines across different hypervisor architectures:
   - **Type-1 (Bare-Metal)**: Proxmox VE
   - **Type-2 (Hosted)**: VMware Workstation Pro
2. **Standardization**: Enforce uniform hardware resource allocations to ensure direct comparability.
3. **Benchmarking**: Execute the `sysbench` CPU computational benchmark using 20,000 prime numbers to stress test CPU virtualization efficiency.
4. **Metric Collection**: Capture execution time, total events processed, throughput (events/sec), and latency statistics.
5. **Architectural Evaluation**: Quantify the performance overhead introduced by host operating system abstraction layers in Type-2 hypervisors versus bare-metal hypervisor execution.

---

## 2. Hypervisor Architectural Comparison

### Type-1 Hypervisor (Proxmox VE - Bare-Metal)
- **Architecture**: Operates directly on the physical server's hardware.
- **Mechanism**: Utilizes the Linux kernel integrated with KVM. Guest VM instructions execute directly on the hardware's CPU extensions.
- **Impact**: Minimal hypervisor interception eliminates heavy delays, offering native-like performance.

### Type-2 Hypervisor (VMware Workstation - Hosted)
- **Architecture**: Operates as a software application on top of an existing host OS (e.g., Windows).
- **Mechanism**: Privileged guest CPU operations undergo a double translation process through the VMware engine and the host OS kernel.
- **Impact**: The host OS scheduler introduces thread preemptions as the VM competes with background desktop services, leading to higher baseline latency.
<img width="800" height="800" alt="image" src="https://github.com/user-attachments/assets/fb4cdbc8-99e4-4902-8229-d8eea5ca7a61" />

---

## 3. Virtual Machine Specifications
To guarantee scientific accuracy and eliminate resource skewing, identical configurations were assigned to both VMs during setup:

| Resource Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) | 
| :--- | :--- | :--- | 
| **VM Name** | `CC-Experiment1-Type1` | `CC-Experiment1-Type2` | 
| **Guest OS** | Ubuntu 22.04 LTS (ISO) | Ubuntu 22.04 LTS (ISO) | 
| **CPU Allocation**| 2 vCPU (1 Socket, 2 Cores) | 2 vCPU (1 Processor, 2 Cores) | 
| **RAM Allocation**| 2048 MiB (2.0 GB) | 2048 MB (2.0 GB) | 
| **Virtual Disk** | 20.0 GB (`local-lvm`) | 20.0 GB (Single File) | 
| **Network Adapter**| Bridge (`vmbr0`) | NAT | 
| **Benchmark Tool** | `sysbench` | `sysbench` | 

---

## 4. Experimental Procedure & Pre-Setups

### Part A: Type-1 Hypervisor Setup (Proxmox VE)
1. **Access**: Logged into the Proxmox VE web interface via `https://<PROXMOX_SERVER_IP>:8006`.
2. **VM Creation Stages**: `General -> OS -> System -> Disks -> CPU -> Memory -> Network -> Confirm`
3. **Configuration**: 
   - **OS**: Selected `ubuntu-22.04.iso` from local storage.
   - **Disks**: Allocated 20 GB on `local-lvm`.
   - **CPU**: 1 Socket, 2 Cores (Total 2 vCPU).
   - **Memory**: 2048 MiB.
   - **Network**: Assigned to `vmbr0` bridge.
4. **Installation**: Started the VM, opened the Console, and completed the standard Ubuntu Normal Installation.
5. **Verification**: verify 2 Cores, 2GB RAM, and 20GB Disk:
   ``` bash
   hostnamectl # Displays and modifies system hostname and detailed OS/kernel metadata
   lscpu # Lists CPU architecture details (cores, threads, sockets, cache sizes)
   free -h # Shows total, used, and available RAM/Swap in human-readable units (e.g., GB)
   df -h # Displays disk space usage across mounted filesystems in human-readable units
   ```

### Part B: Type-2 Hypervisor Setup (VMware Workstation)
1. **Access**: Launched VMware Workstation and selected "Create a New Virtual Machine" (Typical Configuration).
2. **Configuration**:
   - **OS**: Mounted `ubuntu-22.04.iso`.
   - **Disks**: Set Maximum Disk Size to 20 GB (Stored as a single file).
   - **Hardware Customization**: Set Memory to 2048 MB, Processors to 1 (with 2 Cores), and Network Adapter to NAT.
3. **Installation**: Powered on the VM, erased the virtual disk, and completed the standard Ubuntu Normal Installation.
4. **Verification**: Executed the same terminal commands (`lscpu`, `free -h`) to confirm the identical allocation of hardware resources.

### Part C: Benchmark Execution
On both machines, the following commands were executed to run the test:
```bash
sudo apt update # Refreshes the local package index to fetch the latest available package lists from the repositories
sudo apt install sysbench -y # Installs the sysbench benchmarking tool automatically (-y skips the prompt)
sysbench cpu --cpu-max-prime=20000 run # Benchmarks CPU performance by calculating prime numbers up to 20,000
```

### 5. Sysbench Screenshot Comparison

Raw console verification of the benchmark results:

* **Proxmox VE Output:**
 <img width="1920" height="1020" alt="06-proxmox-sysbench-result" src="https://github.com/user-attachments/assets/f8871d7b-ad52-4645-a399-44c9e82bcfb0" />

* **VMware Workstation Output:**
<img width="1280" height="720" alt="04-vmware-sysbench-result" src="https://github.com/user-attachments/assets/1c074507-2512-4517-9f3c-54404ee4f17f" />
 

---

### 6. Performance Comparison Table

The table below summarizes the exact values recorded during the benchmark:
# Hypervisor Performance Comparison

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Delta | Percentage Change | Winner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Time** | 10.003 sec | 10.0013 sec | +0.0017 sec | — | — |
| **Total Events** | 14,548 | 6,399 | +8,149.00 | +127.35% | **Proxmox VE** |
| **Events / sec** | 1,453.98 | 639.70 | +814.28 | +127.29% | **Proxmox VE** |
| **Min Latency (ms)** | 0.57 | 1.19 | -0.62 | -52.10% | **Proxmox VE** |
| **Avg Latency (ms)** | 0.69 | 1.56 | -0.87 | -55.77% | **Proxmox VE** |
| **Max Latency (ms)** | 1.24 | 7.78 | -6.54 | -84.06% | **Proxmox VE** |

---

### Key Takeaway

Proxmox VE (Type-1) significantly outperformed VMware Workstation (Type-2) across all metrics, achieving **127.29% higher throughput** and **55.77% lower average latency**.

---

### 7. Graphs
Total events comparison:
<img width="1200" height="750" alt="total_events_comparison" src="https://github.com/user-attachments/assets/7dc54cb7-a984-440d-b23a-193f05c583a0" />

Events per second comparison:
<img width="1200" height="750" alt="events_per_second_comparison" src="https://github.com/user-attachments/assets/8c33b022-4603-4a3f-8bea-e42ceb620afe" />

Latency comparison:
<img width="1500" height="900" alt="latency_comparison" src="https://github.com/user-attachments/assets/e94c0a9d-3481-45ab-aa20-c24f68728987" />

Overall Performance:
<img width="1753" height="1392" alt="overall_performance_dashboard" src="https://github.com/user-attachments/assets/eac86367-387d-4815-ad36-403c4d6cbba4" />


---

### 8. Takeaway & Conclusion
#### 1. CPU Throughput

##### Results
- Proxmox: **14,548 events / 10s ≈ 1,454 events/s**
- VMware Workstation: **6,399 events / 10s ≈ 640 events/s**
- Proxmox achieved **~127% higher throughput**.

##### Technical Reason
- Proxmox runs directly on the hardware using KVM, avoiding the additional desktop host-OS layer present in VMware Workstation.

#### 2. Latency

##### Results
- Proxmox: **0.69 ms average**
- VMware: **1.56 ms average**
- VMware's average latency was **~2.3× higher**.
- Maximum latency: **7.78 ms vs 1.24 ms**, showing larger latency spikes in the VMware setup.

#### 3. Why the Difference?

##### Technical Explanation
- In VMware Workstation, the VM runs as a process managed by the **Windows host OS**.
- CPU scheduling, memory management, I/O, and host processes can introduce additional overhead and contention.
- Proxmox's KVM-based architecture provides a more direct virtualization path to the physical hardware.

#### 4. Conclusion

##### Key Findings
- The experiment demonstrates that **Proxmox performed better under this specific workload and configuration**.
- It does **not** prove that every Type-1 hypervisor is always faster than every Type-2 hypervisor.
- Proxmox is designed for **server/data-center virtualization**, while VMware Workstation is primarily designed for **desktop development, testing, and labs**.
  

#### Engineering Recommendation
* **Use Type-1 Hypervisors (Proxmox, ESXi):** Ideal for cloud infrastructure, enterprise data centers, and heavy computational workloads.
* **Use Type-2 Hypervisors (VMware Workstation, VirtualBox):** Ideal for local desktop development, software testing, and educational environments.

---

### 9. Repository Structure

```text
CE-Experiment-01-Hypervisor-Analysis/
│
├── results/
│   └── performance-analysis.md
│
├── screenshots/
│   │
│   ├── comparison/
│   │   ├── 01-hypervisor-performance-comparison.png
│   │   ├── events_per_second_comparison.png
│   │   ├── latency_comparison.png
│   │   ├── overall_performance_dashboard.png
│   │   └── total_events_comparison.png
│   │
│   ├── type1-proxmox/
│   │   ├── 01-proxmox-dashboard.jpeg
│   │   ├── 02-proxmox-vm-configuration.jpeg
│   │   ├── 03-proxmox-vm-running.jpeg
│   │   ├── 04-proxmox-ubuntu-console.jpeg
│   │   ├── 05-01-proxmox-system-configuration.png
│   │   ├── 05-02-proxmox-system-configuration.png
│   │   ├── 06-proxmox-bench-result.png
│   │   ├── 07-01proxmox-resource-monitoring.png
│   │   ├── 07-02-proxmox-resource-monitoring.png
│   │   ├── 07-03-proxmox-resource-monitoring.png
│   │   └── 07-04proxmox-resource-monitoring.png
│   │
│   └── type2-vmware/
│       ├── 01-vmware-vm-configuration.png
│       ├── 02-vmware-vm-running.png
│       ├── 03-vmware-system-configuration.jpeg
│       ├── 04-vmware-sysbench-result.jpeg
│       └── README.md
│
├── scripts/
│   ├── benchmark.sh
│   ├── generate_plots.py
│   └── parse_sysbench.py
│
└── README.md
```
