import socket
import os
import hashlib
import random
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import load_pem_x509_certificate

def generate_random_data():
    # Generate random data to simulate biometric scans
    random_data = str(random.getrandbits(256)).encode('utf-8')
    hashed_data = hashlib.sha256(random_data).hexdigest()
    return hashed_data

def generate_certificate():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    identity_card_number = input("Enter Identity Card Number: ")
    input("Press any key to scan thumbprint...")
    print("Thumbprint scan successful.")
    thumbprint_scan = generate_random_data()

    input("Press any key to scan face...")
    print("Face scan successful.")
    face_scan = generate_random_data()

    message = f"{identity_card_number},{thumbprint_scan},{face_scan}"
    client_socket.sendall(message.encode())

    # Receive the private key and certificate from the server
    response = client_socket.recv(8192)  # Increased buffer size to ensure we receive all data
    private_key_pem, certificate_pem = response.split(b"===")

    # Store the private key and certificate
    with open("client_private_key.pem", "wb") as key_file:
        key_file.write(private_key_pem)
    with open("client_certificate.pem", "wb") as cert_file:
        cert_file.write(certificate_pem)

    # Receive the token from the server
    token_response = client_socket.recv(1024)
    token = token_response.split(b"===")[1]

    # Store the token
    with open("client_token.txt", "w") as token_file:
        token_file.write(token.decode())

    print("Registration complete. Token received and stored.")

    client_socket.close()

def access_service():
    ip = input("Enter service IP (leave empty for service.pendakwah.tech): ")
    if not ip:
        ip = "127.0.0.1"
        print("Connecting to service.pendakwah.tech...")
    else:
        print(f"Connecting to {ip}...")

    port = int(input("Enter service port: "))

    # Load the token
    with open("client_token.txt", "r") as token_file:
        token = token_file.read()

    service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_socket.connect((ip, port))

    # Send the token to the service
    service_socket.sendall(token.encode())

    response = service_socket.recv(1024).decode()
    print("Response from service:", response)

    service_socket.close()

def main():
    if not os.path.exists("client_private_key.pem") or not os.path.exists("client_certificate.pem") or not os.path.exists("client_token.txt"):
        print("No existing ID found. Please register first.")
        generate_certificate()
    else:
        print("Existing ID found.")
    
    print("Options: ")
    print("1. Generate certificate")
    print("2. Login to service")

    choice = input("Enter your choice: ")
    if choice == '1':
        generate_certificate()
    elif choice == '2':
        access_service()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
