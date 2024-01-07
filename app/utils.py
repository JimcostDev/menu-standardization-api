from bson import ObjectId
import bcrypt

# Verificar si un ID dado es un ObjectId válido en MongoDB
def is_valid_object_id(id_to_check: str) -> bool:
    try:
        ObjectId(id_to_check)
        return True
    except Exception as e:
        return False

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Función para verificar la contraseña hasheada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
