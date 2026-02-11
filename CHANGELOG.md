# MIDI Lyric Checker v3.1 - Changelog / cambios en versión 3.1.

## Bug Fixes
- Fixed crash when pressing F5 (Refresh) with no file loaded
- Fixed crash when refreshing files with "No lyrics" track pairs
- Fixed accented characters displaying incorrectly (e.g., a showing as A¡, n as A±)
- Fixed MIDI channel setting not being preserved correctly when reopening Track Properties
- Fixed duplicate colon in MIDI device error messages
- Fixed UI layout so labels are properly paired with their controls for better screen reader navigation

## Improvements
- Note preview during navigation (Alt+Arrows) no longer blocks the interface, much more responsive
- Repeated syllables are now announced correctly (e.g., "la la la"), while melismas (multiple notes on one syllable) remain silent as expected. Navigating from a previous or next note into a previous or next melisma also correctly reads the syllable belonging to the melisma.
- File refresh (F5) now announces "File refreshed" and reuses the previous track pairing when the file structure hasn't changed
- Playback note tracking is now significantly faster on large MIDI files
- Removed unnecessary deep copy when loading files, faster load times
- Hardcoded Spanish text in track summary replaced with proper bilingual support

## New Features
- Copy lyrics to clipboard (Ctrl+C) with spoken confirmation
- Note name announcement toggle (F7) — announces pitch (e.g., C4, F#5) when navigating with Alt+Arrows
- Find in lyrics (Ctrl+F) with Find Next (F3) — search syllables and jump to matching positions
- MIDI port auto-recovery — automatically reconnects if the MIDI device is lost mid-session
- Skipped MIDI message reporting — announces count of failed messages after playback ends

## Code Quality
- All silent exception handlers now use `except Exception` instead of bare `except`
- Eliminated duplicate code across track loading, configuration, and refresh
- Removed unused internal variables
- Application now waits for playback and metronome threads to finish before closing
- Thread-safe UI updates during playback

# MIDI Lyric Checker v3.1 - Ccambios

## Arreglos de fallos, bugs
- Corregido el cierre inesperado al presionar F5 (Actualizar) sin archivos cargados.
- Corregido el error al actualizar archivos con pares de pistas marcados como "Sin letra".
- Por fin! Corregidos los caracteres acentuados que se mostraban incorrectamente en letra (por ejemplo. "á" como "A¡", "ñ" como "A±").
- Corregida la configuración del canal MIDI, que ahora se preserva correctamente al reabrir las Propiedades de Pista.
- Eliminado el doble punto en los mensajes de error de dispositivos MIDI.
- Ajustado el diseño de la interfaz para que las etiquetas estén correctamente emparejadas con sus controles, mejorando la navegación con lectores de pantalla.

## Mejoras
- La vista previa de notas durante la navegación (Alt+Flechas) ya no ralentiza la interfaz; es mucho más fluida.
- Las sílabas repetidas ahora se anuncian correctamente (Ejemplo. "la la la"), mientras que los melismas (múltiples notas sobre una sílaba) permanecen en silencio, como es debido. Al navegar hacia un melisma, ahora se lee correctamente la sílaba a la que pertenece.
- La actualización de archivo (F5) ahora anuncia "Archivo actualizado" y mantiene el emparejamiento de pistas previo si la estructura no ha cambiado.
- El seguimiento de notas en reproducción es significativamente más rápido en archivos MIDI de gran tamaño.
- Eliminada la copia profunda (deep copy) innecesaria al cargar archivos, logrando tiempos de carga más veloces.
- El texto en español que estaba fijo (hardcoded) en el resumen de pistas ha sido reemplazado por soporte bilingüe real.

## Funciones nuevas
- Copiar letra al portapapeles (Ctrl+C) y su confirmación hablada.
- Opción para anunciar el nombre de la nota en cifrado americano (F7): anuncia el tono (ej. C4, F#5) al navegar con Alt+Flechas. útil para cuando no hay audio disponible.
- Buscar en la letra (Ctrl+F) con Buscar Siguiente (F3): permite buscar sílabas y saltar a su posición.
- Autorrecuperación de puerto MIDI: reconexión automática si el dispositivo se pierde durante la sesión.
- Reporte de mensajes MIDI omitidos: anuncia el recuento de mensajes fallidos al terminar la reproducción.

## Calidad del código
- Todos los manejadores de excepciones silenciosos ahora usan `except Exception` en lugar de un `except` genérico.
- Eliminado el código duplicado en las funciones de carga de pistas, configuración y actualización.
- Eliminadas variables internas sin uso.
- La aplicación ahora espera a que los hilos de reproducción y metrónomo finalicen antes de cerrarse.
- Actualizaciones de la interfaz seguras entre hilos (thread-safe) durante la reproducción.
