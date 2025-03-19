from supabase_client import buscar_en_toda_bd

# Prueba con una consulta de ejemplo
consulta_prueba = "2025-JNJ-DSN-0001"  # Puedes cambiar esto por otra palabra clave

print("Buscando en la base de datos...")

resultado = buscar_en_toda_bd(consulta_prueba)

# Mostrar resultado
print("Resultado de la bÃºsqueda global:")
print(resultado)  # Esto imprimirÃ¡ la respuesta en consola para verificar si se recuperan los datos



