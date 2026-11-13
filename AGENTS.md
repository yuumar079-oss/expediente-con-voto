# Entorno de trabajo y producción

El entorno de producción es el Codex Cloud guardado con este repositorio. Todas las generaciones y el montaje se ejecutan en una tarea que use ese entorno. No prometer que un secreto guardado esté disponible en otra conversación: comprobar la conexión real.

## Configuración inicial

Python, Pillow, ffmpeg, Blender y transcripción/alineación local. Reutilizar lo instalado; no pedir reinstalación por episodio. Usar el secreto personal de red AI33_API_KEY con api.ai33.pro permitido; no pedirlo en chat ni subirlo a Git. Reutilizar perfil.json y validar voz por la API. Guardar código y configuraciones en Git; guardar medios entregables en archivos descargables. El estado remoto de la producción final de propina no está necesariamente en Git: conservar audio y sincronización existentes antes de modificar nada.

## Flujo por episodio

1. Recibir tema, analizar conflictos y proponer opciones si el usuario no especificó caso.
2. Verificar fuentes oficiales mexicanas vigentes para contenido legal. Definir estado/municipio cuando corresponda. Distinguir votos legales y dilemas morales.
3. Preparar guion y headline corto, sin prometer viralidad. Esperar aprobación editorial una sola vez; si el usuario ya aprobó, continuar.
4. Escenario propio del tema, A azul/B rojo. No forzar carros fuera de tránsito.
5. Generar voz AI33 en dos tomas separadas por el conteo mudo. La primera termina después de pronunciar la pregunta de voto y ambas opciones. No pedir una aprobación adicional por créditos. Reutilizar audio y tareas existentes; no duplicar POST ambiguos.
6. Sincronizar palabras y planos a audio real. Montar efectos y renderizar. Verificar imágenes, literalidad, cierre <=0.6 s tras la última palabra, -14 LUFS y <=-1 dBTP.
7. Entregar MP4, breve descripción y fuentes. Actualizar estado del proyecto para poder retomar sin regenerar voz.

## Titulares y datos

La franja superior muestra el headline del video, leído de proyecto.json; nunca «EXPEDIENTE 01 / MÉXICO». Para propina: «¿PAGAS PROPINA?». La jurisdicción se conserva en las fuentes y metadatos, sin etiqueta fija superior. Titulares breves y legibles; los rótulos de escena pueden cambiar conforme avanza la explicación. Las opciones de voto deben corresponder a la pregunta vigente.

## Estado conocido

Guion, estilo visual y voz de propina en México aprobados. El usuario ya obtuvo un MP4 con narración de 68.67 s y solicitó reemplazar la etiqueta superior. Antes de volver a renderizar desde esta copia, localizar y conservar el audio y la alineación de la producción existente. animar.py en Git sigue siendo el compositor de la prueba muda y no sustituye por sí mismo al render final con voz.

## Corrección autorizada: pregunta de voto audible

El usuario detectó que el audio no plantea «¿Quién tiene la razón?» antes de las opciones y autorizó corregirlo. El texto vigente está en propina_mexico/guion_aprobado.json, campo correccion_audio. Generar solo la primera toma corrida con ese texto y reutilizar la segunda toma de la producción existente. No generar nuevas tomas de la segunda parte ni pedir otra aprobación de guion/créditos. Recalcular los tiempos de subtítulos, conteo y planos con el audio corregido; conservar headline «¿PAGAS PROPINA?». No ejecutar el compositor de prueba muda para sustituir el final con voz. Localizar los archivos de produccion existentes en el entorno y actualizar su montaje. Al verificar el nuevo MP4, confirmar explícitamente que se oye la pregunta antes de las opciones y que el conteo no lleva narración. Marcar la corrección como completada solo tras generar y revisar ese MP4.

Regla permanente: cada voto debe narrar la pregunta y describir las alternativas antes del conteo. El conflicto, el voto y la respuesta deben poder entenderse escuchando sin mirar la pantalla.
