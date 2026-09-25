#!/bin/bash
# Sysbench CPU Benchmark Execution Script
# This script updates the package list, installs sysbench, and runs the CPU benchmark.

echo "Updating package repository..."
sudo apt update

echo "Installing sysbench..."
sudo apt install sysbench -y

echo "Verifying sysbench installation..."
sysbench --version

echo "Running sysbench CPU benchmark (20,000 prime numbers)..."
sysbench cpu --cpu-max-prime=20000 run
