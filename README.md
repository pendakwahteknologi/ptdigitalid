# PTDigital ID

Welcome to the **PTDigital ID** project! This repository demonstrates a Single Sign-On (SSO) system using Python. It includes an Identity Provider (IdP) server, a client application, and a service that interacts with the client through the IdP.

## Overview

**PTDigital ID** is a simplified SSO system that:
- Registers users via an Identity Provider server.
- Issues tokens to authenticated users.
- Allows users to access services using their tokens.

### Features

- **Identity Provider Server**: Generates key pairs, certificates, and tokens.
- **Client**: Registers with the IdP server using an identity card number and simulated biometric scans (thumbprint and face). Logs in to the service using a token.
- **Service**: Verifies tokens and authenticates clients, providing access to resources.

## Setup and Installation

### Prerequisites

- Python 3.x
- `pip3` package manager

### Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/PTDigitalID.git
   cd PTDigitalID

2. **Install the necessary Python packages:
   ```sh
    sudo apt update
    sudo apt install python3-pip
    pip3 install cryptography pyjwt

## Running the Project

### Start the Identity Provider Server
    python3 idp_server.py

### Start the Service
    python3 service.py

### Run the Client
    python3 client.py

## Registration

1. Run the client and choose the option to generate a certificate.
2. Enter your identity card number.
3. Perform the simulated thumbprint and face scans.

## Login to Service

1. Run the client and choose the option to log in to the service.
2. Enter the IP address and port number of the service. If left blank, it defaults to `service.pendakwah.tech` (simulated).
3. The service will authenticate the client and display a confirmation message.

## Code Explanation

### Identity Provider Server (`idp_server.py`)

The server listens for connections from clients, generates a key pair and certificate for the client, and issues a token. It sends the private key, certificate, and token back to the client.

### Client (`client.py`)

The client registers with the IdP server by providing an identity card number and performing simulated biometric scans. It stores the received private key, certificate, and token. The client can also log in to the service using the stored token.

### Service (`service.py`)

The service listens for connections from clients and verifies the received token. Upon successful verification, it authenticates the client and responds with a confirmation message, mentioning "service.pendakwah.tech".

## License

This project is licensed under the MIT License.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
