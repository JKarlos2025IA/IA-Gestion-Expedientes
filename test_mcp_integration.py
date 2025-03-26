import os
import sys
import time
import datetime

# Asegurarse de que los módulos estén en el path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar los componentes MCP
try:
    from models.expediente_model import ExpedienteModel
    from models.documento_model import DocumentoModel
    from models.chat_history_model import ChatHistoryModel
    from controllers.chat_controller import ChatController
    from controllers.ia_controller import IAController
    from controllers.busqueda_controller import BusquedaController
    from utils.supabase_client import get_supabase_client
    
    IMPORTS_OK = True
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    IMPORTS_OK = False

def test_supabase_connection():
    """Prueba la conexión con Supabase"""
    print("\n🔍 Probando conexión con Supabase...")
    
    supabase = get_supabase_client()
    if supabase:
        try:
            # Intentar una consulta simple
            response = supabase.table("expedientes").select("count").limit(1).execute()
            print("✅ Conexión con Supabase establecida correctamente.")
            return True
        except Exception as e:
            print(f"❌ Error al consultar Supabase: {e}")
            return False
    else:
        print("❌ No se pudo crear cliente Supabase.")
        return False

def test_models():
    """Prueba los modelos del patrón MCP"""
    print("\n🔍 Probando modelos...")
    models_ok = True
    
    # Probar modelo de expedientes
    try:
        print("Probando ExpedienteModel...")
        expediente_model = ExpedienteModel()
        print("✅ ExpedienteModel inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error en ExpedienteModel: {e}")
        models_ok = False
    
    # Probar modelo de documentos
    try:
        print("Probando DocumentoModel...")
        documento_model = DocumentoModel()
        print("✅ DocumentoModel inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error en DocumentoModel: {e}")
        models_ok = False
    
    # Probar modelo de historial de chat
    try:
        print("Probando ChatHistoryModel...")
        chat_history_model = ChatHistoryModel()
        print("✅ ChatHistoryModel inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error en ChatHistoryModel: {e}")
        models_ok = False
    
    return models_ok

def test_controllers():
    """Prueba los controladores del patrón MCP"""
    print("\n🔍 Probando controladores...")
    controllers_ok = True
    
    # Probar controlador de IA
    try:
        print("Probando IAController...")
        ia_controller = IAController()
        apis = ia_controller.get_available_apis()
        print(f"✅ IAController inicializado correctamente. APIs disponibles: {apis}")
    except Exception as e:
        print(f"❌ Error en IAController: {e}")
        controllers_ok = False
    
    # Probar controlador de búsqueda
    try:
        print("Probando BusquedaController...")
        busqueda_controller = BusquedaController()
        print("✅ BusquedaController inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error en BusquedaController: {e}")
        controllers_ok = False
    
    # Probar controlador de chat
    try:
        print("Probando ChatController...")
        chat_controller = ChatController(user_id="test_user")
        print("✅ ChatController inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error en ChatController: {e}")
        controllers_ok = False
    
    return controllers_ok

def test_chat_functionality():
    """Prueba la funcionalidad de chat completa"""
    print("\n🔍 Probando funcionalidad de chat completa...")
    
    try:
        # Crear controlador de chat
        chat_controller = ChatController(user_id="test_user")
        
        # Crear una conversación de prueba
        conversation_title = f"Prueba MCP {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        conv_id = chat_controller.create_conversation(conversation_title)
        
        if not conv_id:
            print("❌ No se pudo crear la conversación.")
            return False
        
        print(f"✅ Conversación creada con ID: {conv_id}")
        
        # Enviar un mensaje de prueba
        query = "Busca información sobre contratos de servicios"
        print(f"Enviando consulta de prueba: '{query}'")
        
        result = chat_controller.process_query(query, conv_id)
        
        if "error" in result:
            print(f"❌ Error en la consulta: {result['error']}")
            return False
        
        print("✅ Consulta procesada correctamente.")
        print(f"Respuesta: {result['response'][:100]}...")
        
        # Obtener historial de la conversación
        messages = chat_controller.get_conversation_history(conv_id)
        print(f"✅ Se recuperaron {len(messages)} mensajes de la conversación.")
        
        # Eliminar la conversación de prueba
        if chat_controller.delete_conversation(conv_id):
            print("✅ Conversación de prueba eliminada correctamente.")
        else:
            print("⚠️ No se pudo eliminar la conversación de prueba.")
        
        return True
    except Exception as e:
        print(f"❌ Error en la prueba de chat: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de integración MCP")
    
    # Verificar importaciones
    if not IMPORTS_OK:
        print("❌ No se pudieron importar todos los módulos. Verifica la estructura del proyecto.")
        return
    
    tests = [
        ("Conexión con Supabase", test_supabase_connection),
        ("Modelos MCP", test_models),
        ("Controladores MCP", test_controllers),
        ("Funcionalidad de Chat", test_chat_functionality)
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"📋 Ejecutando prueba: {name}")
        print(f"{'='*50}")
        
        start_time = time.time()
        success = test_func()
        end_time = time.time()
        
        duration = end_time - start_time
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        
        print(f"\nResultado: {status} (Duración: {duration:.2f} segundos)")
        results.append((name, success, duration))
    
    # Mostrar resumen de resultados
    print("\n\n🎯 RESUMEN DE PRUEBAS")
    print("="*50)
    
    all_passed = True
    for name, success, duration in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        all_passed = all_passed and success
        print(f"{status} - {name} ({duration:.2f}s)")
    
    print("="*50)
    if all_passed:
        print("\n🎉 ¡Todas las pruebas pasaron correctamente!")
        print("La arquitectura MCP está funcionando según lo esperado.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("Revisa los errores y corrige los problemas antes de continuar.")

if __name__ == "__main__":
    main()