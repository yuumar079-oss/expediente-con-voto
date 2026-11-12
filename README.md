# Expediente con voto

Proyecto de video vertical sobre propina voluntaria en México.

## Preparación

Python 3.11+, ffmpeg y Blender 4.2+. Instalar `pip install -r requirements.txt`.

El guion y el aspecto visual ya fueron aprobados. Falta generar dos tomas de voz en AI33 y sincronizar el video con su duración real. La prueba visual es muda; no se debe presentar como video final.

## Acceso AI33

Solicitar el secreto personal de red `AI33_API_KEY`, permitiendo `api.ai33.pro` en la red del entorno. No escribir el valor en archivos, Git ni mensajes. Comprobar `/v1/credits` y consultar voces mediante `ai33_api.py`; no generar voz hasta disponer de un ID válido. La autorización del guion ya incluye las dos tomas, sin otro OK por créditos.

## Reproducción visual

`blender -b -t 4 -P propina_mexico/escena.py`

`python propina_mexico/animar.py`

Los tiempos de la composición son provisionales. Para la versión final, usar marcas de voz reales, conteo sin narración, master de -14 LUFS y pico <= -1 dBTP.
