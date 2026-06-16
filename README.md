# CI/CD - Sistema de cebado de mate

Proyecto simple en Python y Flask para demostrar un proceso de integracion y
despliegue continuo.

## Flujo

1. Un `push` a la rama `main` actualiza el repositorio de GitHub.
2. GitHub Actions ejecuta las pruebas unitarias.
3. Si las pruebas pasan, GitHub Actions construye la imagen Docker.
4. Slack informa el resultado de la build.
5. Render espera que los controles de CI finalicen correctamente.
6. Render construye con el `Dockerfile` y despliega la aplicacion web.

```text
Desarrollador -> GitHub
                  |-> GitHub Actions -> tests -> Docker build -> Slack
                  |                         |
                  |                         v
                  |-> Render (After CI Checks Pass)
                        -> Docker build -> despliegue -> aplicacion web
```

La configuracion de Render se administra desde su panel, por eso el despliegue
no aparece como un paso dentro de `.github/workflows/ci.yml`.

Como Render despliega automaticamente despues de aprobarse los controles de
CI, este proyecto implementa despliegue continuo. Tambien cumple la condicion
de entrega continua, porque la aplicacion queda lista para ser desplegada, pero
el ultimo paso no requiere una aprobacion manual.

## Configuracion externa de Render

- Repositorio: `CarlaU13/CI-CD`
- Rama: `main`
- Runtime: Docker
- Auto-Deploy: `After CI Checks Pass`

Para recibir feedback del entorno desplegado en Slack:

1. En el workspace de Render, abrir `Integrations > Notifications`.
2. Elegir `Connect Slack`.
3. Seleccionar `All notifications`.

Esto complementa la notificacion de GitHub Actions: una informa el estado de
CI y la otra informa despliegues en Render.

## Prueba local

```powershell
python -m unittest -v test_mate.py
```

## Ejecucion con Docker

```powershell
docker build -t app-mate-flask .
docker run --rm -p 8000:8000 app-mate-flask
```
