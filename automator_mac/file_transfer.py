import paramiko
import os

def transfer_file(source_file):
    hostname = '10.0.0.16'
    username = 'mittalmak'
    password = 'q&A7ujtdAvP9Bb'  # Replace with your actual password
    destination_path = '/share/Download/JDownloader2/'

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        ssh.connect(hostname, username=username, password=password)

        # Use SFTP to transfer the file
        sftp = ssh.open_sftp()
        sftp.put(source_file, os.path.join(destination_path, os.path.basename(source_file)))
        sftp.close()

        print(f"File {source_file} successfully transferred to {destination_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <source_file>")
    else:
        transfer_file(sys.argv[1])