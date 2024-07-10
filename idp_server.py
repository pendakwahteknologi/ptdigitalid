import socket
import jwt
import time
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import (
    Name, NameAttribute, CertificateBuilder, BasicConstraints
)
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"

def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def create_certificate(public_key, private_key):
    subject = issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, u"MY"),
        NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Selangor"),
        NameAttribute(NameOID.LOCALITY_NAME, u"Cyberjaya"),
        NameAttribute(NameOID.ORGANIZATION_NAME, u"PTDigital ID"),
        NameAttribute(NameOID.COMMON_NAME, u"pendakwah.tech"),
    ])
    cert = CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(public_key).serial_number(1000).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=365)).add_extension(BasicConstraints(ca=True, path_length=None), critical=True).sign(private_key, hashes.SHA256())
    return cert

def create_token(identity_card_number):
    payload = {
        "identity_card_number": identity_card_number,
        "exp": time.time() + 600  # Token valid for 10 minutes
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))  # Listen on all available interfaces
    server_socket.listen()

    print("Identity Provider Server is listening on port 65432...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")

        data = client_socket.recv(1024).decode()
        identity_card_number, thumbprint_scan, face_scan = data.split(',')

        print(f"Received Identity Card Number: {identity_card_number}")
        print(f"Received Thumbprint Scan: {thumbprint_scan}")
        print(f"Received Face Scan: {face_scan}")

        private_key, public_key = generate_key_pair()
        certificate = create_certificate(public_key, private_key)

        # Send the private key and certificate to the client
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)

        client_socket.sendall(private_key_pem + b"===" + certificate_pem)

        # Issue token
        token = create_token(identity_card_number)
        client_socket.sendall(b"===" + token.encode())

        client_socket.close()

if __name__ == "__main__":
    main()
