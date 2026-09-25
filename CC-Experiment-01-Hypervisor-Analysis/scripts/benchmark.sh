#!/bin/bash
# =============================================================
# Sysbench CPU Benchmark Script
# Cloud Computing Lab 1 - Hypervisor Performance Analysis
# =============================================================

echo "============================================="
echo "  Sysbench CPU Benchmark - Hypervisor Lab"
echo "============================================="

echo ""
echo "[1/3] Updating package repository..."
sudo apt update -y

echo ""
echo "[2/3] Installing sysbench..."
sudo apt install sysbench -y

echo ""
echo "[3/3] Verifying installation..."
sysbench --version

echo ""
echo "============================================="
echo "  Running CPU Benchmark (20,000 primes)"
echo "============================================="
echo ""
sysbench cpu --cpu-max-prime=20000 run

echo ""
echo "Benchmark complete. Record the results above."
