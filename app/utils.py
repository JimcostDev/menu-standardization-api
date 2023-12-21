from bson import ObjectId


# Verificar si un ID dado es un ObjectId válido en MongoDB
def is_valid_object_id(id_to_check: str) -> bool:
    try:
        ObjectId(id_to_check)
        return True
    except Exception as e:
        return False
