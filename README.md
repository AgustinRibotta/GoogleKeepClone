

# Documentación de la API

Esta API permite gestionar **notas**, **relaciones usuario-nota**, y **archivos adjuntos**. Todos los endpoints requieren que el usuario esté autenticado mediante **username** y **password**.

---

## **Autenticación**

La autenticación es **básica** (username y password). El cliente debe incluir sus credenciales en cada solicitud usando el encabezado HTTP `Authorization`.


## **Endpoints**

### 1. **Gestión de Notas**

#### Crear una Nota

- **URL:** `/api/note/`
- **Método:** `POST`
- **Requiere Autenticación:** Sí
- **Descripción:** Crea una nueva nota asociada al usuario autenticado.

**Cuerpo de la Solicitud:**

```json
{
  "title": "Título de la Nota",
  "content": "Contenido de la nota"
}
```

**Respuesta Exitosa (201 Created):**

```json
{
  "id": 1,
  "title": "Título de la Nota",
  "content": "Contenido de la nota"
}
```

---

#### Ver Detalles de una Nota

- **URL:** `/api/note/<id>/`
- **Método:** `GET`
- **Requiere Autenticación:** Sí
- **Descripción:** Recupera los detalles de una nota específica asociada al usuario autenticado.

**Ejemplo de Respuesta Exitosa (200 OK):**

```json
{
  "id": 1,
  "title": "Título de la Nota",
  "content": "Contenido de la nota",
  "users": [
    {
      "user": {
        "id": 2,
        "username": "otro_usuario"
      }
    }
  ]
}
```

---

#### Actualizar una Nota

- **URL:** `/api/note/<id>/`
- **Método:** `PUT`
- **Requiere Autenticación:** Sí
- **Descripción:** Actualiza el título y contenido de una nota asociada al usuario autenticado.

**Cuerpo de la Solicitud:**

```json
{
  "title": "Nuevo Título",
  "content": "Contenido actualizado"
}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "id": 1,
  "title": "Nuevo Título",
  "content": "Contenido actualizado"
}
```

---

#### Eliminar una Nota

- **URL:** `/api/note/<id>/`
- **Método:** `DELETE`
- **Requiere Autenticación:** Sí
- **Descripción:** Elimina una nota asociada al usuario autenticado.

**Ejemplo de Respuesta Exitosa (204 No Content):**

No hay contenido en la respuesta.

---

### 2. **Relación Usuario-Nota**

#### Ver Notas Asociadas al Usuario

- **URL:** `/api/user-note/`
- **Método:** `GET`
- **Requiere Autenticación:** Sí
- **Descripción:** Lista todas las notas relacionadas con el usuario autenticado.

**Ejemplo de Respuesta Exitosa (200 OK):**

```json
[
  {
    "user": {
      "id": 1,
      "username": "tu_usuario"
    },
    "note": {
      "id": 1,
      "title": "Título de la Nota",
      "content": "Contenido de la nota"
    },
    "update_note_url": "/api/note/1/",
    "delete_note_url": "/api/note/1/",
    "retrieve_note_url": "/api/note/1/"
  }
]
```

---

#### Asociar un Usuario a una Nota

- **URL:** `/api/user-note/`
- **Método:** `POST`
- **Requiere Autenticación:** Sí
- **Descripción:** Crea una relación entre un usuario y una nota específica.

**Cuerpo de la Solicitud:**

```json
{
  "note": 1,
  "user": 2
}
```

**Ejemplo de Respuesta Exitosa (200 OK):**

```json
{
  "message": "El usuario fue agregado con éxito."
}
```

---

#### Eliminar Relación Usuario-Nota

- **URL:** `/api/user-note/<id>/`
- **Método:** `DELETE`
- **Requiere Autenticación:** Sí
- **Descripción:** Elimina la relación entre un usuario y una nota específica.

**Ejemplo de Respuesta Exitosa (204 No Content):**

No hay contenido en la respuesta.

---

### 3. **Gestión de Archivos Adjuntos**

#### Listar Archivos Adjuntos

- **URL:** `/api/attachment/`
- **Método:** `GET`
- **Requiere Autenticación:** Sí
- **Descripción:** Lista todos los archivos adjuntos de las notas asociadas al usuario autenticado.

**Ejemplo de Respuesta Exitosa (200 OK):**

```json
[
  {
    "id": 1,
    "note": 1,
    "file_path": "/media/uploads/archivo.pdf",
    "create_at": "2024-11-23T10:00:00Z"
  }
]
```

---

#### Subir un Archivo

- **URL:** `/api/attachment/`
- **Método:** `POST`
- **Requiere Autenticación:** Sí
- **Descripción:** Adjunta un archivo a una nota.

**Cuerpo de la Solicitud (Multipart):**

```multipart
note: 1
file_path: <archivo_a_subir>
```

**Ejemplo de Respuesta Exitosa (201 Created):**

```json
{
  "detail": "Archivo adjunto creado exitosamente.",
  "id": 1
}
```

---

#### Eliminar un Archivo

- **URL:** `/api/attachment/<id>/`
- **Método:** `DELETE`
- **Requiere Autenticación:** Sí
- **Descripción:** Elimina un archivo adjunto de una nota asociada.

**Ejemplo de Respuesta Exitosa (204 No Content):**

No hay contenido en la respuesta.

---


