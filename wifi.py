import subprocess

def set_access_point_mode():
    # Step 1: Ensure Wi-Fi is enabled
    subprocess.run(['sudo', 'nmcli', 'radio', 'wifi', 'on'])

    # Step 2: Create the Access Point with the specified SSID and password
    result = subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'hotspot', 'ifname', 'wlan0', 'ssid', 'Neurotic', 'password', '12345678'], capture_output=True, text=True)    
    # Step 3: Check if there was an error creating the hotspot
    if result.returncode != 0:
        print(f"Error setting up hotspot: {result.stderr}")
        return
    
    # Step 4: Set a static IP address for the access point (local use only)
    subprocess.run(['sudo', 'nmcli', 'connection', 'modify', 'Hotspot', 'ipv4.addresses', '192.168.4.1/24'])
    subprocess.run(['sudo', 'nmcli', 'connection', 'modify', 'Hotspot', 'ipv4.gateway', '192.168.4.1'])
    subprocess.run(['sudo', 'nmcli', 'connection', 'modify', 'Hotspot', 'ipv4.method', 'manual'])

    # Step 5: Configure dnsmasq to handle DHCP in the range 192.168.4.10-192.168.4.20 with the gateway
    with open('/etc/dnsmasq.conf', 'w') as f:
        f.write("interface=wlan0\n")
        f.write("dhcp-range=192.168.4.10,192.168.4.20,255.255.255.0,24h\n")
        f.write("dhcp-option=3,192.168.4.1\n")  # Set the gateway to 192.168.4.1
    
    # Step 6: Restart dnsmasq to apply the new configuration
    subprocess.run(['sudo', 'systemctl', 'restart', 'dnsmasq'])
    
    # Step 7: Restart the access point connection
    subprocess.run(['sudo', 'nmcli', 'connection', 'up', 'Hotspot'])

    print("Switched to Access Point mode (local network with gateway 192.168.4.1 set).")

def set_wifi_client_mode():
    # Step 1: Disable the hotspot (if running)
    subprocess.run(['sudo', 'nmcli', 'connection', 'down', 'Hotspot'])

    # Step 2: Enable Wi-Fi and connect to a network using DHCP
    subprocess.run(['sudo', 'nmcli', 'radio', 'wifi', 'on'])

    # Optionally, connect to a known Wi-Fi network
    ssid = "Milos"
    password = "11111111"
    subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])

    print("Switched to Wi-Fi client mode (DHCP).")

# Example usage:
mode = input("Enter mode (ap/wifi): ").strip().lower()
if mode == "ap":
    set_access_point_mode()
elif mode == "wifi":
    set_wifi_client_mode()
else:
    print("Invalid mode. Please enter 'ap' or 'wifi'.")
