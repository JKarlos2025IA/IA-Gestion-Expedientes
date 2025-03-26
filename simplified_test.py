"""
Test simplificado para verificar la arquitectura MCP
"""
import os
import sys
import datetime

# Añadir el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """Prueba las importaciones de los módulos"""
    print("\n🔍 Probando importaciones de módulos...")
    
    modules_to_test = [
        "utils.supabase_client",
        "models.expediente_model",
        "models.documento_model",
        "models.chat_history_model",
        "controllers.busqueda_controller",
        "controllers.chat_controller",
        "controllers.ia_controller",
        "presenters.chat_presenter"
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module_name in modules_to_test:
        try:
            print(f"Intentando importar {module_name}...")
            module = __import__(module_name, fromlist=["*"])
            successful_imports.append(module_name)
            print(f"✅ Módulo {module_name} importado correctamente")
        except ImportError as e:
            print(f"❌ Error importando {module_name}: {e}")
            failed_imports.append((module_name, str(e)))
        except Exception as e:
            print(f"⚠️ Otro error en {module_name}: {e}")
            failed_imports.append((module_name, str(e)))
    
    print("\n📊 Resumen de importaciones:")
    print(f"✅ Módulos importados correctamente: {len(successful_imports)}/{len(modules_to_test)}")
    
    if successful_imports:
        print("\nMódulos correctos:")
        for module in successful_imports:
            print(f"  ✓ {module}")
    
    if failed_imports:
        print("\nMódulos con error:")
        for module, error in failed_imports:
            print(f"  ✗ {module}: {error}")
    
    return len(failed_imports) == 0

def test_supabase_connection():
    """Prueba la conexión con Supabase"""
    print("\n🔍 Probando conexión con Supabase...")
    
    try:
        from utils.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        if supabase:
            try:
                # Intentar una consulta simple
                response = supabase.table("expedientes").select("count").limit(1).execute()
                print(f"✅ Conexión con Supabase establecida correctamente: {response}")
                return True
            except Exception as e:
                print(f"❌ Error al consultar Supabase: {e}")
                return False
        else:
            print("❌ No se pudo crear cliente Supabase.")
            return False
    except ImportError as e:
        print(f"❌ Error importando el cliente Supabase: {e}")
        return False

def test_chat_tables():
    """Prueba que las tablas de chat existan"""
    print("\n🔍 Probando tablas de chat en Supabase...")
    
    try:
        from utils.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        if not supabase:
            print("❌ No se pudo crear cliente Supabase.")
            return False
            
        tables_to_check = [
            "chat_conversations",
            "chat_messages",
            "projects"
        ]
        
        success = True
        for table in tables_to_check:
            try:
                # Verificar si podemos consultar la tabla
                response = supabase.table(table).select("count").limit(1).execute()
                print(f"✅ Tabla '{table}' existe y es accesible.")
            except Exception as e:
                print(f"❌ Error al acceder a la tabla '{table}': {e}")
                success = False
        
        return success
    except ImportError as e:
        print(f"❌ Error importando el cliente Supabase: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas simplificadas de integración MCP")
    print("="*50)
    
    tests = [
        ("Importaciones de módulos", test_imports),
        ("Conexión con Supabase", test_supabase_connection),
        ("Tablas de chat", test_chat_tables)
    ]
    
    all_passed = True
    for name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"📋 Ejecutando prueba: {name}")
        print(f"{'='*50}")
        
        success = test_func()
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        all_passed = all_passed and success
        
        print(f"\nResultado: {status}")
    
    print("\n\n🎯 RESUMEN FINAL")
    print("="*50)
    
    if all_passed:
        print("\n🎉 ¡Todas las pruebas básicas pasaron correctamente!")
        print("La estructura fundamental parece estar en orden.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("Revisa los errores y corrige los problemas antes de continuar.")

if __name__ == "__main__":
    main()