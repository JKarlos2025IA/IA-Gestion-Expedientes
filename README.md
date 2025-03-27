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

#### Fase 2: Mejoras Planificadas
1. ������ Sistema RAG (Retrieval Augmented Generation) con embeddings vectoriales
2. ������ Búsqueda semántica en documentos legales
3. ������ Dashboard analítico de expedientes
4. ������ Sistema de alertas y notificaciones para plazos
5. ������ Vistas específicas por tipo de proceso jurídico
6. ������ Calendario integrado con visualización de eventos
7. ������ Extracción automática de entidades y conceptos jurídicos
8. ������ Generador de documentos legales basados en plantillas
9. ������ Integración con firma electrónica
10. ������ Modo offline con sincronización
11. ������ Versionado de documentos
12. ������ Sistema de anotaciones y comentarios colaborativos
13. ������ Estadísticas de uso y rendimiento
14. ������ Sistema de etiquetas personalizable
15. ������ Exportación a formatos legales estándar (PDF/A)

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