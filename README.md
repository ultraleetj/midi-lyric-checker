# English
## MIDI Lyric Checker

A fully portable application for reviewing MIDI files with synchronized lyrics display and announcement, designed for blind musicians, karaoke enthusiasts.
download: Fully compiled binary .exe file from releases section (at the bottom)

## Features

- **Fully portable app** - No installation required, runs standalone
- **Auto detection** of tracks with MIDI notes or lyrics, reads and displays track names from file
- **Multi-track support** - Select multiple track pairs to review
- **Configurable announcements** - Lyrics announcements can be turned on or off
- **Synchronized metronome** - Detects bars, tempo and time signatures, runs synchronously with playback
- **Customizable audio** - Configure sounds, pan, volume for tracks
- **MIDI device selection** - Dialog to select MIDI output device or use default
- **Manual navigation** - Step through notes manually for each track
- **Memory-based loading** - Loads file into RAM for quick refresh without reopening
- **Bilingual interface** - English and Spanish (default Spanish) with dynamic switching, no need to restart program at all.
- **Keyboard shortcuts** - For most tasks and functions

##  Requirements for building from source:

### Dependencies
- Python 3.7+
- wxPython (`pip install wxpython`)
- mido (`pip install mido`)
- python-rtmidi (`pip install python-rtmidi`) - For MIDI support
- accessible-output2 (`pip install accessible-output2`) - For screen reader support

### Optional Dependencies
- If MIDI libraries are not available, the application will run in limited mode without MIDI playback

## How to Use

### program overview
The app has three main elements: a list view with tracks, a lyrics display field, and a status field. You must load a file first. You can select the track that will be played using the list. Only one track plays at a time. The lyrics field will highlight and scroll the lyrics. Accented characters due to midi limitations will be shown as some strange symbols, this will hopefully be fixed at some point. The status field displays the note you are on, say, three out of 50, and the syllable as well, the tempo and the selected tracks for notes and lyrics.
Some notation or karaoke programs could put notes in one track, lyrics in another track, or both notes and lyrics in the same track. The program supports both and has automatic detection. To start, open a file. You will then select track pairs for: One track containing notes, and another track containing lyrics, or  simply accept or check the default detection. It is possible that lyrics may be incorrectly displayed for a track, but this will depend on the specific knoledge of which track has the corresponding lyrics to the notes track. If there are many voices to check in a file, in the case of chorales, you can select one or many pairs to review. There is also the possibility of  pairing a track with notes and no lyrics to use with instrumental accompanying parts for example.

### Navigation and playback controls
- **Space** - Play/Pause
- **Alt + Left/Right arrows** - Navigate between notes. Each syllable will be announced. In the case of a melisma (several notes using one syllable) the announcement will change only when the syllable changes.
- **Home/End** - Go to beginning/end of track
- **Page Up/Page Down** - Jump backward/forward by 8 notes
- **F4** - Toggle metronome
- **F6** - Toggle auto lyrics announcement

### Menus, Options
- **File > Open MIDI File** (Ctrl+O) - Load a new MIDI file
- **File > Configure Tracks** (Ctrl+T) - Reconfigure track pairs
- **File > Clear** (Ctrl+C) - Clear current file
- **File > Refresh** (F5) - Reload current file
- **File > Select midi device** Choose a different output device or select one of no default midi device is found.
- **File > Track Properties** (Ctrl+P) - Configure MIDI channel, instrument, bank, volume for a track
- **File > Metronome Settings** (Ctrl+M) - Configure tempo, metronome sounds. Uses channel 10 only.
- **Language menu** - Switch between English and Spanish

## File Support

- Standard MIDI files (.mid, .midi). You can rename files from .kar to .mid and they will work.
- Supports Type 0 and Type 1 MIDI files
- Reads lyrics from various MIDI text events (lyrics, text, markers, cue markers)
- Handles different text encodings automatically

## Technical Details

### MIDI Implementation
- Supports all 16 MIDI channels
- Configurable instruments (0-127)
- Bank select support (0-127)
- Volume control per track (0-127)
- Real-time MIDI output with synchronized timing

### Metronome Features
- Auto-detects tempo changes in MIDI file
- Supports time signature changes
- Configurable downbeat and upbeat sounds
- Synchronized with track playback timing

### Accessibility
- Various screen reader support (NVDA, windows narrator, jaws) via accessible-output2. Announces lyric syllables in the first beat  of each bar during playback and each one as you move manually through notes. Fully accessible interface via WX python.
- Keyboard-only navigation
- Status information display updates automatically.

## Troubleshooting

### MIDI Issues
- If no MIDI devices are found, check Windows audio settings and that you have installed a midi device or have a port available.
- Install or build using python-rtmidi for full MIDI support
- Try selecting a different MIDI device from the menu if no audio plays.

### File Loading Issues
- Ensure MIDI file is not corrupted
- Try refreshing the file if it was recently modified
- Check that the file contains both notes and lyrics.
- It is possible to rename .kar to .mid and check these.

# español
## MIDI Lyric Checker

Una aplicación completamente portable para revisar archivos MIDI con visualización y audición sincronizada de letras, diseñada para músicos ciegos, entusiastas del karaoke.
Descargar: Archivo ejecutable binario (compilado) desde la sección releases, abajo.

## Funciones

- **Programa completamente portable** - No requiere instalación, funciona desde un solo archivo
- **Detección automática** de pistas con notas MIDI o letras, lee y muestra nombres de pistas del archivo
- **Soporte multi-pista** - Selecciona múltiples parejas de pistas para revisar
- **Anuncios configurables** - Los anuncios de letras se pueden activar o desactivar
- **Metrónomo sincronizado** - Detecta compases, tempo y métricas, funciona sincrónicamente con la reproducción
- **Audio personalizable** - Configura sonidos, balance, volumen para pistas
- **Selección de dispositivo MIDI** - Diálogo para seleccionar dispositivo de salida MIDI o usar predeterminado
- **Navegación manual** - Avanza manualmente por las notas de cada pista
- **Carga en memoria** - Carga archivo en memoria RAM para actualización rápida sin reabrir archivo o reiniciar el programa.
- **Interfaz bilingüe** - Inglés y español (predeterminado español) con cambio dinámico entre idiomas
- **Atajos de teclado** - Para la mayoría de tareas y funciones

## Requisitos para construir desde código fuente

### Dependencias
- Python 3.7+
- wxPython (`pip install wxpython`)
- mido (`pip install mido`)
- python-rtmidi (`pip install python-rtmidi`) - Para soporte MIDI
- accessible-output2 (`pip install accessible-output2`) - Para soporte de lectores de pantalla

### Dependencias Opcionales
- Si las librerías MIDI no están disponibles, la aplicación funcionará en modo limitado sin reproducción MIDI
## Cómo usar

### Descripción general del programa
La aplicación tiene tres elementos principales: una vista de lista con pistas, un campo de visualización de letras y un campo de estado. Primero se debe cargar un archivo. se puede seleccionar la pista que se reproducirá usando la lista. Solo una pista se reproduce a la vez. El campo de letras subraya y desplaza la letra a medida que se reproduce el archivo. Debido a las limitaciones MIDI los caracteres acentuados se mostrarán como algunos símbolos extraños, con suerte solucionaré esto en algún momento. El campo de estado muestra la nota en la que se encuentra, digamos, tres de 50, y la sílaba también, el tempo actual, y las pistas que fueron seleccionadas para notas y letras.
Algunos programas de notación o karaoke podrían poner notas en una pista, letras en otra pista, o ambas: notas y letras en la misma pista. El programa admite ambos casos y tiene detección automática. Para comenzar, abra un archivo midi. Luego deberá seleccionar las parejas de pistas, una que contenga notas y otra que contenga letras, o simplemente acepete o verifique la detección automática. Es posible que las letras no se muestren correctamente, pero ya dependerá del conocimiento exacto de cual pista con letra corresponde a cual pista con notas. Si hay muchas voces para verificar en un archivo, en el caso de los corales, se puede seleccionar una o varias parejas para revisar. También existe la posibilidad de combinar una pista con notas con la opción sin letras.

### Controles de Navegación y reproducción
- **Espacio** - Reproducir/Pausa
- **Alt + Flechas izquierda/derecha** - Navegar manualmente entre notas. Se anunciará cada sílaba. En el caso de melisma (varias notas que usan la misma sílaba) se anunciará solo cuando cambie la sílaba.
- **Inicio/Fin** - Ir al principio/final
- **Retroceso /Avance Página** - Saltar hacia atrás/adelante 8 notas
- **F4** - Encender apagar metrónomo
- **F6** - Encender apagar anuncio  automático de letras

### Opciones del Menú
- **Archivo > Abrir Archivo MIDI** (Ctrl+O) - Cargar nuevo archivo MIDI
- **Archivo > Configurar Pistas** (Ctrl+T) - Reconfigurar parejas de pistas
- **Archivo > Limpiar** (Ctrl+C) - Limpiar o cerrar archivo actual, descargar de memoria.
- **Archivo > Actualizar** (F5) - Recargar archivo actual
- **Archivo > Seleccionar dispositivo MIDI** - Elija un dispositivo de salida diferente o seleccione uno si no se encuentra el dispositivo MIDI predeterminado.
- **Archivo > Propiedades de Pista** (Ctrl+P) - Configurar pista MIDI, instrumento, banco, volumen
- **Archivo > Configuración de Metrónomo** (Ctrl+M) - Configurar tempo, sonidos del metrónomo. Se usa únicamente el canal midi 10
- **menú Idioma** - Cambiar entre inglés y español

## Soporte de Archivos

- Archivos MIDI estándar (.mid, .midi). También se pueden renombrar archivos de .kar a .mid y funcionarán correctamente.
- Soporta archivos MIDI Tipo 0 y Tipo 1
- Lee letras de varios eventos de texto MIDI (lyrics, text, markers, cue markers)
- Maneja diferentes codificaciones de texto automáticamente

## Detalles Técnicos

### Implementación MIDI
- Soporta los 16 canales MIDI
- Instrumentos configurables (0-127)
- Soporte de selección de banco (0-127)
- Control de volumen por pista (0-127)
- Salida MIDI en tiempo real con sincronización temporal

### Características del Metrónomo
- Auto-detecta cambios de tempo en el archivo MIDI
- Soporta cambios de métrica
- Sonidos configurables para tiempo fuerte y débil, usando únicamente el canal 10.
- Sincronizado con  tiempo real y reproducción de pista

### Accesibilidad
- Soporte para varios lectores de pantalla (jaws, narrador de windows, nvda) usando accessible-output2. Anuncia las sílabas cada primer tiempo de cada compás, y  cada una cuando se mueve manualmente. Interfaz de usuario completamente accesible mediante wx Python.
- Navegación solo con teclado
- Visualización clara de información de estado se actualiza automáticamente.

## Solución de Problemas

### Problemas MIDI
- Si no se encuentran dispositivos MIDI, revise la configuración de audio de Windows y que estén libres los puertos o dispositivos midi en caso de que no haya audio sonando.
- Compile incluyendo python-rtmidi para soporte MIDI completo
- Intenta seleccionar un dispositivo MIDI diferente desde el menú.

### Problemas de Carga de Archivos
- Asegurarse de que el archivo MIDI no esté corrupto
- Intente actualizar el archivo si fue modificado recientemente
- Verifique que el archivo contenga tanto notas como letra.

## License / Licencia

This project is open source. Feel free to modify and distribute according to your needs.

Este proyecto es código abierto. Siéntete libre de modificar y distribuir según tus necesidades.

## Contributing / Contribuyendo

Contributions are welcome! Please feel free to submit issues and enhancement requests.

¡Las contribuciones son bienvenidas! Por favor siéntete libre de enviar problemas y solicitudes de mejoras.

