# MIDI Lyric Checker v3.1 - Changelog

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
- Copy lyrics to clipboard (Ctrl+C) with audio confirmation
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
