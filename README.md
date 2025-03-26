# IA-Gestion-Expedientes

## Descripción
Sistema avanzado de gestión de expedientes jurídicos con integración de inteligencia artificial para la búsqueda, análisis y procesamiento de documentos legales. Diseñado para profesionales del derecho que necesitan organizar, consultar y analizar grandes volúmenes de información documental.

## Arquitectura del Proyecto

Este proyecto implementa el patrón de arquitectura MCP (Model-Controller-Presenter) que proporciona:
- **Separación clara de responsabilidades**: Cada componente tiene un propósito específico
- **Mantenibilidad**: Facilidad para modificar o añadir funcionalidades
- **Escalabilidad**: Capacidad para crecer incorporando nuevos modelos de IA o funcionalidades
- **Testabilidad**: Estructura que facilita las pruebas unitarias e integración

### Estructura de carpetas
```
proyecto/
├── app.py                     # Punto de entrada principal (Streamlit)
├── config.py                  # Configuración centralizada
├── models/                    # Capa de acceso a datos
│   ├── expediente_model.py    # Gestión de expedientes
│   ├── documento_model.py     # Gestión de documentos
│   └── chat_history_model.py  # Gestión de conversaciones
├── controllers/               # Lógica de negocio
│   ├── busqueda_controller.py # Lógica de búsqueda
│   ├── chat_controller.py     # Gestión de conversaciones
│   └── ia_controller.py       # Integración con APIs de IA
├── presenters/                # Preparación para la UI
│   └── chat_presenter.py      # Formateo de mensajes
└── utils/                     # Utilidades
    └── supabase_client.py     # Cliente para Supabase
```

## Funcionalidades Principales

### 1. Gestión de Expedientes
- Búsqueda avanzada de expedientes por múltiples criterios
- Visualización detallada de metadatos y documentos asociados
- Creación automática de expedientes al subir documentos (con validación)
- Categorización y etiquetado de expedientes

### 2. Procesamiento de Documentos
- Carga individual de archivos PDF
- Procesamiento por lotes de múltiples PDFs
- Extracción automática de texto con revisión manual
- Detección inteligente del tipo de documento
- Almacenamiento optimizado en base de datos

### 3. Asistente IA Conversacional
- Consultas en lenguaje natural sobre expedientes
- Detección de intención para optimizar respuestas
- Adaptación de formato según tipo de consulta
- Soporte para múltiples proveedores de IA
- Historial de conversaciones persistente

### 4. Integración con Bases de Datos
- Conexión con Supabase (PostgreSQL)
- Políticas de seguridad a nivel de fila (RLS)
- Búsqueda relacional de documentos y expedientes
- Almacenamiento eficiente de contenido textual extenso

## Tecnologías Utilizadas

- **Frontend**: Streamlit (interfaz interactiva en Python)
- **Backend**: Python (3.12+)
- **Base de Datos**: Supabase (PostgreSQL)
- **Procesamiento de Documentos**: PyMuPDF (extracción de texto)
- **Inteligencia Artificial**:
  - Deepseek (reemplazo de Claude)
  - Google Gemini
  - Soporte para OpenAI (opcional)
  
## Configuración y Despliegue

### Requisitos Previos
- Python 3.12 o superior
- Cuenta en Supabase
- Claves API para servicios de IA (Deepseek, Gemini, etc.)

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/JKarlos2025/IA-Gestion-Expedientes.git
cd IA-Gestion-Expedientes
```

2. Crear entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar claves API:
   - Actualizar `config.py` con tus claves API
   - Configurar la conexión a Supabase en `utils/supabase_client.py`

5. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## Estrategia de Desarrollo

### Control de Versiones
Este proyecto utiliza Git con la siguiente estructura de ramas:
- **main**: Código estable y listo para producción
- **desarrollo**: Rama principal para integración de nuevas características
- **feature/xxx**: Ramas para desarrollo de características específicas

### Buenas Prácticas
- **Commits frecuentes**: Realizar commits específicos y descriptivos
- **Pull Requests**: Revisar código antes de integrar a ramas principales
- **Documentación**: Mantener actualizada la documentación con cada cambio
- **Testing**: Escribir pruebas para nuevas funcionalidades

## Contribución

Si deseas contribuir a este proyecto:
1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commits (`git commit -m 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Contacto

Desarrollado por JKarlos2025IA
- GitHub: [@JKarlos2025](https://github.com/JKarlos2025)