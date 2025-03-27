# IA-Gestion-Expedientes

## Descripci√≥n
Sistema avanzado de gesti√≥n de expedientes jur√≠dicos con integraci√≥n de inteligencia artificial para la b√∫squeda, an√°lisis y procesamiento de documentos legales. Dise√±ado para profesionales del derecho que necesitan organizar, consultar y analizar grandes vol√∫menes de informaci√≥n documental.

## Arquitectura del Proyecto

Este proyecto implementa el patr√≥n de arquitectura MCP (Model-Controller-Presenter) que proporciona:
- **Separaci√≥n clara de responsabilidades**: Cada componente tiene un prop√≥sito espec√≠fico
- **Mantenibilidad**: Facilidad para modificar o a√±adir funcionalidades
- **Escalabilidad**: Capacidad para crecer incorporando nuevos modelos de IA o funcionalidades
- **Testabilidad**: Estructura que facilita las pruebas unitarias e integraci√≥n

### Estructura de carpetas
```
proyecto/
‚îú‚îÄ‚îÄ app.py                     # Punto de entrada principal (Streamlit)
‚îú‚îÄ‚îÄ config.py                  # Configuraci√≥n centralizada
‚îú‚îÄ‚îÄ models/                    # Capa de acceso a datos
‚îÇ   ‚îú‚îÄ‚îÄ expediente_model.py    # Gesti√≥n de expedientes
‚îÇ   ‚îú‚îÄ‚îÄ documento_model.py     # Gesti√≥n de documentos
‚îÇ   ‚îî‚îÄ‚îÄ chat_history_model.py  # Gesti√≥n de conversaciones
‚îú‚îÄ‚îÄ controllers/               # L√≥gica de negocio
‚îÇ   ‚îú‚îÄ‚îÄ busqueda_controller.py # L√≥gica de b√∫squeda
‚îÇ   ‚îú‚îÄ‚îÄ chat_controller.py     # Gesti√≥n de conversaciones
‚îÇ   ‚îî‚îÄ‚îÄ ia_controller.py       # Integraci√≥n con APIs de IA
‚îú‚îÄ‚îÄ presenters/                # Preparaci√≥n para la UI
‚îÇ   ‚îî‚îÄ‚îÄ chat_presenter.py      # Formateo de mensajes
‚îî‚îÄ‚îÄ utils/                     # Utilidades
    ‚îî‚îÄ‚îÄ supabase_client.py     # Cliente para Supabase
```

## Funcionalidades Principales

### 1. Gesti√≥n de Expedientes
- B√∫squeda avanzada de expedientes por m√∫ltiples criterios
- Visualizaci√≥n detallada de metadatos y documentos asociados
- Creaci√≥n autom√°tica de expedientes al subir documentos (con validaci√≥n)
- Categorizaci√≥n y etiquetado de expedientes

### 2. Procesamiento de Documentos
- Carga individual de archivos PDF
- Procesamiento por lotes de m√∫ltiples PDFs
- Extracci√≥n autom√°tica de texto con revisi√≥n manual
- Detecci√≥n inteligente del tipo de documento
- Almacenamiento optimizado en base de datos

### 3. Asistente IA Conversacional
- Consultas en lenguaje natural sobre expedientes
- Detecci√≥n de intenci√≥n para optimizar respuestas
- Adaptaci√≥n de formato seg√∫n tipo de consulta
- Soporte para m√∫ltiples proveedores de IA
- Historial de conversaciones persistente

### 4. Integraci√≥n con Bases de Datos
- Conexi√≥n con Supabase (PostgreSQL)
- Pol√≠ticas de seguridad a nivel de fila (RLS)
- B√∫squeda relacional de documentos y expedientes
- Almacenamiento eficiente de contenido textual extenso

## Tecnolog√≠as Utilizadas

- **Frontend**: Streamlit (interfaz interactiva en Python)
- **Backend**: Python (3.12+)
- **Base de Datos**: Supabase (PostgreSQL)
- **Procesamiento de Documentos**: PyMuPDF (extracci√≥n de texto)
- **Inteligencia Artificial**:
  - Claude de Anthropic (API principal)
  - Deepseek (alternativa)
  - Google Gemini (en desarrollo)
  
## Configuraci√≥n y Despliegue

### Requisitos Previos
- Python 3.12 o superior
- Cuenta en Supabase
- Claves API para servicios de IA (Claude, Deepseek, Gemini)
- Git instalado para control de versiones

### Instalaci√≥n

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
   - Configurar la conexi√≥n a Supabase en `utils/supabase_client.py`

5. Ejecutar la aplicaci√≥n:
```bash
streamlit run app.py
```

### Control de Versiones con Git

Este proyecto utiliza Git para control de versiones con la siguiente estructura:

- **main**: Rama principal estable para producci√≥n
- **desarrollo**: Rama de desarrollo activo e integraci√≥n

#### Realizar copias de seguridad con Git

Para guardar tus cambios y hacer respaldo en GitHub:

1. Verificar estado de los archivos:
```bash
git status
```

2. A√±adir archivos modificados:
```bash
git add .
```

3. Confirmar cambios con un mensaje descriptivo:
```bash
git commit -m "Descripci√≥n de los cambios realizados"
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

Para descargar la √∫ltima versi√≥n desde GitHub:

```bash
git pull origin desarrollo   # Si est√°s en la rama desarrollo
```

## Estado Actual (Marzo 2025)

### Funcionalidades Implementadas
- ‚úÖ Arquitectura MCP completa y funcionando
- ‚úÖ Conexi√≥n estable con Supabase
- ‚úÖ Integraci√≥n con API de Claude (Anthropic)
- ‚úÖ Interfaz para carga y procesamiento de documentos PDF
- ‚úÖ Extracci√≥n autom√°tica de texto con PyMuPDF
- ‚úÖ Visualizaci√≥n y edici√≥n del contenido extra√≠do
- ‚úÖ Chat con IA para consultas sobre expedientes
- ‚úÖ B√∫squeda relacional de expedientes y documentos
- ‚úÖ Creaci√≥n de expedientes con validaci√≥n de campos

### Pr√≥ximos Desarrollos

#### Fase 1: Despliegue y Optimizaci√≥n
1. ‚è≥ Despliegue en plataforma de hosting (Streamlit Cloud/Heroku/PythonAnywhere)
2. ‚è≥ Configuraci√≥n de CI/CD para actualizaciones autom√°ticas
3. ‚è≥ Optimizaci√≥n de rendimiento y experiencia de usuario

### Gu√≠a de Despliegue en Streamlit Cloud

Para desplegar la aplicaci√≥n y hacerla accesible desde cualquier lugar:

1. **Preparaci√≥n del repositorio**:
   - Verificar que el archivo requirements.txt est√© actualizado: `pip freeze > requirements.txt`
   - Asegurar que todas las dependencias est√©n incluidas
   - Commit y push de los cambios a GitHub: `git add requirements.txt && git commit -m "Actualizar requirements.txt" && git push origin desarrollo`

2. **Configuraci√≥n en Streamlit Cloud**:
   - Crear cuenta en [Streamlit Cloud](https://streamlit.io/cloud)
   - Conectar con la cuenta de GitHub
   - Seleccionar el repositorio "IA-Gestion-Expedientes"
   - Especificar la rama (main o desarrollo) y el archivo principal (app.py)

3. **Configuraci√≥n de secretos**:
   - En Streamlit Cloud, a√±adir variables de entorno para:
     - SUPABASE_URL
     - SUPABASE_KEY
     - CLAUDE_API_KEY
     - DEEPSEEK_API_KEY
     - GEMINI_API_KEY

4. **Ajustes avanzados**:
   - Configurar recursos de la instancia seg√∫n necesidades
   - Establecer configuraci√≥n de privacidad (p√∫blico o privado)
   - Opcionalmente, configurar un dominio personalizado

#### Fase 2: Mejoras Planificadas
1. Ì†ΩÌ¥Ñ Sistema RAG (Retrieval Augmented Generation) con embeddings vectoriales
2. Ì†ΩÌ¥Ñ B√∫squeda sem√°ntica en documentos legales
3. Ì†ΩÌ¥Ñ Dashboard anal√≠tico de expedientes
4. Ì†ΩÌ¥Ñ Sistema de alertas y notificaciones para plazos
5. Ì†ΩÌ¥Ñ Vistas espec√≠ficas por tipo de proceso jur√≠dico
6. Ì†ΩÌ¥Ñ Calendario integrado con visualizaci√≥n de eventos
7. Ì†ΩÌ¥Ñ Extracci√≥n autom√°tica de entidades y conceptos jur√≠dicos
8. Ì†ΩÌ¥Ñ Generador de documentos legales basados en plantillas
9. Ì†ΩÌ¥Ñ Integraci√≥n con firma electr√≥nica
10. Ì†ΩÌ¥Ñ Modo offline con sincronizaci√≥n
11. Ì†ΩÌ¥Ñ Versionado de documentos
12. Ì†ΩÌ¥Ñ Sistema de anotaciones y comentarios colaborativos
13. Ì†ΩÌ¥Ñ Estad√≠sticas de uso y rendimiento
14. Ì†ΩÌ¥Ñ Sistema de etiquetas personalizable
15. Ì†ΩÌ¥Ñ Exportaci√≥n a formatos legales est√°ndar (PDF/A)

## Modelo de Datos

### Tabla: expedientes
| Campo | Tipo | Descripci√≥n | Restricciones |
|-------|------|-------------|---------------|
| id | serial | Identificador √∫nico | PK |
| numero_expediente | text | C√≥digo del expediente | NOT NULL, UNIQUE |
| fecha_creacion | date | Fecha de creaci√≥n | NOT NULL |
| tipo_proceso | text | Tipo de proceso legal | NOT NULL |
| modalidad | text | Modalidad del expediente | NOT NULL |
| seccion | text | Secci√≥n o departamento | NOT NULL |
| tema_principal | text | Tema principal del expediente | NOT NULL |
| estado | text | Estado actual del expediente | NOT NULL |
| area_solicitante | text | √Årea que solicita el expediente | NOT NULL |
| created_at | timestamp | Fecha de creaci√≥n en el sistema | DEFAULT now() |

### Tabla: documentos_expediente
| Campo | Tipo | Descripci√≥n | Restricciones |
|-------|------|-------------|---------------|
| id | serial | Identificador √∫nico | PK |
| expediente_id | integer | ID del expediente relacionado | FK ‚Üí expedientes(id) |
| nombre_archivo | text | Nombre del documento | NOT NULL |
| tipo_documento | text | Tipo de documento | NOT NULL |
| contenido | text | Texto extra√≠do del documento | |

## Licencia

Este proyecto est√° bajo la Licencia MIT. Ver archivo `LICENSE` para m√°s detalles.

## Contacto

Desarrollado por JKarlos2025IA
- GitHub: [@JKarlos2025](https://github.com/JKarlos2025)