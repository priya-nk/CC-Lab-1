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
9. [Engineering Recommendation](#9-engineering-recommendation)
10. [Repository Structure](#10-repository-structure)

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
<img width="824" height="705" alt="image" src="https://github.com/user-attachments/assets/6eb21f62-2c9a-4f5e-8be8-4f3ae3635fde" />

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
5. **Verification**: Used `hostnamectl`, `lscpu`, `free -h`, and `df -h` to verify 2 Cores, 2GB RAM, and 20GB Disk.

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
sudo apt update
sudo apt install sysbench -y
sysbench cpu --cpu-max-prime=20000 run
```

### 5. Sysbench Screenshot Comparison

Raw console verification of the benchmark results:

* **Proxmox VE Output:** `images/1.png`
* **VMware Workstation Output:** `images/2.png`

---

### 6. Performance Comparison Table

The table below summarizes the exact values recorded during the benchmark:

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | 
| :--- | :--- | :--- | :--- |
| **Total Execution Time** | 9.9943 sec | 10.0006 sec | 
| **Total Events Processed** | 14,548 | 7,077 | 
| **Events per Sec (Throughput)** | 1,453.98 | 707.43 | 
| **Minimum Latency** | 0.57 ms | 1.16 ms | 
| **Average Latency** | 0.69 ms | 1.41 ms | 
| **Maximum Latency** | 1.24 ms | 9.00 ms | 

---

### 7. Graphs

Visualizations mapping the throughput, total events, and comprehensive latency metrics can be found in the `images/` directory and are fully rendered in `LAB_REPORT.md` / `performance-analysis.md`.

---

### 8. Takeaway & Conclusion



#### 9. Engineering Recommendation
* **Use Type-1 Hypervisors (Proxmox, ESXi):** Ideal for cloud infrastructure, enterprise data centers, and heavy computational workloads.
* **Use Type-2 Hypervisors (VMware Workstation, VirtualBox):** Ideal for local desktop development, software testing, and educational environments.

---

### 10. Repository Structure

```text

```
