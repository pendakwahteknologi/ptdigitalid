import socket
import jwt

SECRET_KEY = "supersecretkey"

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def main():
    service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_socket.bind(('0.0.0.0', 65433))  # Listen on all available interfaces
    service_socket.listen()

    print("Service is listening on port 65433...")

    while True:
        client_socket, addr = service_socket.accept()
        print(f"Connected by {addr}")

        token = client_socket.recv(1024).decode()
        print("Token received:", token)

        verification_result = verify_token(token)
        if isinstance(verification_result, dict):
            identity_card_number = verification_result.get("identity_card_number", "Unknown")
            response = f"Authenticated user with Identity Card Number {identity_card_number} via PTDigital ID SSO. Login allowed to service.pendakwah.tech."
        else:
            response = verification_result

        client_socket.sendall(response.encode())
        client_socket.close()

if __name__ == "__main__":
    main()
