from conn_db import get_database_instance

# Obtener una instancia de la base de datos utilizando la función get_database_instance
db = get_database_instance()



# Cerrar la conexión
db.close_connection()