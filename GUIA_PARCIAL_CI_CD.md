# Guia simple para el parcial de Integracion y Entrega Continua

## 1. Lo minimo que debo poder explicar

### Integracion continua (CI)

Es una practica de desarrollo de software en la que los cambios se integran
frecuentemente en un repositorio comun. Cada integracion dispara una build
automatica con pruebas para detectar errores lo antes posible.

Ideas clave:

- Es una practica, no solamente una herramienta.
- Los cambios deben ser pequenos y frecuentes.
- La build debe ejecutarse automaticamente.
- Debe haber pruebas automatizadas.
- El equipo debe recibir feedback rapido.
- Si la build falla, corregirla es prioridad.

### Build

Una build es el proceso que toma el codigo y verifica que el software funcione
como una unidad. Puede incluir preparacion del entorno, compilacion, pruebas,
inspeccion, empaquetado y despliegue.

Una build automatica es una build que comienza por un evento, por ejemplo un
`push`, sin que una persona tenga que ejecutar manualmente todos sus pasos.

En este proyecto, la build automatica:

1. Descarga el codigo.
2. Prepara Python 3.10.
3. Ejecuta las pruebas.
4. Construye una imagen Docker.
5. Informa el resultado por Slack.

### Pipeline

Es la secuencia automatizada de etapas por las que pasa el software.

Importante: pipeline y build no son exactamente lo mismo. El pipeline organiza
todo el flujo; la build es el proceso de construccion y verificacion que se
ejecuta dentro de ese flujo.

### Entrega y despliegue

- **Entrega continua (Continuous Delivery):** el software queda siempre listo
  para ser desplegado, pero una persona decide cuando enviarlo a produccion.
- **Despliegue continuo (Continuous Deployment):** cada cambio que supera todas
  las validaciones se despliega automaticamente a produccion.

Primero se necesita una buena integracion continua. Se puede tener CI sin
entrega continua, y entrega continua sin despliegue continuo.

### Feedback

Es la informacion rapida sobre el resultado del pipeline: si termino
correctamente, si fallaron pruebas o si no pudo construirse la aplicacion.

En este proyecto, GitHub Actions muestra el resultado y Slack envia la
notificacion incluso cuando un paso falla.

## 2. Componentes de mi solucion

| Componente pedido | Herramienta usada | Funcion |
| --- | --- | --- |
| Entorno del desarrollador | VS Code, Python y terminal | Escribir codigo y ejecutar la build local |
| Repositorio de codigo | Git y GitHub | Versionar y compartir los cambios |
| Servidor de CI | GitHub Actions | Ejecutar el pipeline en una maquina Ubuntu |
| Build local | `python -m unittest test_mate.py` | Verificar cambios antes del `push` |
| Prueba automatizada | `unittest` | Comprobar los tres rangos de temperatura |
| Empaquetado | Docker | Crear un entorno reproducible para la aplicacion |
| Aplicacion web | Flask | Mostrar el resultado de la logica en una pagina |
| Entorno de entrega | Render | Ejecutar y publicar la aplicacion web |
| Feedback | GitHub Actions y Slack | Comunicar el estado de la build |

Flujo completo:

`Desarrollador -> Git push -> GitHub`

Desde GitHub se activan dos automatizaciones:

- `GitHub Actions -> pruebas -> Docker build -> Slack`
- `Render -> construccion y despliegue -> aplicacion web publica`

## 3. Que hace cada archivo

### `mate.py`

Contiene la logica principal: la funcion `cebar_mate(temperatura_agua)`.

- Si la temperatura es 90 o mas, el agua esta demasiado caliente.
- Si es menor que 80, esta fria.
- Entre 80 y 89, la temperatura es ideal.

Es una funcion simple porque la consigna valora un ejemplo facil de demostrar.

### `test_mate.py`

Contiene tres pruebas unitarias:

- `test_temperatura_ideal` prueba 85 grados.
- `test_agua_hervida` prueba 90 grados.
- `test_agua_fria` prueba 75 grados.

Cada prueba compara el resultado real con el resultado esperado mediante
`assertEqual`. Son pruebas unitarias porque verifican una funcion pequena de
forma aislada.

### `app.py`

Crea una aplicacion web Flask. La ruta `/` llama a `cebar_mate` y muestra el
resultado dentro de una pagina HTML.

Actualmente llama a `cebar_mate(75)`, por eso la pagina muestra el estado de
agua fria. Este cambio no rompe las pruebas porque las pruebas validan
directamente la funcion de `mate.py`, no el valor elegido por la interfaz web.

### `Dockerfile`

Describe como construir la imagen:

1. Parte de una imagen liviana con Python 3.10.
2. define `/app` como directorio de trabajo.
3. Copia el proyecto.
4. Instala Flask.
5. documenta que la aplicacion usa el puerto 8000.
6. define `python app.py` como comando de inicio.

Docker ayuda a que la aplicacion se ejecute en un ambiente reproducible y evita
el problema de "en mi maquina funciona".

### `.github/workflows/ci.yml`

- `on: push` indica que el pipeline comienza con cada `push` a `main`.
- `runs-on: ubuntu-latest` solicita una maquina virtual Linux.
- `actions/checkout` descarga el repositorio.
- `actions/setup-python` instala Python 3.10.
- `python -m unittest test_mate.py` ejecuta las pruebas.
- `docker build` construye la imagen solo si las pruebas anteriores pasan.
- La accion de Slack informa el resultado.
- `if: always()` hace que Slack se ejecute aunque haya fallado un paso anterior.
- El webhook esta guardado como secreto para no publicar una credencial.

## 4. Como funciona el despliegue en Render

Render esta conectado al repositorio de GitHub y observa la rama configurada.
La opcion `After CI Checks Pass` hace que espere el resultado de GitHub Actions.
Si todos los controles pasan, construye la aplicacion usando el `Dockerfile`,
inicia el contenedor y publica la aplicacion web.

El despliegue no aparece como un paso dentro de `ci.yml` porque esta configurado
externamente desde el panel de Render. Render reconoce los controles generados
por GitHub Actions y espera que finalicen correctamente.

La explicacion correcta es:

> GitHub Actions ejecuta las pruebas, construye la imagen y envia feedback.
> Render funciona como entorno de entrega: detecta el cambio en GitHub,
> construye la aplicacion y la publica en una URL accesible.

Importante: la construccion de Docker en GitHub Actions no es el despliegue.
El despliegue ocurre cuando Render ejecuta y publica la aplicacion.

Como no existe una aprobacion manual despues de las pruebas, este flujo es
**despliegue continuo**. Tambien satisface la entrega continua, pero llega un
paso mas lejos: publica automaticamente cada cambio valido.

La ruta `/health` permite que Render compruebe el funcionamiento de la
aplicacion mediante HTTP. En Render se debe configurar:

- `Settings -> Health Check Path -> /health`
- `Integrations -> Notifications -> Connect Slack`
- Nivel de notificacion: `All notifications`

Asi Slack puede informar si un despliegue falla, si llega correctamente a
produccion o si el servicio se vuelve no saludable.

## 5. Guion oral de hasta 5 minutos

### Minuto 0 a 1: objetivo

> Implemente un ejemplo sencillo de integracion continua para una aplicacion de
> mate. La logica recibe la temperatura del agua y devuelve si esta fria, ideal
> o demasiado caliente. Elegi un ejemplo pequeno para poder concentrarme en el
> proceso de CI.

### Minuto 1 a 2: componentes

> Uso Git para control de versiones y GitHub como repositorio. Desarrollo con
> Python y puedo ejecutar las pruebas localmente. GitHub Actions funciona como
> servidor de integracion continua. Las pruebas estan hechas con unittest,
> Docker empaqueta la aplicacion y Slack funciona como mecanismo de feedback.

### Minuto 2 a 3: pipeline

> Cada push a main activa GitHub Actions. Este crea una maquina Ubuntu, descarga
> el codigo, instala Python 3.10 y ejecuta las tres pruebas. Si pasan, construye
> la imagen Docker. Finalmente envia a Slack el estado del trabajo. Render
> tambien detecta el cambio en GitHub y publica la aplicacion web.

### Minuto 3 a 4: demostracion

> Primero ejecuto las pruebas localmente. Despues muestro los archivos y hago un
> cambio pequeno. Lo subo al repositorio y enseño como GitHub Actions ejecuta el
> pipeline. Finalmente muestro el resultado, la notificacion de Slack, el
> despliegue de Render y la aplicacion funcionando desde su URL publica.

### Minuto 4 a 5: teoria y conclusion

> La integracion continua permite detectar errores temprano, reducir tareas
> manuales y obtener feedback rapido. No es solo GitHub Actions: tambien exige
> integrar frecuentemente, mantener pruebas automatizadas y reparar enseguida
> una build rota. Render completa el entorno de entrega al construir y publicar
> la aplicacion web desde el repositorio.

## 6. Demostracion ordenada

1. Mostrar `mate.py` y explicar sus tres resultados.
2. Mostrar `test_mate.py`.
3. Ejecutar:

   ```powershell
   python -m unittest -v test_mate.py
   ```

4. Mostrar el `Dockerfile`.
5. Mostrar el workflow y seguir sus pasos de arriba hacia abajo.
6. Hacer un cambio pequeno y entendible.
7. Crear el commit y hacer `push` a `main`.
8. Abrir la pestaña Actions de GitHub.
9. Mostrar cada paso exitoso o explicar exactamente cual fallo.
10. Mostrar el mensaje recibido en Slack.
11. Abrir el panel de Render y mostrar el ultimo despliegue.
12. Abrir la URL publica y mostrar la aplicacion funcionando.

Antes del parcial:

- Comprobar que Docker Desktop este iniciado.
- Comprobar que el secreto `SLACK_WEBHOOK_URL` siga configurado.
- Comprobar que el servicio de Render este activo y conectado a `main`.
- Tener anotada o abierta la URL publica de Render.
- No hacer cambios importantes a ultimo momento.
- Tener abierta la pestaña Actions y una ejecucion exitosa anterior.
- Tener abierto Render con un despliegue exitoso anterior.
- Recordar que el archivo `app.py` tiene cambios locales sin confirmar.

## 7. Preguntas probables y respuestas cortas

### ¿Que es integracion continua?

Es integrar cambios pequenos y frecuentes en un repositorio comun y verificar
cada integracion con una build y pruebas automatizadas.

### ¿CI es una herramienta?

No. Es una practica. GitHub Actions es una herramienta que ayuda a aplicarla.

### ¿Cual es el servidor de CI de tu proyecto?

GitHub Actions. Ejecuta el workflow en una maquina virtual Ubuntu.

### ¿Que evento dispara tu pipeline?

Un `push` a la rama `main`.

### ¿Que es la build local?

Es la verificacion que ejecuto en mi computadora antes de subir el cambio. En
este caso es `python -m unittest test_mate.py`.

### ¿Por que probar localmente si GitHub vuelve a probar?

Porque da feedback mas rapido y evita subir cambios que ya sabemos que estan
rotos. El servidor vuelve a probar en un ambiente limpio y compartido.

### ¿Que es una prueba unitaria?

Es una prueba automatizada de una unidad pequena y aislada. Aqui se prueba la
funcion `cebar_mate`.

### ¿Que ocurre si una prueba falla?

El comando devuelve un error, el job se detiene y no se construye la imagen
Docker. Slack igualmente informa el fallo por `if: always()`.

### ¿Por que se usa Docker?

Para empaquetar la aplicacion con su entorno y ejecutarla de manera consistente
en distintas maquinas.

### ¿`EXPOSE 8000` publica el puerto?

No. Documenta el puerto utilizado por la aplicacion. Al ejecutar el contenedor
se debe publicar, por ejemplo con `-p 8000:8000`.

### ¿Por que usar un secreto para Slack?

Porque el webhook es una credencial. Si se escribiera en el repositorio,
cualquier persona con acceso podria utilizarlo.

### ¿Que beneficios aporta CI?

Detecta errores temprano, reduce tareas manuales, mejora la visibilidad del
proyecto y aumenta la confianza en que el software funciona.

### ¿Por que convienen cambios pequenos?

Generan menos conflictos, son mas faciles de revisar y permiten encontrar con
mayor rapidez cual cambio produjo un error.

### ¿Que significa fail fast?

Detectar y comunicar un problema lo antes posible para reducir el costo y la
dificultad de corregirlo.

### ¿Diferencia entre CI, delivery y deployment?

CI integra y verifica. Delivery mantiene el software listo y una persona decide
cuando desplegar. Deployment envia automaticamente cada cambio valido.

### ¿Tu proyecto hace entrega o despliegue continuo?

Hace despliegue continuo. Render tiene configurado `After CI Checks Pass`, por
lo que espera que GitHub Actions termine correctamente y luego despliega sin
aprobacion manual. La configuracion de Render esta fuera de `ci.yml`.

### ¿Que mejorarias?

Agregaria un archivo de dependencias con versiones, publicaria la imagen en un
registro y agregaria una prueba automatizada que consulte la URL publica luego
del despliegue.

## 8. Errores de concepto que debo evitar

- Decir que CI significa solamente "usar GitHub Actions".
- Confundir `push` con `commit`: el commit es local; el push lo envia a GitHub.
- Decir que compilar o construir una imagen equivale a desplegar.
- Decir que Docker es una maquina virtual.
- Decir que una build es solamente compilar.
- Ocultar una build fallida en vez de explicar la causa.
- Afirmar que las pruebas cubren Flask: actualmente prueban la funcion de mate.

## 9. Resumen de memoria

> Hago un cambio pequeño, lo pruebo localmente, lo versiono con Git y lo envio a
> GitHub. El push dispara GitHub Actions. El servidor descarga el codigo,
> prepara Python, ejecuta las pruebas y construye una imagen Docker. Slack
> informa el resultado. Render detecta el cambio, despliega la aplicacion y la
> publica en una URL. Esto permite detectar errores temprano y mantener visible
> el estado del proyecto.

## 10. Fuentes usadas del material

- Consigna de la segunda instancia de evaluacion, paginas 1 y 2.
- Apunte Yoel, paginas 51 a 63: CI, build, pipeline, feedback y entrega continua.
- Apunte Yoel, paginas 166 y 167: preguntas de repaso de la unidad.
- Paul Duvall, *Continuous Integration*, capitulo 1.
- Jez Humble y David Farley, *Continuous Delivery*, capitulos 1 a 3.
