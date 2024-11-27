#!/bin/bash

# Directory for SSL certificates
SSL_DIR="../nginx/ssl"

# Create SSL directory if it doesn't exist
mkdir -p $SSL_DIR

# Generate private key and certificate
openssl req -x509 \
    -nodes \
    -days 365 \
    -newkey rsa:2048 \
    -keyout $SSL_DIR/key.pem \
    -out $SSL_DIR/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
    -addext "subjectAltName = DNS:localhost,IP:127.0.0.1"

# Set appropriate permissions
chmod 600 $SSL_DIR/key.pem
chmod 644 $SSL_DIR/cert.pem

echo "SSL certificates generated successfully!"
echo "Location: $SSL_DIR"
echo "Note: These are self-signed certificates for development only."
echo "For production, please use proper SSL certificates from a trusted CA."

# Generate Diffie-Hellman parameters for improved security
openssl dhparam -out $SSL_DIR/dhparam.pem 2048

echo "Diffie-Hellman parameters generated."
echo "SSL setup complete!"

# Instructions for trust on different platforms
echo -e "\nTo trust this certificate in development:"
echo "MacOS:"
echo "1. Double click cert.pem"
echo "2. Add to System keychain"
echo "3. Trust the certificate for SSL"
echo ""
echo "Linux (Ubuntu/Debian):"
echo "1. sudo cp $SSL_DIR/cert.pem /usr/local/share/ca-certificates/volleyball-local.crt"
echo "2. sudo update-ca-certificates"
echo ""
echo "Windows:"
echo "1. Double click cert.pem"
echo "2. Install Certificate"
echo "3. Place in Trusted Root Certification Authorities"
