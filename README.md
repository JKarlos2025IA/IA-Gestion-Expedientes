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
  - Claude de Anthropic (API principal)
  - Deepseek (alternativa)
  - Google Gemini (en desarrollo)
  
## Configuración y Despliegue

### Requisitos Previos
- Python 3.12 o superior
- Cuenta en Supabase
- Claves API para servicios de IA (Claude, Deepseek, Gemini)
- Git instalado para control de versiones

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

### Control de Versiones con Git

Este proyecto utiliza Git para control de versiones con la siguiente estructura:

- **main**: Rama principal estable para producción
- **desarrollo**: Rama de desarrollo activo e integración

#### Realizar copias de seguridad con Git

Para guardar tus cambios y hacer respaldo en GitHub:

1. Verificar estado de los archivos:
```bash
git status
```

2. Añadir archivos modificados:
```bash
git add .
```

3. Confirmar cambios con un mensaje descriptivo:
```bash
git commit -m "Descripción de los cambios realizados"
```

4. Subir cambios a GitHub (respaldo remoto):
```bash
# Para rama desarrollo
git push origin desarrollo

# Para rama main
git push origin main
```

5. Verificar ramas existentes:
```bash
git branch
```

6. Verificar repositorio remoto configurado:
```bash
git remote -v
```

7. Cambiar entre ramas:
```bash
git checkout main   # Cambiar a rama main
git checkout desarrollo   # Cambiar a rama desarrollo
```

#### Recuperar cambios desde GitHub

Para descargar la última versión desde GitHub:

```bash
git pull origin desarrollo   # Si estás en la rama desarrollo
```

## Estado Actual (Marzo 2025)

### Funcionalidades Implementadas
- ✅ Arquitectura MCP completa y funcionando
- ✅ Conexión estable con Supabase
- ✅ Integración con API de Claude (Anthropic)
- ✅ Interfaz para carga y procesamiento de documentos PDF
- ✅ Extracción automática de texto con PyMuPDF
- ✅ Visualización y edición del contenido extraído
- ✅ Chat con IA para consultas sobre expedientes
- ✅ Búsqueda relacional de expedientes y documentos
- ✅ Creación de expedientes con validación de campos

### Próximos Desarrollos

#### Fase 1: Despliegue y Optimización
1. ⏳ Despliegue en plataforma de hosting (Streamlit Cloud/Heroku/PythonAnywhere)
2. ⏳ Configuración de CI/CD para actualizaciones automáticas
3. ⏳ Optimización de rendimiento y experiencia de usuario

### Guía de Despliegue en Streamlit Cloud

Para desplegar la aplicación y hacerla accesible desde cualquier lugar:

1. **Preparación del repositorio**:
   - Verificar que el archivo requirements.txt esté actualizado: `pip freeze > requirements.txt`
   - Asegurar que todas las dependencias estén incluidas
   - Commit y push de los cambios a GitHub: `git add requirements.txt && git commit -m "Actualizar requirements.txt" && git push origin desarrollo`

2. **Configuración en Streamlit Cloud**:
   - Crear cuenta en [Streamlit Cloud](https://streamlit.io/cloud)
   - Conectar con la cuenta de GitHub
   - Seleccionar el repositorio "IA-Gestion-Expedientes"
   - Especificar la rama (main o desarrollo) y el archivo principal (app.py)

3. **Configuración de secretos**:
   - En Streamlit Cloud, añadir variables de entorno para:
     - SUPABASE_URL
     - SUPABASE_KEY
     - CLAUDE_API_KEY
     - DEEPSEEK_API_KEY
     - GEMINI_API_KEY

4. **Ajustes avanzados**:
   - Configurar recursos de la instancia según necesidades
   - Establecer configuración de privacidad (público o privado)
   - Opcionalmente, configurar un dominio personalizado

#### Fase 2: Mejoras Planificadas
1. �� Sistema RAG (Retrieval Augmented Generation) con embeddings vectoriales
2. �� Búsqueda semántica en documentos legales
3. �� Dashboard analítico de expedientes
4. �� Sistema de alertas y notificaciones para plazos
5. �� Vistas específicas por tipo de proceso jurídico
6. �� Calendario integrado con visualización de eventos
7. �� Extracción automática de entidades y conceptos jurídicos
8. �� Generador de documentos legales basados en plantillas
9. �� Integración con firma electrónica
10. �� Modo offline con sincronización
11. �� Versionado de documentos
12. �� Sistema de anotaciones y comentarios colaborativos
13. �� Estadísticas de uso y rendimiento
14. �� Sistema de etiquetas personalizable
15. �� Exportación a formatos legales estándar (PDF/A)

## Modelo de Datos

### Tabla: expedientes
| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| id | serial | Identificador único | PK |
| numero_expediente | text | Código del expediente | NOT NULL, UNIQUE |
| fecha_creacion | date | Fecha de creación | NOT NULL |
| tipo_proceso | text | Tipo de proceso legal | NOT NULL |
| modalidad | text | Modalidad del expediente | NOT NULL |
| seccion | text | Sección o departamento | NOT NULL |
| tema_principal | text | Tema principal del expediente | NOT NULL |
| estado | text | Estado actual del expediente | NOT NULL |
| area_solicitante | text | Área que solicita el expediente | NOT NULL |
| created_at | timestamp | Fecha de creación en el sistema | DEFAULT now() |

### Tabla: documentos_expediente
| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| id | serial | Identificador único | PK |
| expediente_id | integer | ID del expediente relacionado | FK → expedientes(id) |
| nombre_archivo | text | Nombre del documento | NOT NULL |
| tipo_documento | text | Tipo de documento | NOT NULL |
| contenido | text | Texto extraído del documento | |

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Contacto

Desarrollado por JKarlos2025IA
- GitHub: [@JKarlos2025](https://github.com/JKarlos2025)