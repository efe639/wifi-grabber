import subprocess

# Show all wifi profiles
def show_wifi_profiles():
    wifi_profiles = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="replace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in wifi_profiles if "All User Profile" in i]
    return profiles

# Connect to wifi network
def connect_to_wifi():
    wifi_profiles = show_wifi_profiles()
    if len(wifi_profiles) == 0:
        print("No wifi profiles found")
        return
    print("Available profiles:")
    for i, profile in enumerate(wifi_profiles):
        print("{}. {}".format(i + 1, profile))
    print("Already connected to wifi: ", get_wifi_network_name())
    choice = int(input("Enter profile number: "))
    if choice > len(wifi_profiles):
        print("Invalid choice")
        return
    connect_to_profile(wifi_profiles[choice - 1])
    print("Connecting to {}".format(wifi_profiles[choice - 1]))
    print("Type 'connect' to connect to wifi again or 'exit' to exit")
    while True:
        choice = input("Enter choice: ")
        if choice == "connect":
            connect_to_wifi()
        elif choice == "exit":
            break
        else:
            print("Invalid choice")
            continue

# Connect to wifi profile
def connect_to_profile(profile):
    subprocess.call(['netsh', 'wlan', 'connect', profile])

# Get wifi network name
def get_wifi_network_name():
    network_name = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8', errors="replace").split('\n')
    for line in network_name:
        if "SSID" in line:
            return line.split(":")[1][1:-1]
    return None

# Single profile password grabber
def get_wifi_profile_password(profile):
    password = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="replace").split('\n')
    for line in password:
        if "Key Content" in line:
            return line.split(":")[1][1:-1]
    return None

# Grab all wifi passwords
def wifi_password_grabber():
    password_list = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="replace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in password_list if "All User Profile" in i]
    passwords = []
    for profile in profiles:
        password = get_wifi_profile_password(profile)
        if password is not None:
            passwords.append((profile, password))
        else:
            passwords.append((profile, "No password"))
    return passwords
    
