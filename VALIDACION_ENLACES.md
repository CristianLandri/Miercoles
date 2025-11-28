# ✅ Validación de Enlaces y Botones - AgroStar

## Página de Contacto
**Archivo**: `Contacto.html`
**Status**: ✅ CREADA Y FUNCIONAL

### Características:
- ✅ Navbar completa con enlaces a todas las secciones
- ✅ Formulario de contacto con validación JavaScript
- ✅ Información de contacto (Email, Teléfono, Ubicación)
- ✅ Enlaces a redes sociales (Instagram, Twitter, Facebook, TikTok)
- ✅ Preguntas frecuentes (FAQ) con accordion
- ✅ Mapa integrado
- ✅ Mensajes de éxito y validación de errores

---

## Enlaces Principales - Navegación Global

### En todas las páginas:
| Página | Inicio | Plantas | Tienda | Registro | Contacto | Login | Estado |
|--------|--------|---------|--------|----------|----------|-------|--------|
| **Principal.html** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | CORRECTO |
| **Plantas.html** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | CORRECTO |
| **Tienda.html** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | CORRECTO |
| **Login.html** | ✅ | - | - | ✅ | - | - | CORRECTO |
| **Registro.html** | ✅ | - | - | ✅ | - | - | CORRECTO |
| **Contacto.html** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | CORRECTO |

---

## Botones Funcionales

### Principal.html
- ✅ Botón "Más información" (desplaza a sección #sec)
- ✅ Enlaces en navbar a todas las secciones

### Plantas.html
- ✅ Botones "Flores" y "Árboles" (scroll a secciones)
- ✅ Botones "Ver más" en tarjetas de plantas
  - Limonero.html
  - Macetas.html
  - Semillas.html
  - Arboles.html
- ✅ Navbar con menú responsivo

### Tienda.html
- ✅ Botón hamburguesa (☰) para menú móvil
- ✅ Carrito de compras (icono + contador)
- ✅ Botones "Añadir al carrito" en productos
- ✅ Botones activos/deshabilitados según stock
- ✅ JavaScript para carrito funcional

### Login.html
- ✅ Botón "Entrar" (submit)
- ✅ Toggle de contraseña (mostrar/ocultar)
- ✅ Enlace a Registro.html
- ✅ Enlace de regreso a Principal.html

### Registro.html
- ✅ Botón "Registrarse" (submit)
- ✅ Toggle de contraseña (mostrar/ocultar)
- ✅ Enlace a Login.html
- ✅ Enlace de regreso a Principal.html

### Contacto.html
- ✅ Botón "Enviar Mensaje" con validación
- ✅ Validación de campos (nombre, email, asunto, mensaje)
- ✅ Mensaje de éxito
- ✅ Enlaces a redes sociales (Instagram, Twitter, Facebook, TikTok)
- ✅ Accordion FAQ

---

## Formularios

### Login.html
- ✅ Campo Email (required)
- ✅ Campo Contraseña (required, con toggle)
- ✅ Botón Entrar (submit)
- ✅ Acción: `login.php` (POST)

### Registro.html
- ✅ Campo Nombre (required)
- ✅ Campo Email (required)
- ✅ Campo Contraseña (required, con toggle)
- ✅ Campo Confirmar Contraseña (required)
- ✅ Botón Registrarse (submit)
- ✅ Acción: `registrar.php` (POST)

### Contacto.html
- ✅ Campo Nombre (validación: mín 3 caracteres)
- ✅ Campo Email (validación: formato correcto)
- ✅ Campo Teléfono (opcional)
- ✅ Campo Asunto (validación: mín 5 caracteres)
- ✅ Campo Mensaje (validación: mín 10 caracteres)
- ✅ Botón Enviar Mensaje
- ✅ Mensaje de éxito/error

---

## Validaciones JavaScript

### Contacto.html
```javascript
✅ Validación de nombre (mínimo 3 caracteres)
✅ Validación de email (@ y . requeridos)
✅ Validación de asunto (mínimo 5 caracteres)
✅ Validación de mensaje (mínimo 10 caracteres)
✅ Mostrar/ocultar mensajes de error
✅ Mostrar mensaje de éxito
✅ Limpiar formulario después de envío
✅ Auto-ocultar mensaje después de 5 segundos
```

### Tienda.html
```javascript
✅ Abrir/cerrar carrito
✅ Agregar productos al carrito
✅ Eliminar productos del carrito
✅ Calcular total
✅ Actualizar contador de productos
✅ Mostrar/ocultar estado de carrito vacío
```

### Login.html / Registro.html
```javascript
✅ Toggle de visibilidad de contraseña
✅ Cambio de icono (ojo/ojo tachado)
```

---

## Redes Sociales

### Enlaces verificados en todas las páginas:
- ✅ Instagram: https://www.instagram.com/agrostar0?igsh=MWZ1N2NucG5xbGVobg==
- ✅ Twitter: https://x.com/AgroStar?s=09
- ✅ Facebook: https://www.facebook.com (en Contacto.html)
- ✅ TikTok: https://www.tiktok.com (en Contacto.html)

---

## Recursos CSS y JS

### Verificación de rutas:
- ✅ CSS Bootstrap: `static/bootstrap.min.css`
- ✅ CSS Bootstrap completo: `static/bootstrap-5.3.7-dist/`
- ✅ CSS personalizado: `css/tienda.css`, `css/estys.css`, etc.
- ✅ Iconos Bootstrap: CDN `bootstrap-icons@1.10.5`
- ✅ JavaScript Bootstrap: `static/bootstrap-5.3.7-dist/js/bootstrap.bundle.min.js`

---

## Resumen de Cambios Realizados

### ✅ Página de Contacto
1. **Crear** `Contacto.html` con:
   - Formulario completo con validación
   - Información de contacto
   - Redes sociales
   - FAQ section
   - Mapa integrado

### ✅ Principal.html
1. Agregar enlace a Contacto en navbar
2. Corregir Enlaces de navegación

### ✅ Plantas.html
1. Agregar enlace a Contacto en navbar
2. Actualizar navbar con estructura consistente

### ✅ Tienda.html
1. Agregar enlace a Contacto en menú móvil

### ✅ Login.html
1. Corregir enlace a Registro (Registro.html en lugar de registro.html)
2. Agregar enlace de regreso a Principal

### ✅ Registro.html
1. Corregir enlace a Login (Login.html en lugar de login.html)
2. Agregar enlace de regreso a Principal

---

## Estado Final: ✅ COMPLETO Y FUNCIONAL

Todas las páginas tienen:
- ✅ Navegación consistente
- ✅ Enlaces correctos (mayúsculas consistentes)
- ✅ Botones funcionales
- ✅ Formularios con validación
- ✅ Redes sociales integradas
- ✅ Diseño responsive

