import paramiko
import getpass
import time

# Accept SSH username and password
username = input("Enter SSH username: ")
password = getpass.getpass("Enter SSH password: ")
device = input("Enter device IP or hostname: ")

# Create SSH client object
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to device
print("Connecting to device...")
ssh.connect(hostname=device, username=username, password=password)


# Selectively simulate hardware component failure
# Usage: simulate_failure(failure_type, device_name, slot_number)

def simulate_failure(failure_type, device_name, slot_number):
    # Create shell channel
    channel = ssh.invoke_shell()
    time.sleep(2)

    # Send command to enter configuration mode
    channel.send("configure terminal\n")
    time.sleep(2)

    # Send command to simulate failure based on failure type
    if failure_type == "Link":
        # Simulate Link failure for interface Hu0/0/0/38/<number>
        command = "interface Hu0/0/0/38/{}\nshutdown\n".format(slot_number)
    elif failure_type == "Power Supply":
        # Simulate Power Supply Failure for ASR-9900-AC-PEM
        command = "poweroff module {} all\n".format(device_name)
    elif failure_type == "Fan Tray":
        # Simulate Fan Tray Failure for ASR-9902-FAN
        command = "environmental-fan-failure slot {}\n".format(slot_number)
    elif failure_type == "RP Active":
        # Simulate RP (Route Processor) Failure for A99-RP-F (Active)
        command = "redundancy force-switchover\n"
    elif failure_type == "RP Standby":
        # Simulate RP (Route Processor) Failure for A99-RP-F (Standby)
        command = "redundancy reload peer\n"
    elif failure_type == "Line Card":
        # Simulate Line Card Failure for ASR-9902-LC
        command = "hw-module slot {} shutdown\n".format(slot_number)
    elif failure_type == "LDC Node":
        # Simulate LDC Node Failure
        command = "reload ldc-node {}\n".format(device_name)
    elif failure_type == "AR1 reload":
        # Simulate reload for AR1
        command = "reload slot {}\n".format(slot_number)
    elif failure_type == "AR2 reload":
        # Simulate reload for AR2
        command = "reload slot {}\n".format(slot_number)
    else:
        print(
            "Invalid failure type specified. Allowed values: Link, Power Supply, Fan Tray, RP Active, RP Standby, Line Card, LDC Node, AR1 reload, AR2 reload")
        return

    # Send command to simulate failure
    channel.send(command)
    time.sleep(2)

    # Send command to exit configuration mode
    channel.send("exit\n")
    time.sleep(2)

    # Close the channel
    channel.close()

    print("Done.")


# Test the script
simulate_failure("Power Supply", "ASR-9902-AC-PEM", "1")
simulate_failure("Link", "Hu0/0/0/38", "2")

# Close the SSH connection
ssh.close()
