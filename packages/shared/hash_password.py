import bcrypt

# Génère un hash pour "test123"
password = "test123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
print(f"Hash pour '{password}':")
print(hashed.decode('utf-8'))