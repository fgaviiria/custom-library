📚 Library Management System (Odoo Module)
Este repositorio contiene un sistema de gestión de bibliotecas en Odoo. El módulo library_management permite administrar libros, socios y préstamos, integrándose con servicios externos y asegurando la integridad de datos.

🚀 Características Principales
1. Gestión de Catálogo y Socios
Libros (library.book): Registro detallado con validación de ISBN único.

Socios (library.member): Extensión del modelo res.partner mediante herencia por delegación (_inherits), manteniendo la compatibilidad con el ecosistema de contactos de Odoo.

Disponibilidad: Control automático del campo is_available.

2. Gestión de Préstamos (library.checkout)
Flujo de Estados: Ciclo completo Prestado -> Devuelto.

Validaciones:

Restricción de software (Domain) para UX.

Restricción de integridad (Python Constraint): Impide a nivel de servidor prestar un libro que ya está ocupado, evitando condiciones de carrera.

Automatización: Liberación automática del libro al registrar la devolución.

3. Integración API Externa (Open Library)
Enriquecimiento de Datos: Búsqueda automática por ISBN consumiendo la Open Library Books API.

Robustez: Implementación de dateutil para parsear formatos de fecha inconsistentes retornados por la API (ej: "2017", "Nov 2017").

Feedback de Usuario: Notificaciones visuales (Success/Warning/Danger) según el resultado de la petición.

Historial: Pestaña dedicada con el historial de préstamos en la vista del socio.

🛠️ Tecnologías
Odoo 18.0

Python 3.10+

PostgreSQL 15

Docker & Docker Compose

⚙️ Instalación y Despliegue
El proyecto está dockerizado para un despliegue rápido y aislado.

1. Clonar el repositorio:

git clone <url-del-repo>
cd custom-library

2. Construir y levantar los contenedores:

docker-compose up --build -d

3. Acceder a la aplicación:

URL: http://localhost:8069

Email: admin
Password: admin

Nota: El contenedor está configurado para intentar instalar el módulo library_management automáticamente al inicio.

🧪 Pruebas Automatizadas (Testing)
El módulo incluye pruebas unitarias para validar la lógica de negocio y restricciones.

Para ejecutar los tests desde el contenedor:

docker-compose run --rm web odoo -d odoo -i library_management --test-enable --test-tags library_management --stop-after-init

