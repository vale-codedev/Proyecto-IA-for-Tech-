# Evidencia del deploy en OCI

Completa esta pagina cuando publiques la aplicacion en Oracle Cloud Infrastructure.

## Enlace publico

Pendiente:

```text
https://URL-DE-TU-APLICACION
```

## Captura de pantalla

Guarda una captura en `docs/assets/deploy_oci.png` y reemplaza esta referencia cuando exista el archivo:

```markdown
![Aplicacion desplegada en OCI](assets/deploy_oci.png)
```

## Opcion de despliegue sugerida con Docker

1. Construir la imagen:

```bash
docker build -t ia-for-tech-agent .
```

2. Ejecutar localmente para verificar:

```bash
docker run -p 8501:8501 ia-for-tech-agent
```

3. Publicar la imagen en un registro compatible con OCI.
4. Crear el servicio en OCI usando la imagen publicada.
5. Exponer el puerto `8501`.
6. Probar la URL publica.
7. Tomar una captura de pantalla de la aplicacion funcionando.

## Checklist de evidencia

- [ ] URL publica agregada al README o a este documento.
- [ ] Captura de pantalla agregada en `docs/assets/`.
- [ ] La captura muestra la aplicacion abierta y una respuesta generada por el agente.
- [ ] El repositorio contiene instrucciones para reproducir el despliegue.

