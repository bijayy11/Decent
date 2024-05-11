# Write private key to a hidden file
filename = ".private_key.pem"  # Prefix filename with a dot
with open(filename, 'wb') as f:
    f.write("ishanpanta")

print("Private key has been written to:", filename)