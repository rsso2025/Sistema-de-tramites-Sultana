# Documento técnico del proyecto

# SISTEMA DE TRÁMITES SULTANA

## 1. Información general

### 1.1 Nombre del proyecto
Sistema de Trámites Sultana

### 1.2 Objetivo
El proyecto tiene como propósito centralizar la gestión de información de propietarios, vehículos y trámites documentales de una empresa de transporte, facilitando la creación de documentos institucionales a partir de plantillas Word y almacenando un historial de generación documental.

El sistema se diseñó como una aplicación de escritorio desarrollada en Python con interfaz gráfica mediante CustomTkinter, orientada a operaciones de uso interno para la administración de personas, vehículos y documentos formales.

### 1.3 Estado actual
El proyecto se encuentra en fase de desarrollo funcional. Actualmente cuenta con:

- Gestión básica de propietarios.
- Gestión básica de vehículos.
- Integración con una base de datos MySQL para lectura de datos de vehículos.
- Generación de documentos Word a partir de plantillas .docx.
- Historial de documentos generados.
- Exportación opcional a PDF mediante la librería docx2pdf.
- Configuración dinámica de tipos de documentos mediante un archivo JSON.

Sin embargo, todavía presenta áreas de mejora en cuanto a:

- Consolidación total de la persistencia en una única arquitectura de base de datos.
- Mejor separación entre lógica de negocio, acceso a datos y UI.
- Validaciones más exhaustivas y manejo de errores.
- Automatización de exportación PDF y limpieza de archivos temporales.
- Gestión más completa de trámites y estados.

### 1.4 Autor
Richard Smith Sánchez Ortega

### 1.5 Fecha
2026-07-06

---

## 2. Arquitectura general

El proyecto sigue una arquitectura de capas orientada a separar responsabilidades entre:

- Interfaz de usuario.
- Servicios o lógica de negocio.
- Repositorios o acceso a datos.
- Entidades o DTOs.
- Recursos estáticos como plantillas y configuraciones.

Esta estructura permite que la interfaz no acceda directamente a la base de datos y que la lógica documental se encapsule en un servicio independiente.

### 2.1 Principios de diseño aplicados

1. Separación de responsabilidades.
2. Uso de DTOs para transferir datos entre capas.
3. Repositorios para abstraer el almacenamiento.
4. Servicios para centralizar reglas de negocio.
5. Configuración externa mediante JSON y variables de entorno.

### 2.2 Arquitectura lógica

```text
Usuario
  │
  ▼
Interfaz (CustomTkinter)
  │
  ▼
Services
  │
  ├─ VehiculoService
  ├─ PropietarioService
  ├─ DocumentoService
  └─ SystemService
  │
  ▼
Repositories / Adapters
  │
  ├─ SQLite repositories
  └─ MySQL repositories
  │
  ▼
Base de datos
  ├─ SQLite local
  └─ MySQL remoto
  │
  ▼
DTOs / entidades
  │
  ▼
Plantillas Word + configuración JSON
  │
  ▼
Documento generado (.docx/.pdf)
```

### 2.3 Diagrama ASCII de la estructura del sistema

```text
+-----------------------------+
|           USUARIO           |
+-----------------------------+
              |
              v
+-----------------------------+
|     UI / customtkinter      |
|  main_window.py             |
|  propietarios_window.py     |
|  vehiculos_window.py        |
|  documentos_window.py       |
+-----------------------------+
              |
              v
+-----------------------------+
|          SERVICES           |
|  propietario_service.py     |
|  vehiculo_service.py        |
|  vehiculo_mysql_service.py  |
|  document_service.py        |
|  system_service.py         |
+-----------------------------+
              |
              v
+-----------------------------+
|      INFRASTRUCTURE         |
|  repositories/             |
|  mysql/                    |
|  database/                 |
+-----------------------------+
              |
              v
+-----------------------------+
|      PERSISTENCIA           |
|  SQLite (local)            |
|  MySQL (remoto)            |
+-----------------------------+
              |
              v
+-----------------------------+
|   CONFIG + TEMPLATES       |
|  documentos_config.json     |
|  assets/templates/         |
+-----------------------------+
              |
              v
+-----------------------------+
|   DOCUMENTO GENERADO       |
|  .docx / .pdf              |
+-----------------------------+
```

---

## 3. Árbol completo del proyecto

### 3.1 Estructura principal

```text
sistema_tramites_sultana/
├── main.py
├── test_buscar_por_id.py
├── .env
├── app/
│   ├── __init__.py
│   ├── PROYECTO_MASTER.md
│   ├── assets/
│   │   └── templates/
│   │       ├── CARTA_MINISTERIO_DESVINCULACION.docx
│   │       ├── CESION_DE_DERECHOS.docx
│   │       ├── CONSTANCIA_INGRESOS.docx
│   │       ├── CONTRATO VINCULACIÓN RADIO ACCION NACIONAL 2026.docx
│   │       ├── DESVINCULACION_ADMINISTRATIVA.docx
│   │       ├── DESVINCULACION_MUTUO_ACUERDO.docx
│   │       ├── INFORME_ACCIDENTE_DANOS_MATERIALES.docx
│   │       ├── Informe_Accidente_Sencillo.docx
│   │       ├── PAZ_Y_SALVO.docx
│   │       └── plantilla_certificacion_contrato.docx
│   ├── config/
│   │   ├── app_config.py
│   │   └── documentos_config.json
│   ├── core/
│   │   └── entities.py
│   ├── database/
│   │   ├── database.py
│   │   └── sistema_tramites.db
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── mysql/
│   │   │   ├── __init__.py
│   │   │   ├── mysql_connection.py
│   │   │   └── vehiculo_mysql_repository.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── documento_repository.py
│   │       ├── propietario_repository.py
│   │       └── vehiculo_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── propietario_service.py
│   │   ├── system_service.py
│   │   ├── vehiculo_mysql_service.py
│   │   └── vehiculo_service.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── documentos_window.py
│   │   ├── main_window.py
│   │   ├── propietarios_window.py
│   │   └── vehiculos_window.py
│   └── utils/
├── backups/
└── __pycache__/
```

### 3.2 Propósito de cada carpeta

- app/: Contiene la aplicación completa, organizada por capas.
- app/assets/: Recursos estáticos del sistema, principalmente plantillas Word.
- app/config/: Configuraciones globales y definición de documentos.
- app/core/: Entidades y DTOs del dominio.
- app/database/: Persistencia local mediante SQLite y archivo de base de datos.
- app/infrastructure/: Adaptadores de acceso a datos y conexión con servicios externos.
- app/infrastructure/mysql/: Conexión y repositorio para MySQL.
- app/infrastructure/repositories/: Repositorios para SQLite.
- app/services/: Lógica de negocio y coordinación entre UI y repositorios.
- app/ui/: Interfaces gráficas de usuario con CustomTkinter.
- app/utils/: Espacio reservado para utilidades futuras.
- backups/: Copias de seguridad del proyecto.

---

## 4. Tecnologías

### 4.1 Python
Python es el lenguaje principal del proyecto. Se utiliza para:

- Crear la interfaz gráfica.
- Gestionar servicios y reglas de negocio.
- Conectar con bases de datos.
- Generar documentos Word mediante la librería python-docx.
- Administrar la lógica de negocio documental.

### 4.2 CustomTkinter
CustomTkinter se utiliza para construir la interfaz gráfica moderna y con apariencia más actualizada que Tkinter clásico.

Es el componente principal de:

- Pantalla principal.
- Gestión de propietarios.
- Gestión de vehículos.
- Módulo de generación documental.

### 4.3 PyMySQL
PyMySQL es la librería usada para conectar y consultar una base de datos MySQL remota. Se utiliza principalmente desde el módulo de integración con vehículos.

### 4.4 python-docx
python-docx permite abrir, modificar y guardar documentos Word .docx. Es la base del motor documental del sistema.

### 4.5 SQLite
SQLite está presente en el proyecto como mecanismo de persistencia local. Se usa para almacenar:

- Propietarios.
- Vehículos.
- Historial documental.
- Trámites.

El archivo persistente se encuentra en:

- app/database/sistema_tramites.db

### 4.6 MySQL
MySQL se usa como base de datos externa/remota para consultar información más completa de vehículos, especialmente en el flujo de generación documental. La conexión se configura mediante variables de entorno cargadas desde el archivo .env.

### 4.7 Librerías utilizadas
Además de las anteriores, el proyecto utiliza:

- sqlite3: módulo estándar de Python para bases de datos SQLite.
- dotenv: carga de variables de entorno desde .env.
- docx2pdf: conversión de documentos Word a PDF.
- tkinter: base de la interfaz gráfica de apoyo.
- pathlib: manejo de rutas de archivos.
- datetime: generación de fechas y marcas temporales.
- json: lectura de configuraciones JSON.

---

## 5. Flujo completo del sistema

El sistema opera como un flujo transaccional orientado a documentos. El recorrido general puede describirse así:

```text
Usuario
  │
  ▼
Interfaz
  │
  ▼
Services
  │
  ▼
Repositories
  │
  ▼
MySQL
  │
  ▼
DTO
  │
  ▼
DocumentService
  │
  ▼
Plantillas Word
  │
  ▼
Documento generado
```

### 5.1 Descripción del flujo

1. El usuario accede a la interfaz.
2. En la interfaz selecciona un tipo de documento y un vehículo.
3. La UI invoca a los servicios correspondientes.
4. Los servicios consultan a los repositorios.
5. Los repositorios recuperan los datos desde SQLite o MySQL.
6. Se construye un DTO con la información del vehículo y del propietario.
7. El DocumentService combina los datos automáticos con los campos editables.
8. El sistema reemplaza marcadores en la plantilla Word.
9. Se genera un archivo .docx y, si aplica, se convierte a PDF.
10. El documento queda registrado en el historial.

### 5.2 Flujo documental detallado

- El usuario escribe o selecciona datos en la ventana de documentos.
- Se carga un vehículo desde MySQL mediante el servicio de vehículos MySQL.
- Se preparan los campos automáticos del propietario y del vehículo.
- Se crean campos editables según el tipo de documento.
- Se genera un diccionario de reemplazo con marcadores como {{placa}} o {{nombre_propietario}}.
- La plantilla se abre y se sustituyen los valores.
- El archivo generado se guarda en disco.
- Se registra la operación en la tabla documentos_generados.

---

## 6. Explicar cada módulo

### 6.1 UI
La carpeta ui contiene todas las ventanas de la aplicación. Cada ventana está diseñada para ser una clase independiente que maneja la presentación y los eventos del usuario.

#### main_window.py
Es la ventana principal de la aplicación. Desde aquí se accede a los módulos de:

- Propietarios.
- Vehículos.
- Trámites.
- Documentos.

También verifica el estado general del sistema y muestra si la base de datos MySQL está disponible.

#### propietarios_window.py
Permite registrar, visualizar y limpiar propietarios. Se apoya en PropietarioService para asegurar una separación entre UI y lógica de negocio.

#### vehiculos_window.py
Permite registrar vehículos asociados a un propietario. Usa VehiculoService para realizar el guardado y obtención de información.

#### documentos_window.py
Es el módulo más complejo del proyecto. Permite:

- Seleccionar el tipo de documento.
- Buscar un vehículo.
- Cargar datos automáticos del vehículo.
- Completar campos editables.
- Generar .docx.
- Convertir a PDF.

### 6.2 Services
La carpeta services concentra la lógica de negocio y la coordinación entre UI y repositorios.

#### propietario_service.py
Encapsula la validación y creación de propietarios. Asegura que la UI no trabaje directamente con SQL ni con entidades crudas.

#### vehiculo_service.py
Maneja la lógica de negocio para vehículos sobre SQLite.

#### vehiculo_mysql_service.py
Es la capa de adaptación para obtener datos de vehículos desde MySQL y transformarlos en el DTO VehiculoDTO utilizado por la lógica documental.

#### document_service.py
Es el corazón documental del sistema. Combina los datos de entrada, rescata la configuración de documentos y ejecuta el reemplazo de variables dentro de las plantillas.

#### system_service.py
Realiza comprobaciones generales del estado del sistema, principalmente la conexión a MySQL.

### 6.3 Infrastructure
La carpeta infrastructure agrupa la infraestructura técnica del sistema.

Incluye:

- Conexiones a bases de datos.
- Repositorios para SQL.
- Adaptadores de acceso a MySQL.

### 6.4 Repositories
Los repositorios encapsulan las operaciones de lectura y escritura. Son responsables del acceso a datos y dejan el resto a los servicios.

#### propietario_repository.py
Accede a la tabla propietarios en SQLite.

#### vehiculo_repository.py
Accede a la tabla vehiculos en SQLite.

#### documento_repository.py
Gestiona el historial documental en la tabla documentos_generados.

#### vehiculo_mysql_repository.py
Consulta datos de vehículos en MySQL y devuelve resultados estructurados.

### 6.5 DTO
La carpeta core define las entidades del dominio usando dataclasses.

#### PropietarioDTO
Representa un propietario con datos básicos.

#### VehiculoDTO
Representa un vehículo, su propietario y datos complementarios que luego son usados en documentos.

#### DocumentoGeneradoDTO
Representa un registro del historial documental.

#### TramiteDTO
Representa un trámite asociado a un vehículo.

### 6.6 Assets
La carpeta assets contiene recursos estáticos. En este proyecto, su función principal es guardar las plantillas Word del sistema.

### 6.7 Config
La carpeta config define información general y específica del sistema.

#### app_config.py
Contiene:

- Nombre del sistema.
- Descripción.
- Versión.
- Empresa.
- Autor.
- Motor de base de datos.
- Formato por defecto de documentos.

#### documentos_config.json
Define tipos de documentos, plantillas asociadas y campos editables.

### 6.8 Templates
Esta carpeta es el repositorio de plantillas Word. Cada tipo de documento tiene una plantilla específica, que luego se alimenta con datos del sistema.

### 6.9 Historial
El historial se implementa a través de la tabla documentos_generados en SQLite. Cada generación documental registra:

- Tipo de documento.
- Placa del vehículo.
- Ruta del archivo generado.
- Fecha y hora de generación.

Esto permite trazar la actividad documental de la aplicación.

---

## 7. Base de datos

El sistema emplea dos modelos de persistencia:

1. SQLite local para la aplicación de escritorio.
2. MySQL remoto para obtener datos operativos del vehículo.

### 7.1 Base de datos SQLite local
El archivo de base de datos local es app/database/sistema_tramites.db.

#### Tabla propietarios
Atributos:

- id: identificador único.
- documento: documento de identidad.
- nombre: nombre completo.
- telefono: teléfono del propietario.
- direccion: dirección del propietario.

#### Tabla vehiculos
Atributos:

- id: identificador único.
- placa: placa del vehículo.
- numero_interno: número interno.
- marca: marca.
- modelo: modelo.
- clase: clase del vehículo.
- fecha_afiliacion: fecha de afiliación.
- propietario_id: referencia al propietario.

#### Tabla documentos_generados
Atributos:

- id: identificador único.
- tipo_documento: nombre del tipo documentado.
- placa_vehiculo: placa asociada al documento.
- ruta_archivo: ubicación física del archivo.
- fecha_generacion: fecha y hora del registro.

#### Tabla tramites
Atributos:

- id: identificador único.
- tipo: tipo de trámite.
- descripcion: descripción.
- vehiculo_id: referencia al vehículo.
- fecha_creacion: fecha de creación.
- estado: estado del trámite.

### 7.2 Relaciones

- Un propietario tiene muchos vehículos.
- Un vehículo pertenece a un propietario.
- Un vehículo puede tener múltiples trámites.
- Un documento generado está asociado a una placa de vehículo, no necesariamente a una clave foránea directa en el modelo actual.

### 7.3 Relación conceptual

```text
propietarios 1 --- * vehiculos
vehiculos    1 --- * tramites
vehiculos    1 --- * documentos_generados
```

### 7.4 Consultas principales

#### Consultar propietarios
Se obtiene un listado ordenado por nombre.

#### Consultar vehículos con propietario
Se realiza un JOIN entre vehiculos y propietarios para recuperar datos relacionados.

#### Consultar vehículos por ID o placa
Se utilizan consultas específicas para cargar información en la generación documental.

#### Insertar historial documental
Se registra cada documento generado en documentos_generados.

### 7.5 Base de datos MySQL
La conexión remota se gestiona a través de app/infrastructure/mysql/mysql_connection.py y utiliza variables de entorno.

Se consulta información desde tablas como:

- vehiculo
- propietario
- marca
- clasevehi
- ruta
- color
- carroceria
- servicio
- combustible
- motorista

El repositorio MySQL transforma estos resultados en el DTO VehiculoDTO, que luego usa el servicio documental.

---

## 8. Generación documental

La generación documental es uno de los módulos más importantes del sistema. Se basa en three elementos fundamentales: plantillas Word, configuración JSON y un motor de reemplazo de texto.

### 8.1 Módulo document_service.py
El archivo document_service.py es el núcleo documental del sistema.

#### Funciones principales

- generar_documento(ruta_plantilla, ruta_salida, datos): abre la plantilla, reemplaza los marcadores y guarda el resultado.
- _reemplazar_texto_en_parrafo(parrafo, datos): sustituye placeholders dentro de los párrafos.
- _reemplazar_texto_en_tabla(tabla, datos): aplica el reemplazo a los contenidos de tablas.
- _reemplazar_texto_en_documento(documento, datos): recorre párrafos y tablas del documento completo.

#### Clase DocumentoService
Coordina:

- Carga de configuración.
- Lectura de datos del vehículo.
- Preparación del diccionario de datos.
- Generación del documento.
- Registro del historial.

### 8.2 documentos_config.json
Este archivo define los tipos de documentos disponibles y sus parámetros.

Cada entrada contiene:

- plantilla: nombre del archivo .docx asociado.
- nombre_archivo: prefijo del archivo generado.
- campos_editables: lista de campos que el usuario podrá llenar manualmente.

Ejemplos de tipos incluidos:

- Certificación
- Formato de Accidente (Interno)
- Paz y Salvo
- Cesión de Derechos
- Constancia de Ingresos
- Desvinculación Administrativa
- Desvinculación Mutuo Acuerdo
- Carta Ministerio Desvinculación
- Informe Accidente Daños Materiales

### 8.3 Plantillas Word
El sistema emplea varias plantillas en la ruta app/assets/templates.

Cada plantilla contiene marcadores como:

- {{placa}}
- {{nombre_propietario}}
- {{documento_propietario}}
- {{marca}}
- {{modelo}}
- {{clase}}
- {{fecha_larga}}
- {{ciudad_expedicion}}

El motor documental reemplaza esos marcadores por valores reales obtenidos del sistema.

### 8.4 Motor de reemplazo
El reemplazo se realiza de manera directa sobre los runs de texto del documento. Esto permite sustituir valores dentro de los párrafos y tablas.

#### Comportamiento actual
- Reemplaza placeholders encerrados en dobles llaves o en una sola llave.
- Está preparado para trabajar sobre párrafos y tablas.
- Es relativamente simple y funcional.

#### Limitación conocida
El mecanismo actual funciona correctamente cuando el marcador se encuentra dentro de un único run de texto. Si un marcador está dividido por el formateo de Word, la sustitución puede no ocurrir como se espera.

### 8.5 Historial
Tras cada generación, el sistema guarda un registro en documentos_generados con:

- tipo_documento
- placa_vehiculo
- ruta_archivo
- fecha_generacion

Esto permite auditar los documentos generados por el sistema.

### 8.6 Exportación PDF
La interfaz incluye la opción de generar el documento en formato PDF.

El flujo es:

1. Se genera primero un archivo .docx temporal.
2. Se invoca a docx2pdf para convertirlo a PDF.
3. Se elimina el archivo intermedio.
4. Se presenta la ruta del PDF final al usuario.

---

## 9. Variables documentales

La generación documental se apoya en un conjunto de variables que se alimentan de distintas fuentes.

| Variable | Origen | Tipo de origen | Documento donde se usa |
|---|---|---|---|
| nombre_propietario | BD / MySQL | BD | Todos los documentos con datos del propietario |
| documento_propietario | BD / MySQL | BD | Paz y Salvo, Cesión de Derechos, Constancia de Ingresos |
| telefono_propietario | BD / MySQL | BD | Documentos con datos de contacto |
| direccion_propietario | BD / MySQL | BD | Documentos con datos del propietario |
| ciudad_expedicion | Editable | Editable | Paz y Salvo, Cesión de Derechos, Constancia de Ingresos |
| placa | BD / MySQL | BD | Todos los documentos |
| numero_interno | BD / MySQL | BD | Documentos con datos del vehículo |
| marca | BD / MySQL | BD | Documentos de certificación y accidentes |
| modelo | BD / MySQL | BD | Documentos de certificación |
| clase | BD / MySQL | BD | Documentos de certificación |
| motor | BD / MySQL | BD | Documentos técnicos |
| chasis | BD / MySQL | BD | Documentos técnicos |
| serie | BD / MySQL | BD | Documentos técnicos |
| vin | BD / MySQL | BD | Documentos técnicos |
| fecha_matricula | BD / MySQL | BD | Documentos con fechas de matrícula |
| fecha_afiliacion | BD / SQLite | BD | Documentos con datos del vehículo |
| ruta | BD / MySQL | BD | Informes y documentos operativos |
| color | BD / MySQL | BD | Documentos de flota |
| carroceria | BD / MySQL | BD | Documentos de flota |
| servicio | BD / MySQL | BD | Documentos de flota |
| capacidad | BD / MySQL | BD | Documentos técnicos |
| tipo | BD / MySQL | BD | Documentos técnicos |
| combustible | BD / MySQL | BD | Documentos técnicos |
| modalidad | BD / MySQL | BD | Documentos técnicos |
| nombre_conductor | BD / MySQL | BD | Informes de accidente |
| documento_conductor | BD / MySQL | BD | Informes de accidente |
| celular_conductor | BD / MySQL | BD | Informes de accidente |
| direccion_conductor | BD / MySQL | BD | Informes de accidente |
| correo_conductor | BD / MySQL | BD | Informes de accidente |
| fecha_larga | Valor fijo dinámico | Valor fijo | Todos los documentos con fecha larga |
| fecha_inicio | Editable | Editable | Certificación |
| fecha_fin | Editable | Editable | Certificación |
| fecha_firma | Editable | Editable | Certificación |
| duracion | Editable | Editable | Certificación |
| fecha_emision | Editable | Editable | Certificación |
| ciudad | Editable | Editable | Certificación, Desvinculación Administrativa |
| fecha_reporte | Editable | Editable | Formato de Accidente |
| fecha_incidente | Editable | Editable | Formato de Accidente |
| hora_incidente | Editable | Editable | Formato de Accidente |
| direccion_incidente | Editable | Editable | Formato de Accidente |
| motorista | Editable | Editable | Formato de Accidente |
| nombre_reporta | Editable | Editable | Formato de Accidente |
| cc_reporta | Editable | Editable | Formato de Accidente |
| cargo_reporta | Editable | Editable | Formato de Accidente |
| tipo_novedad | Editable | Editable | Formato de Accidente |
| lugar_novedad | Editable | Editable | Formato de Accidente |
| otro_lugar | Editable | Editable | Formato de Accidente |
| descripcion_novedad | Editable | Editable | Formato de Accidente |
| Daños_Vehiculo_1 | Editable | Editable | Formato de Accidente |
| Daños_Vehiculo_2 | Editable | Editable | Formato de Accidente |
| nombre_cesionario | Editable | Editable | Cesión de Derechos |
| documento_cesionario | Editable | Editable | Cesión de Derechos |
| ciudad_cesionario | Editable | Editable | Cesión de Derechos |
| destinatario | Editable | Editable | Constancia de Ingresos |
| ingreso_letras | Editable | Editable | Constancia de Ingresos |
| ingreso_valor | Editable | Editable | Constancia de Ingresos |
| fecha_incumplimiento | Editable | Editable | Desvinculación Administrativa |
| lugar_accidente | Editable | Editable | Informe Accidente Daños Materiales |
| ciudad_accidente | Editable | Editable | Informe Accidente Daños Materiales |
| fecha_accidente | Editable | Editable | Informe Accidente Daños Materiales |
| hora_accidente | Editable | Editable | Informe Accidente Daños Materiales |
| seguro_todo_riesgo | Editable | Editable | Informe Accidente Daños Materiales |
| informe_transito | Editable | Editable | Informe Accidente Daños Materiales |
| tipo_inmueble | Editable | Editable | Informe Accidente Daños Materiales |
| nombre_tercero | Editable | Editable | Informe Accidente Daños Materiales |
| documento_tercero | Editable | Editable | Informe Accidente Daños Materiales |
| direccion_tercero | Editable | Editable | Informe Accidente Daños Materiales |
| ciudad_tercero | Editable | Editable | Informe Accidente Daños Materiales |
| celular_tercero | Editable | Editable | Informe Accidente Daños Materiales |
| correo_tercero | Editable | Editable | Informe Accidente Daños Materiales |
| relato_hechos | Editable | Editable | Informe Accidente Daños Materiales |
| danos_vehiculo | Editable | Editable | Informe Accidente Daños Materiales |
| danos_tercero | Editable | Editable | Informe Accidente Daños Materiales |

---

## 10. Estado actual

### 10.1 Qué funciona

- La aplicación inicia correctamente desde main.py.
- La interfaz principal carga y permite abrir los módulos.
- Se pueden registrar propietarios y vehículos.
- Se pueden cargar vehículos desde la base de datos MySQL y preparar documentos.
- Se generan documentos Word desde plantillas.
- Se registran los documentos generados en la tabla de historial.
- Se puede exportar a PDF usando docx2pdf.

### 10.2 Qué está pendiente

- Consolidar una única fuente de datos para propietarios y vehículos.
- Mejorar la consistencia del modelo de datos entre SQLite y MySQL.
- Implementar una gestión completa de trámites con workflow real.
- Mejorar el manejo de errores y excepciones.
- Añadir validaciones de campos más rigurosas.
- Implementar un sistema de usuarios y permisos.
- Mejorar la gestión de archivos temporales y limpieza automática.
- Añadir pruebas automatizadas.
- Incorporar manejo de versiones y auditoría de documentos.

### 10.3 Mejoras futuras

- Migrar el almacenamiento local a una base de datos relacional más robusta.
- Introducir una arquitectura basada en modelos más formalizada.
- Crear una capa de servicios compartida para documentos y trazabilidad.
- Añadir control de versiones y firma digital.
- Implementar exportación directa a PDF sin intermediario.
- Desarrollar una capa de autenticación y roles.
- Incorporar reportes y dashboards de gestión documental.

---

## 11. Historial de mejoras realizadas

### 11.1 Integración MySQL
Se incorporó la capacidad de consultar datos operativos de vehículos desde una base de datos MySQL, lo que amplió la funcionalidad documental del sistema.

### 11.2 Integración Conductores
Se añadieron campos relacionados con conductores y datos de contacto al modelo documental, permitiendo que los documentos puedan incorporar información de conductores provenientes de MySQL.

### 11.3 Motor documental
Se construyó un motor de generación de documentos capaz de abrir plantillas Word y reemplazar variables automáticamente.

### 11.4 Conservación de formato
El sistema busca preservar el contenido estructural del documento Word, reemplazando texto en párrafos y tablas con una lógica simple pero efectiva.

### 11.5 Configuración JSON
La configuración centralizada de tipos de documento en un archivo JSON permitió hacer el sistema extensible y configurable sin modificar el código fuente de forma manual en cada caso.

### 11.6 Plantillas
Se incorporó un catálogo de plantillas Word para distintos tipos de documentos institucionales, lo que convierte al sistema en una herramienta documental y no solo en un gestor de datos.

---

## 12. Recomendaciones técnicas

### 12.1 Mejoras de arquitectura

- Unificar el uso de una sola base de datos principal.
- Introducir un patrón de repositorio más uniforme.
- Separar completamente los modelos de dominio de los modelos de persistencia.
- Evitar mezclar lógica de negocio con lógica de UI.

### 12.2 Mejoras de calidad

- Añadir pruebas unitarias y de integración.
- Crear un sistema de logging.
- Manejar excepciones de forma más explícita.
- Centralizar mensajes y traducciones.

### 12.3 Mejoras de generación documental

- Implementar un motor de reemplazo más robusto que soporte formatos complejos de Word.
- Añadir soporte para tablas dinámicas y listas.
- Mejorar la estrategia de nombres de archivo.
- Añadir previsualización antes de guardar.

### 12.4 Buenas prácticas recomendadas

- Mantener la configuración en archivos externos.
- Usar variables de entorno para credenciales sensibles.
- Documentar cada plantilla y su uso.
- Versionar plantillas y cambios en la lógica documental.
- Mantener los DTOs desacoplados del acceso a la base de datos.

### 12.5 Conclusión
El proyecto representa una base sólida para un sistema de gestión documental orientado a trámites y vehículos. Su arquitectura actual ya permite gestionar información, generar documentos institucionales y registrar un historial de producción documental. El siguiente paso lógico es consolidar la arquitectura, unificar la fuente de datos y fortalecer la capa de generación documental para convertirlo en una solución más escalable, mantenible y profesional.

---

## Anexos

### A. Puntos clave del sistema

- Aplicación de escritorio en Python.
- Interfaz moderna con CustomTkinter.
- Persistencia local en SQLite.
- Integración remota con MySQL.
- Generación documental con Word.
- Historial de documentos generados.
- Exportación a PDF.

### B. Resumen ejecutivo
El Sistema de Trámites Sultana es una solución orientada a automatizar la administración documental de una empresa de transporte, combinando gestión de propietarios y vehículos con generación de actas, certificados, informes y otros documentos institucionales. El sistema está bien encaminado y cuenta con una base técnica que permite su evolución hacia una herramienta más completa y robusta.
