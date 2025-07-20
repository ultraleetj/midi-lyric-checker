import os
import sys
import time
import threading
import copy

# Handle PyInstaller
if getattr(sys, 'frozen', False):
    sys.path.insert(0, sys._MEIPASS)

# MIDI imports with fallback
try:
    from mido import MidiFile, Message, open_output, get_output_names
    MIDI_AVAILABLE = True
except ImportError:
    MIDI_AVAILABLE = False
    class MidiFile:
        def __init__(self, *args, **kwargs):
            self.tracks = []
            self.ticks_per_beat = 480
            self.filename = args[0] if args else "unknown"
    class Message:
        def __init__(self, *args, **kwargs):
            self.type = kwargs.get('type', 'note_on')
            self.note = kwargs.get('note', 60)
            self.velocity = kwargs.get('velocity', 100)
            self.channel = kwargs.get('channel', 0)
            self.time = 0
    def get_output_names():
        return []
    def open_output(name):
        return None

# TTS imports with fallback
try:
    from accessible_output2.outputs.auto import Auto
except ImportError:
    class Auto:
        def speak(self, text, interrupt=False):
            pass

import wx

# Language strings
STRINGS = {
    'en': {
        'title': 'MIDI Lyric Checker',
        'track_config': 'Track Configuration',
        'config_instructions': 'Configure track pairing for notes and lyrics:',
        'add_pair': 'Add Pair',
        'ok': 'OK',
        'cancel': 'Cancel',
        'remove': 'Remove',
        'notes': 'Notes:',
        'lyrics': 'Lyrics:',
        'no_lyrics': 'No lyrics',
        'track_properties': 'Track Properties',
        'midi_channel': 'MIDI Channel (1-16):',
        'instrument': 'Instrument (0-127):',
        'bank': 'Bank (0-127):',
        'volume': 'Volume (0-127):',
        'metronome_settings': 'Metronome Settings',
        'tempo_bpm': 'Tempo (BPM):',
        'downbeat_note': 'Downbeat Note:',
        'upbeat_note': 'Upbeat Note:',
        'enable_metronome': 'Enable Metronome',
        'track_pairs': 'Track Pairs:',
        'status': 'Status:',
        'controls': 'Space=Play/Pause, Alt+Arrows=Navigate, Home/End=Start/End, F4=Metronome, F6=Auto Announce',
        'open_midi': '&Open MIDI File\tCtrl+O',
        'configure_tracks': '&Configure Tracks\tCtrl+T',
        'clear': '&Clear\tCtrl+C',
        'refresh': '&Refresh file\tF5',
        'select_midi_device': '&Select MIDI Device',
        'track_properties_menu': '&Track Properties\tCtrl+P',
        'metronome_settings_menu': '&Metronome Settings\tCtrl+M',
        'toggle_metronome': '&Toggle Metronome\tF4',
        'toggle_auto_announce': '&Toggle Auto Announce\tF6',
        'quit': '&Quit\tCtrl+Q',
        'file_menu': '&File',
        'language_menu': '&Language',
        'english': 'English',
        'spanish': 'Español',
        'paused': 'Paused',
        'playing': 'Playing',
        'beginning': 'Beginning',
        'end': 'End',
        'position': 'Position',
        'metronome_on': 'Metronome on',
        'metronome_off': 'Metronome off',
        'auto_announce_on': 'Auto announce on',
        'auto_announce_off': 'Auto announce off',
        'midi_device': 'MIDI device:',
        'no_file_loaded': 'Please load a MIDI file first.',
        'no_file_loaded_title': 'No File Loaded',
        'midi_not_available': 'MIDI backend not available.\nInstall python-rtmidi to enable MIDI support.',
        'midi_not_available_title': 'MIDI Not Available',
        'no_midi_devices': 'No MIDI devices found.',
        'no_midi_devices_title': 'No MIDI Devices',
        'select_midi_device_title': 'MIDI Devices',
        'select_midi_device_prompt': 'Select MIDI Output Device:',
        'error': 'Error',
        'error_opening_device': 'Error opening device:',
        'error_accessing_midi': 'Error accessing MIDI devices:',
        'error_loading_midi': 'Error loading MIDI:',
        'open_midi_file': 'Open MIDI file',
        'midi_files': 'MIDI files (*.mid;*.midi)|*.mid;*.midi',
        'loaded_tracks': 'Loaded',
        'notes_word': 'notes',
        'lyrics_found': 'lyrics',
        'track_pair': 'Pair',
        'no_track_pair': 'No track pair selected',
        'no_notes_pair': 'No notes available in selected pair',
        'no_lyrics_found': 'No lyrics found for this track pair',
        'no_notes_track': 'No notes in this track pair',
        'pair_prefix': 'Pair',
        'notes_prefix': 'Notes=Track',
        'lyrics_prefix': 'Lyrics=Track',
        'none': 'None',
        'note': 'Note',
        'of': 'of',
        'track': 'Track',
        'lyrics_in_pair': 'Lyrics in pair:',
        'midi_status': 'MIDI:',
        'metronome': 'Metronome:',
        'auto_announce': 'Auto announce:',
        'on': 'On',
        'off': 'Off',
        'yes': 'Yes',
        'no': 'No'
    },
    'es': {
        'title': 'Verificador de Letras MIDI',
        'track_config': 'Configuración de Pistas',
        'config_instructions': 'Selecciona  la pareja de pistas para notas y letras, o simplemente revisa y acepta la detección automática:',
        'add_pair': 'Agregar Pareja',
        'ok': 'Aceptar',
        'cancel': 'Cancelar',
        'remove': 'Quitar',
        'notes': 'Notas:',
        'lyrics': 'Letras:',
        'no_lyrics': 'Sin letras',
        'track_properties': 'Propiedades de Pista',
        'midi_channel': 'Canal MIDI (1-16):',
        'instrument': 'Instrumento (0-127):',
        'bank': 'Banco (0-127):',
        'volume': 'Volumen (0-127):',
        'metronome_settings': 'Configuración de Metrónomo',
        'tempo_bpm': 'Tempo (BPM):',
        'downbeat_note': 'Nota de Tiempo Fuerte:',
        'upbeat_note': 'Nota de Tiempo Débil:',
        'enable_metronome': 'Activar Metrónomo',
        'track_pairs': 'Parejas de Pistas:',
        'status': 'Estado:',
        'controls': 'Espacio=Reproducir/Pausa, Alt+Flechas=Navegar, Inicio/Fin=Principio/Final, F4=Metrónomo, F6=Activar desactivar Anuncios',
        'open_midi': '&Abrir Archivo MIDI\tCtrl+O',
        'configure_tracks': '&Configurar Pistas\tCtrl+T',
        'clear': '&Limpiar\tCtrl+C',
        'refresh': '&Actualizar\tF5',
        'select_midi_device': '&Seleccionar Dispositivo MIDI',
        'track_properties_menu': '&Propiedades de Pista\tCtrl+P',
        'metronome_settings_menu': '&Configuración de Metrónomo\tCtrl+M',
        'toggle_metronome': '&Alternar Metrónomo\tF4',
        'toggle_auto_announce': '&Alternar Anuncios\tF6',
        'quit': '&Salir\tCtrl+Q',
        'file_menu': '&Archivo',
        'language_menu': '&Idioma - language',
        'english': 'English',
        'spanish': 'Español',
        'paused': 'Pausado',
        'playing': 'Reproduciendo',
        'beginning': 'Principio',
        'end': 'Final',
        'position': 'Posición',
        'metronome_on': 'Metrónomo activado',
        'metronome_off': 'Metrónomo desactivado',
        'auto_announce_on': 'Anuncio automático activado',
        'auto_announce_off': 'Anuncio automático desactivado',
        'midi_device': 'Dispositivo MIDI:',
        'no_file_loaded': 'Por favor carga un archivo MIDI primero.',
        'no_file_loaded_title': 'Archivo No Cargado',
        'midi_not_available': 'Backend MIDI no disponible.\nInstala python-rtmidi para habilitar soporte MIDI.',
        'midi_not_available_title': 'MIDI No Disponible',
        'no_midi_devices': 'No se encontraron dispositivos MIDI.',
        'no_midi_devices_title': 'Sin Dispositivos MIDI',
        'select_midi_device_title': 'Dispositivos MIDI',
        'select_midi_device_prompt': 'Seleccionar Dispositivo de Salida MIDI:',
        'error': 'Error',
        'error_opening_device': 'Error al abrir dispositivo:',
        'error_accessing_midi': 'Error al acceder a dispositivos MIDI:',
        'error_loading_midi': 'Error al cargar MIDI:',
        'open_midi_file': 'Abrir archivo MIDI',
        'midi_files': 'Archivos MIDI (*.mid;*.midi)|*.mid;*.midi',
        'loaded_tracks': 'Cargado',
        'notes_word': 'notas',
        'lyrics_found': 'letras',
        'track_pair': 'Pareja',
        'no_track_pair': 'No hay pareja de pistas seleccionada',
        'no_notes_pair': 'No hay notas disponibles en la pareja seleccionada',
        'no_lyrics_found': 'No se encontraron letras para esta pareja de pistas',
        'no_notes_track': 'No hay notas en esta pareja de pistas',
        'pair_prefix': 'Pareja',
        'notes_prefix': 'Notas=Pista',
        'lyrics_prefix': 'Letras=Pista',
        'none': 'Ninguna',
        'note': 'Nota',
        'of': 'de',
        'track': 'Pista',
        'lyrics_in_pair': 'Letras en pareja:',
        'midi_status': 'MIDI:',
        'metronome': 'Metrónomo:',
        'auto_announce': 'Anuncio de letras:',
        'on': 'Activado',
        'off': 'Desactivado',
        'yes': 'Sí',
        'no': 'No'
    }
}

class LanguageManager:
    def __init__(self):
        self.current_language = 'es'  # Spanish as default
        
    def set_language(self, lang):
        if lang in STRINGS:
            self.current_language = lang
            
    def get(self, key):
        return STRINGS.get(self.current_language, STRINGS['en']).get(key, key)

# Global language manager
lang = LanguageManager()

class TrackPairingDialog(wx.Dialog):
    def __init__(self, parent, track_info):
        super().__init__(parent, title=lang.get('track_config'), size=(500, 400))
        self.track_info = track_info
        self.track_pairs = []
        
        # Create filtered lists for selection
        self.notes_tracks = []  # Tracks with notes
        self.lyrics_tracks = []  # Tracks with lyrics (or option for no lyrics)
        
        # Filter tracks with notes for notes selection
        for i, (name, has_notes, has_lyrics) in enumerate(track_info):
            if has_notes:
                self.notes_tracks.append((i, name))
        
        # Filter tracks with lyrics for lyrics selection, plus "No lyrics" option
        for i, (name, has_notes, has_lyrics) in enumerate(track_info):
            if has_lyrics:
                self.lyrics_tracks.append((i, name))
        # Always add "No lyrics" option at the end
        self.lyrics_tracks.append((None, lang.get('no_lyrics')))
        
        self.init_ui()
        
    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        instructions = wx.StaticText(panel, label=lang.get('config_instructions'))
        vbox.Add(instructions, 0, wx.ALL, 10)
        
        # Track pairing area
        self.pairing_panel = wx.ScrolledWindow(panel)
        self.pairing_panel.SetScrollRate(5, 5)
        self.pairing_sizer = wx.BoxSizer(wx.VERTICAL)
        self.pairing_panel.SetSizer(self.pairing_sizer)
        vbox.Add(self.pairing_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Buttons
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(panel, label=lang.get('add_pair'))
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_pair)
        btn_box.Add(add_btn, 0, wx.ALL, 5)
        
        btn_box.Add(wx.Button(panel, wx.ID_OK, lang.get('ok')), 0, wx.ALL, 5)
        btn_box.Add(wx.Button(panel, wx.ID_CANCEL, lang.get('cancel')), 0, wx.ALL, 5)
        vbox.Add(btn_box, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        panel.SetSizer(vbox)
        
        # Initialize with suggested pairing
        self.auto_suggest_pairs()
        
    def auto_suggest_pairs(self):
        # Clear existing pairs
        self.pairing_sizer.Clear(True)
        self.track_pairs.clear()
        
        # Suggest pairs based on track content
        notes_indices = [i for i, (_, has_notes, _) in enumerate(self.track_info) if has_notes]
        lyrics_indices = [i for i, (_, _, has_lyrics) in enumerate(self.track_info) if has_lyrics]
        
        # Strategy 1: Same track has both notes and lyrics
        same_track_pairs = []
        for i, (name, has_notes, has_lyrics) in enumerate(self.track_info):
            if has_notes and has_lyrics:
                same_track_pairs.append((i, i))
        
        if same_track_pairs:
            # Use same-track pairs
            for notes_track, lyrics_track in same_track_pairs:
                notes_selection = self.get_notes_track_index(notes_track)
                lyrics_selection = self.get_lyrics_track_index(lyrics_track)
                self.add_track_pair(notes_selection, lyrics_selection)
        else:
            # Strategy 2: Separate tracks - try alternating pattern
            for i, notes_track_idx in enumerate(notes_indices):
                lyrics_track_idx = None
                # Try to find a lyrics track after this notes track
                for lyrics_idx in lyrics_indices:
                    if lyrics_idx > notes_track_idx:
                        lyrics_track_idx = lyrics_idx
                        break
                
                notes_selection = self.get_notes_track_index(notes_track_idx)
                if lyrics_track_idx is not None:
                    lyrics_selection = self.get_lyrics_track_index(lyrics_track_idx)
                else:
                    lyrics_selection = len(self.lyrics_tracks) - 1  # "No lyrics"
                
                self.add_track_pair(notes_selection, lyrics_selection)
        
        # If no pairs were suggested, add at least one empty pair
        if not self.track_pairs:
            self.add_track_pair()
        
        self.pairing_panel.FitInside()
    
    def get_notes_track_index(self, track_idx):
        """Get the index in the filtered notes_tracks list"""
        for i, (idx, _) in enumerate(self.notes_tracks):
            if idx == track_idx:
                return i
        return 0
    
    def get_lyrics_track_index(self, track_idx):
        """Get the index in the filtered lyrics_tracks list"""
        if track_idx is None:
            return len(self.lyrics_tracks) - 1  # "No lyrics" option
        for i, (idx, _) in enumerate(self.lyrics_tracks):
            if idx == track_idx:
                return i
        return len(self.lyrics_tracks) - 1  # Default to "No lyrics"
        
    def add_track_pair(self, notes_track=0, lyrics_track=0):
        pair_panel = wx.Panel(self.pairing_panel)
        pair_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Notes track selection (filtered to only tracks with notes)
        pair_sizer.Add(wx.StaticText(pair_panel, label=lang.get('notes')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        notes_choices = [name for _, name in self.notes_tracks]
        notes_choice = wx.Choice(pair_panel, choices=notes_choices)
        if notes_choices:  # Only set selection if there are choices
            notes_choice.SetSelection(min(notes_track, len(notes_choices) - 1))
        pair_sizer.Add(notes_choice, 1, wx.ALL, 5)
        
        # Lyrics track selection (filtered to only tracks with lyrics + "No lyrics")
        pair_sizer.Add(wx.StaticText(pair_panel, label=lang.get('lyrics')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        lyrics_choices = [name for _, name in self.lyrics_tracks]
        lyrics_choice = wx.Choice(pair_panel, choices=lyrics_choices)
        if lyrics_choices:  # Only set selection if there are choices
            lyrics_choice.SetSelection(min(lyrics_track, len(lyrics_choices) - 1))
        pair_sizer.Add(lyrics_choice, 1, wx.ALL, 5)
        
        # Remove button
        remove_btn = wx.Button(pair_panel, label=lang.get('remove'))
        remove_btn.Bind(wx.EVT_BUTTON, lambda evt: self.remove_pair(pair_panel))
        pair_sizer.Add(remove_btn, 0, wx.ALL, 5)
        
        pair_panel.SetSizer(pair_sizer)
        self.pairing_sizer.Add(pair_panel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.track_pairs.append((notes_choice, lyrics_choice))
        self.pairing_panel.FitInside()
        
    def remove_pair(self, pair_panel):
        # Find and remove the pair
        for i, (notes_choice, lyrics_choice) in enumerate(self.track_pairs):
            if notes_choice.GetParent() == pair_panel:
                del self.track_pairs[i]
                break
        
        pair_panel.Destroy()
        self.pairing_panel.FitInside()
        
    def on_add_pair(self, event):
        self.add_track_pair()
        
    def get_track_pairs(self):
        pairs = []
        for notes_choice, lyrics_choice in self.track_pairs:
            # Get the actual track indices from the filtered lists
            notes_selection = notes_choice.GetSelection()
            lyrics_selection = lyrics_choice.GetSelection()
            
            if notes_selection >= 0 and notes_selection < len(self.notes_tracks):
                notes_track = self.notes_tracks[notes_selection][0]
                
                if lyrics_selection >= 0 and lyrics_selection < len(self.lyrics_tracks):
                    lyrics_track = self.lyrics_tracks[lyrics_selection][0]
                else:
                    lyrics_track = None  # "No lyrics" selected
                
                pairs.append((notes_track, lyrics_track))
        
        return pairs

class TrackPropertiesDialog(wx.Dialog):
    def __init__(self, parent, channel=1, instrument=1, bank=0, volume=100):
        super().__init__(parent, title=lang.get('track_properties'), size=(350, 300))
        self.channel = channel
        self.instrument = instrument
        self.bank = bank
        self.volume = volume
        self.init_ui()
        
    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Channel (1-16)
        channel_box = wx.BoxSizer(wx.HORIZONTAL)
        channel_box.Add(wx.StaticText(panel, label=lang.get('midi_channel')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.channel_spin = wx.SpinCtrl(panel, value=str(self.channel), min=1, max=16)
        channel_box.Add(self.channel_spin, 0, wx.ALL, 5)
        
        # Instrument (0-127)
        inst_box = wx.BoxSizer(wx.HORIZONTAL)
        inst_box.Add(wx.StaticText(panel, label=lang.get('instrument')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.inst_spin = wx.SpinCtrl(panel, value=str(self.instrument), min=0, max=127)
        inst_box.Add(self.inst_spin, 0, wx.ALL, 5)
        
        # Bank (0-127)
        bank_box = wx.BoxSizer(wx.HORIZONTAL)
        bank_box.Add(wx.StaticText(panel, label=lang.get('bank')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.bank_spin = wx.SpinCtrl(panel, value=str(self.bank), min=0, max=127)
        bank_box.Add(self.bank_spin, 0, wx.ALL, 5)
        
        # Volume (0-127)
        vol_box = wx.BoxSizer(wx.HORIZONTAL)
        vol_box.Add(wx.StaticText(panel, label=lang.get('volume')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.vol_spin = wx.SpinCtrl(panel, value=str(self.volume), min=0, max=127)
        vol_box.Add(self.vol_spin, 0, wx.ALL, 5)
        
        # Buttons
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_box.Add(wx.Button(panel, wx.ID_OK, lang.get('ok')), 0, wx.ALL, 5)
        btn_box.Add(wx.Button(panel, wx.ID_CANCEL, lang.get('cancel')), 0, wx.ALL, 5)
        
        vbox.Add(channel_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(inst_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(bank_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(vol_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(btn_box, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        panel.SetSizer(vbox)
        
    def get_values(self):
        return {
            'channel': self.channel_spin.GetValue() - 1,  # Convert to 0-15 for MIDI
            'instrument': self.inst_spin.GetValue(),
            'bank': self.bank_spin.GetValue(),
            'volume': self.vol_spin.GetValue()
        }

class MetronomeDialog(wx.Dialog):
    def __init__(self, parent, tempo=120, downbeat_note=76, upbeat_note=77, enabled=False):
        super().__init__(parent, title=lang.get('metronome_settings'), size=(350, 250))
        self.tempo = tempo
        self.downbeat_note = downbeat_note
        self.upbeat_note = upbeat_note
        self.enabled = enabled
        self.init_ui()
        
    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Tempo
        tempo_box = wx.BoxSizer(wx.HORIZONTAL)
        tempo_box.Add(wx.StaticText(panel, label=lang.get('tempo_bpm')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.tempo_spin = wx.SpinCtrl(panel, value=str(self.tempo), min=60, max=200)
        tempo_box.Add(self.tempo_spin, 0, wx.ALL, 5)
        
        # Downbeat note
        down_box = wx.BoxSizer(wx.HORIZONTAL)
        down_box.Add(wx.StaticText(panel, label=lang.get('downbeat_note')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.down_spin = wx.SpinCtrl(panel, value=str(self.downbeat_note), min=35, max=81)
        down_box.Add(self.down_spin, 0, wx.ALL, 5)
        
        # Upbeat note
        up_box = wx.BoxSizer(wx.HORIZONTAL)
        up_box.Add(wx.StaticText(panel, label=lang.get('upbeat_note')), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.up_spin = wx.SpinCtrl(panel, value=str(self.upbeat_note), min=35, max=81)
        up_box.Add(self.up_spin, 0, wx.ALL, 5)
        
        # Enable checkbox
        self.enable_check = wx.CheckBox(panel, label=lang.get('enable_metronome'))
        self.enable_check.SetValue(self.enabled)
        
        # Buttons
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_box.Add(wx.Button(panel, wx.ID_OK, lang.get('ok')), 0, wx.ALL, 5)
        btn_box.Add(wx.Button(panel, wx.ID_CANCEL, lang.get('cancel')), 0, wx.ALL, 5)
        
        vbox.Add(tempo_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(down_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(up_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.enable_check, 0, wx.ALL, 5)
        vbox.Add(btn_box, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        panel.SetSizer(vbox)
        
    def get_values(self):
        return {
            'tempo': self.tempo_spin.GetValue(),
            'downbeat_note': self.down_spin.GetValue(),
            'upbeat_note': self.up_spin.GetValue(),
            'enabled': self.enable_check.GetValue()
        }

class MidiLyricChecker(wx.Frame):
    def __init__(self):
        super().__init__(None, title=lang.get('title'), size=(800, 600))
        
        # Core components
        self.output = Auto()
        self.midi_data = None
        self.output_port = None
        self.play_thread = None
        
        # Data structures
        self.track_names = []
        self.track_pairs = []
        self.notes = []
        self.timed_lyrics = []
        self.track_properties = {}
        
        # State variables
        self.current_pair = 0
        self.current_note_index = 0
        self.playing = False
        
        # Metronome settings
        self.metronome_enabled = False
        self.tempo = 120
        self.downbeat_note = 76
        self.upbeat_note = 77
        self.beat_count = 0
        self.metronome_thread = None
        # Accessibility settings
        self.auto_announce_lyrics = True
        self.last_announced_lyric = None
        self.current_single_lyric = None
        
        # UI elements for language updates
        self.track_label = None
        self.lyric_label = None
        self.status_label = None
        self.instructions = None
        
        self.init_ui()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Auto-select MIDI device
        wx.CallAfter(self.auto_select_default_midi)

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.create_menu()

        # Track list
        self.track_label = wx.StaticText(panel, label=lang.get('track_pairs'))
        vbox.Add(self.track_label, 0, wx.EXPAND | wx.ALL, 5)
        self.track_list = wx.ListBox(panel)
        self.track_list.Bind(wx.EVT_LISTBOX, self.on_track_select)

        # Lyric display
        self.lyric_label = wx.StaticText(panel, label=lang.get('lyrics'))
        vbox.Add(self.lyric_label, 0, wx.EXPAND | wx.ALL, 5)
        self.lyric_display = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.lyric_display.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Status display
        self.status_label = wx.StaticText(panel, label=lang.get('status'))
        vbox.Add(self.status_label, 0, wx.EXPAND | wx.ALL, 5)
        self.status_display = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # Instructions
        self.instructions = wx.StaticText(panel, label=lang.get('controls'))

        # Layout
        vbox.Add(self.track_list, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.lyric_display, 2, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.status_display, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.instructions, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)

    def auto_select_default_midi(self):
        if not MIDI_AVAILABLE:
            return False
            
        try:
            ports = get_output_names()
            if ports:
                selected_port = None
                # Look for preferred Windows MIDI devices
                for candidate in ['Microsoft GS Wavetable Synth', 'Windows MIDI', 'MIDI Mapper', 'Wavetable']:
                    for port in ports:
                        if candidate.lower() in port.lower():
                            selected_port = port
                            break
                    if selected_port:
                        break
                
                # If no preferred device found, use the first available
                if not selected_port:
                    selected_port = ports[0]
                
                self.output_port = open_output(selected_port)
                self.output.speak(f"{lang.get('midi_device')} {selected_port}", interrupt=False)
                return True
        except Exception as e:
            pass
        return False

    def create_menu(self):
        menubar = wx.MenuBar()
        
        # File menu
        file_menu = wx.Menu()
        file_menu.Append(101, lang.get('open_midi'))
        file_menu.Append(102, lang.get('configure_tracks'))
        file_menu.Append(103, lang.get('clear'))
        file_menu.Append(104, lang.get('refresh'))
        file_menu.Append(105, lang.get('select_midi_device'))
        file_menu.AppendSeparator()
        file_menu.Append(106, lang.get('track_properties_menu'))
        file_menu.Append(107, lang.get('metronome_settings_menu'))
        file_menu.Append(108, lang.get('toggle_metronome'))
        file_menu.Append(109, lang.get('toggle_auto_announce'))
        file_menu.AppendSeparator()
        file_menu.Append(110, lang.get('quit'))
        menubar.Append(file_menu, lang.get('file_menu'))
        
        # Language menu
        language_menu = wx.Menu()
        language_menu.Append(201, lang.get('english'))
        language_menu.Append(202, lang.get('spanish'))
        menubar.Append(language_menu, lang.get('language_menu'))
        
        self.SetMenuBar(menubar)

        # Bind events
        self.Bind(wx.EVT_MENU, self.on_open, id=101)
        self.Bind(wx.EVT_MENU, self.on_configure_tracks, id=102)
        self.Bind(wx.EVT_MENU, self.on_clear, id=103)
        self.Bind(wx.EVT_MENU, self.on_refresh, id=104)
        self.Bind(wx.EVT_MENU, self.on_select_device, id=105)
        self.Bind(wx.EVT_MENU, self.on_track_properties, id=106)
        self.Bind(wx.EVT_MENU, self.on_metronome_settings, id=107)
        self.Bind(wx.EVT_MENU, self.on_toggle_metronome, id=108)
        self.Bind(wx.EVT_MENU, self.on_toggle_auto_announce, id=109)
        self.Bind(wx.EVT_MENU, self.on_quit, id=110)
        self.Bind(wx.EVT_MENU, self.on_language_english, id=201)
        self.Bind(wx.EVT_MENU, self.on_language_spanish, id=202)

    def on_key(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()
        alt = bool(modifiers & wx.MOD_ALT)
        ctrl = bool(modifiers & wx.MOD_CONTROL)

        if (alt and ctrl) or (alt and keycode == wx.WXK_F4):
            event.Skip()
            return

        if not self.notes or self.current_pair >= len(self.notes):
            event.Skip()
            return

        notes = self.notes[self.current_pair]
        if not notes:
            event.Skip()
            return

        if keycode == wx.WXK_SPACE and not alt and not ctrl:
            self.toggle_playback()
        elif keycode == wx.WXK_HOME and not alt and not ctrl:
            self.go_to_beginning()
        elif keycode == wx.WXK_END and not alt and not ctrl:
            self.go_to_end()
        elif keycode == wx.WXK_PAGEUP and not alt and not ctrl:
            self.jump_backward()
        elif keycode == wx.WXK_PAGEDOWN and not alt and not ctrl:
            self.jump_forward()
        elif keycode == wx.WXK_F4 and not alt and not ctrl:
            self.on_toggle_metronome(event)
        elif keycode == wx.WXK_F6 and not alt and not ctrl:
            self.on_toggle_auto_announce(event)
        elif alt and keycode == wx.WXK_RIGHT and not ctrl:
            self.navigate_next()
        elif alt and keycode == wx.WXK_LEFT and not ctrl:
            self.navigate_previous()
        else:
            event.Skip()

    def toggle_playback(self):
        if self.playing:
            self.playing = False
            self.output.speak(lang.get('paused'), interrupt=True)
        else:
            self.output.speak(lang.get('playing'), interrupt=True)
            self.play_current_track()

    def go_to_beginning(self):
        self.current_note_index = 0
        self.update_displays()
        self.output.speak(lang.get('beginning'), interrupt=True)

    def go_to_end(self):
        notes = self.notes[self.current_pair]
        self.current_note_index = len(notes) - 1
        self.update_displays()
        self.output.speak(lang.get('end'), interrupt=True)

    def jump_backward(self):
        self.current_note_index = max(0, self.current_note_index - 8)
        self.update_displays()
        self.output.speak(f"{lang.get('position')} {self.current_note_index + 1}", interrupt=True)

    def jump_forward(self):
        notes = self.notes[self.current_pair]
        self.current_note_index = min(len(notes) - 1, self.current_note_index + 8)
        self.update_displays()
        self.output.speak(f"{lang.get('position')} {self.current_note_index + 1}", interrupt=True)

    def navigate_next(self):
        notes = self.notes[self.current_pair]
        if self.current_note_index < len(notes) - 1:
            self.current_note_index += 1
            self.update_displays()
            self.play_current_note()
            self.announce_lyric_if_changed()

    def navigate_previous(self):
        if self.current_note_index > 0:
            self.current_note_index -= 1
            self.update_displays()
            self.play_current_note()
            self.announce_lyric_if_changed()

    def announce_lyric_if_changed(self):
        if self.auto_announce_lyrics and self.current_single_lyric:
            if self.current_single_lyric != self.last_announced_lyric and self.current_single_lyric != lang.get('no_lyrics_found'):
                self.output.speak(self.current_single_lyric, interrupt=True)
                self.last_announced_lyric = self.current_single_lyric

    def play_current_note(self):
        if not MIDI_AVAILABLE or not self.output_port:
            return
            
        notes = self.notes[self.current_pair]
        _, note, channel = notes[self.current_note_index] if len(notes[self.current_note_index]) == 3 else (notes[self.current_note_index][0], notes[self.current_note_index][1], 0)
        
        if self.current_pair in self.track_properties:
            channel = self.track_properties[self.current_pair]['channel']
        
        self.play_note(note, channel)

    def update_displays(self):
        self.update_lyric_display()
        self.update_status_display()

    # Language switching methods
    def on_language_english(self, event):
        lang.set_language('en')
        self.update_interface_language()
        
    def on_language_spanish(self, event):
        lang.set_language('es')
        self.update_interface_language()
        
    def update_interface_language(self):
        # Update window title
        self.SetTitle(lang.get('title'))
        
        # Update labels
        if self.track_label:
            self.track_label.SetLabel(lang.get('track_pairs'))
        if self.lyric_label:
            self.lyric_label.SetLabel(lang.get('lyrics'))
        if self.status_label:
            self.status_label.SetLabel(lang.get('status'))
        if self.instructions:
            self.instructions.SetLabel(lang.get('controls'))
        
        # Recreate menu with new language
        self.create_menu()
        
        # Update displays with new language
        self.update_displays()
        self.update_track_list()
        
        # Refresh the UI
        self.Refresh()

    # Menu handlers
    def on_open(self, event):
        dlg = wx.FileDialog(self, lang.get('open_midi_file'), wildcard=lang.get('midi_files'), style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.load_midi(dlg.GetPath())
        dlg.Destroy()

    def on_configure_tracks(self, event):
        if not self.midi_data:
            wx.MessageBox(lang.get('no_file_loaded'), lang.get('no_file_loaded_title'), wx.OK | wx.ICON_WARNING)
            return
            
        # Analyze tracks
        track_info = []
        for i, track in enumerate(self.midi_data.tracks):
            name = f"{lang.get('track')} {i + 1}"
            for msg in track:
                if msg.type == 'track_name':
                    name = f"{lang.get('track')} {i + 1}: {msg.name.strip()}"
                    break
            
            has_notes, has_lyrics = self.analyze_track_content(track)
            track_info.append((name, has_notes, has_lyrics))
        
        dlg = TrackPairingDialog(self, track_info)
        if dlg.ShowModal() == wx.ID_OK:
            self.track_pairs = dlg.get_track_pairs()
            self.process_tracks()
            self.update_track_list()
            
            if self.track_pairs:
                self.track_list.SetSelection(0)
                self.current_pair = 0
                self.current_note_index = 0
                self.last_announced_lyric = None
                self.update_displays()
                
                total_notes = sum(len(notes) for notes in self.notes)
                total_lyrics = sum(len(lyrics) for lyrics in self.timed_lyrics)
                self.output.speak(f"{lang.get('loaded_tracks')} {len(self.track_pairs)} pares, {total_notes} {lang.get('notes_word')}, {total_lyrics} {lang.get('lyrics_found')}", interrupt=True)
        dlg.Destroy()

    def on_clear(self, event):
        self.playing = False
        self.track_list.Clear()
        self.lyric_display.Clear()
        self.status_display.Clear()
        self.notes.clear()
        self.timed_lyrics.clear()
        self.track_properties.clear()
        self.track_pairs.clear()
        self.current_note_index = 0
        self.last_announced_lyric = None
        self.midi_data = None

    def on_refresh(self, event):
        if self.midi_data:
            # Re-analyze and show dialog again
            track_info = []
            for i, track in enumerate(self.midi_data.tracks):
                name = f"{lang.get('track')} {i + 1}"
                for msg in track:
                    if msg.type == 'track_name':
                        name = f"{lang.get('track')} {i + 1}: {msg.name.strip()}"
                        break
                
                has_notes, has_lyrics = self.analyze_track_content(track)
                track_info.append((name, has_notes, has_lyrics))
            
            dlg = TrackPairingDialog(self, track_info)
            if dlg.ShowModal() == wx.ID_OK:
                self.track_pairs = dlg.get_track_pairs()
                self.process_tracks()
                self.update_track_list()
                
                if self.track_pairs:
                    self.track_list.SetSelection(0)
                    self.current_pair = 0
                    self.current_note_index = 0
                    self.last_announced_lyric = None
                    self.update_displays()
            dlg.Destroy()

    def on_select_device(self, event):
        if not MIDI_AVAILABLE:
            wx.MessageBox(lang.get('midi_not_available'), lang.get('midi_not_available_title'), wx.OK | wx.ICON_WARNING)
            return
            
        try:
            ports = get_output_names()
            if not ports:
                wx.MessageBox(lang.get('no_midi_devices'), lang.get('no_midi_devices_title'), wx.OK | wx.ICON_WARNING)
                return
            
            dlg = wx.SingleChoiceDialog(self, lang.get('select_midi_device_prompt'), lang.get('select_midi_device_title'), ports)
            if dlg.ShowModal() == wx.ID_OK:
                selected = dlg.GetStringSelection()
                try:
                    if self.output_port:
                        self.output_port.close()
                    self.output_port = open_output(selected)
                except Exception as e:
                    wx.MessageBox(f"{lang.get('error_opening_device')}:\n{str(e)}", lang.get('error'), wx.OK | wx.ICON_ERROR)
            dlg.Destroy()
        except Exception as e:
            wx.MessageBox(f"{lang.get('error_accessing_midi')}:\n{str(e)}", lang.get('error'), wx.OK | wx.ICON_ERROR)

    def on_track_properties(self, event):
        if self.current_pair < len(self.track_pairs):
            props = self.track_properties.get(self.current_pair, {'channel': 1, 'instrument': 1, 'bank': 0, 'volume': 100})
            dlg = TrackPropertiesDialog(self, **props)
            if dlg.ShowModal() == wx.ID_OK:
                self.track_properties[self.current_pair] = dlg.get_values()
                self.apply_track_properties()
            dlg.Destroy()

    def on_metronome_settings(self, event):
        dlg = MetronomeDialog(self, self.tempo, self.downbeat_note, self.upbeat_note, self.metronome_enabled)
        if dlg.ShowModal() == wx.ID_OK:
            values = dlg.get_values()
            self.tempo = values['tempo']
            self.downbeat_note = values['downbeat_note']
            self.upbeat_note = values['upbeat_note']
            self.metronome_enabled = values['enabled']
        dlg.Destroy()

    def on_toggle_metronome(self, event):
        self.metronome_enabled = not self.metronome_enabled
        status = lang.get('metronome_on') if self.metronome_enabled else lang.get('metronome_off')
        self.output.speak(status, interrupt=True)
        self.update_status_display()

    def on_toggle_auto_announce(self, event):
        self.auto_announce_lyrics = not self.auto_announce_lyrics
        status = lang.get('auto_announce_on') if self.auto_announce_lyrics else lang.get('auto_announce_off')
        self.output.speak(status, interrupt=True)
        self.update_status_display()

    def on_track_select(self, event):
        self.current_pair = event.GetSelection()
        self.current_note_index = 0
        self.last_announced_lyric = None
        self.update_displays()
        self.apply_track_properties()

    def on_quit(self, event):
        self.Close()

    def on_close(self, event):
        self.playing = False
        if self.output_port:
            self.output_port.close()
        self.Destroy()

    # Core functionality
    def load_midi(self, path):
        try:
            # Load MIDI data completely into RAM
            self.midi_data = copy.deepcopy(MidiFile(path))
            
            # Analyze tracks
            track_info = []
            for i, track in enumerate(self.midi_data.tracks):
                name = f"{lang.get('track')} {i + 1}"
                for msg in track:
                    if msg.type == 'track_name':
                        name = f"{lang.get('track')} {i + 1}: {msg.name.strip()}"
                        break
                
                has_notes, has_lyrics = self.analyze_track_content(track)
                track_info.append((name, has_notes, has_lyrics))
            
            # Always show the track pairing dialog
            dlg = TrackPairingDialog(self, track_info)
            if dlg.ShowModal() == wx.ID_OK:
                self.track_pairs = dlg.get_track_pairs()
                self.process_tracks()
                self.update_track_list()
                
                total_notes = sum(len(notes) for notes in self.notes)
                total_lyrics = sum(len(lyrics) for lyrics in self.timed_lyrics)
                self.output.speak(f"{lang.get('loaded_tracks')} {len(self.track_pairs)} pares, {total_notes} {lang.get('notes_word')}, {total_lyrics} {lang.get('lyrics_found')}", interrupt=True)
                
                if self.track_pairs:
                    self.track_list.SetSelection(0)
                    self.current_pair = 0
                    self.current_note_index = 0
                    self.last_announced_lyric = None
                    self.update_displays()
                    
                # Auto-select MIDI device after successful load
                wx.CallAfter(self.ensure_midi_auto_select)
            else:
                # User cancelled, clear data
                self.midi_data = None
            dlg.Destroy()
                
        except Exception as e:
            wx.MessageBox(f"{lang.get('error_loading_midi')}: {e}", lang.get('error'), wx.OK | wx.ICON_ERROR)

    def ensure_midi_auto_select(self):
        """Ensure MIDI device is selected after loading a file"""
        if not self.output_port and MIDI_AVAILABLE:
            if not self.auto_select_default_midi():
                # No device could be auto-selected
                wx.MessageBox(
                    lang.get('no_midi_devices'),
                    lang.get('no_midi_devices_title'),
                    wx.OK | wx.ICON_INFORMATION
                )

    def analyze_track_content(self, track):
        has_notes = False
        has_lyrics = False
        
        for msg in track:
            # Check for notes
            if msg.type == 'note_on' and msg.velocity > 0:
                has_notes = True
                
            # Check for lyrics - be very broad in detection
            elif (msg.type in ['lyrics', 'text', 'marker', 'cue_marker'] or 
                  hasattr(msg, 'text') or 
                  hasattr(msg, 'data')):
                
                text_content = ""
                if hasattr(msg, 'text') and msg.text:
                    text_content = str(msg.text).strip()
                elif hasattr(msg, 'data') and msg.data:
                    try:
                        if isinstance(msg.data, bytes):
                            text_content = msg.data.decode('utf-8', errors='ignore').strip()
                        else:
                            text_content = str(msg.data).strip()
                    except:
                        pass
                
                if text_content and len(text_content) > 0:
                    has_lyrics = True
        
        return has_notes, has_lyrics

    def process_tracks(self):
        self.notes.clear()
        self.timed_lyrics.clear()
        
        for notes_track_idx, lyrics_track_idx in self.track_pairs:
            # Process notes track
            if notes_track_idx < len(self.midi_data.tracks):
                track_notes = self.extract_notes_from_track(self.midi_data.tracks[notes_track_idx])
                self.notes.append(track_notes)
            else:
                self.notes.append([])
            
            # Process lyrics track
            if lyrics_track_idx is not None and lyrics_track_idx < len(self.midi_data.tracks):
                track_lyrics = self.extract_lyrics_from_track(self.midi_data.tracks[lyrics_track_idx])
                self.timed_lyrics.append(track_lyrics)
            else:
                self.timed_lyrics.append([])

    def extract_notes_from_track(self, track):
        abs_time = 0
        track_notes = []
        
        for msg in track:
            abs_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                track_notes.append((abs_time, msg.note, getattr(msg, 'channel', 0)))
        
        return track_notes

    def extract_lyrics_from_track(self, track):
        abs_time = 0
        track_lyrics = []
        
        for msg in track:
            abs_time += msg.time
            
            # Check for standard lyric types
            if msg.type in ['lyrics', 'text', 'marker', 'cue_marker']:
                if hasattr(msg, 'text'):
                    lyric_text = msg.text.strip() if msg.text else ""
                    if lyric_text and lyric_text not in ['/', '\\', '-', '']:
                        track_lyrics.append((abs_time, lyric_text))
                        
            # Check for any message with text attribute
            elif hasattr(msg, 'text') and msg.text:
                lyric_text = msg.text.strip()
                if lyric_text and lyric_text not in ['/', '\\', '-', '']:
                    track_lyrics.append((abs_time, lyric_text))
                    
            # Check for data attribute (some MIDI files store lyrics differently)
            elif hasattr(msg, 'data'):
                try:
                    if isinstance(msg.data, bytes):
                        lyric_text = msg.data.decode('utf-8', errors='ignore').strip()
                    else:
                        lyric_text = str(msg.data).strip()
                    if lyric_text and lyric_text not in ['/', '\\', '-', '']:
                        track_lyrics.append((abs_time, lyric_text))
                except:
                    pass
        
        return track_lyrics

    def update_track_list(self):
        track_names = []
        for i, (notes_track_idx, lyrics_track_idx) in enumerate(self.track_pairs):
            lyrics_name = f"{lyrics_track_idx + 1}" if lyrics_track_idx is not None else lang.get('none')
            track_names.append(f"{lang.get('pair_prefix')} {i + 1}: {lang.get('notes_prefix')} {notes_track_idx + 1}, {lang.get('lyrics_prefix')} {lyrics_name}")
        
        self.track_list.Set(track_names)

    def update_lyric_display(self):
        if not self.notes or self.current_pair >= len(self.notes):
            self.lyric_display.SetValue(lang.get('no_track_pair'))
            return False
            
        notes = self.notes[self.current_pair]
        lyrics = self.get_current_lyrics()
        
        if not notes:
            current_lyric = " ".join([lyric[1] for lyric in lyrics]) if lyrics else lang.get('no_notes_track')
            self.current_single_lyric = None
            self.lyric_display.SetValue(current_lyric)
            return False
        
        if not lyrics:
            self.lyric_display.SetValue(lang.get('no_lyrics_found'))
            self.current_single_lyric = None
            return False
        
        # Display all lyrics
        current_lyric = " ".join([lyric[1] for lyric in lyrics])
        self.lyric_display.SetValue(current_lyric)
        
        # Find current lyric based on note timing
        current_note_time = notes[self.current_note_index][0]
        current_position = -1
        
        for i, (lyric_time, lyric_text) in enumerate(lyrics):
            if lyric_time <= current_note_time:
                current_position = i
            else:
                break
        
        if current_position >= 0:
            self.current_single_lyric = lyrics[current_position][1]
            # Highlight current lyric
            try:
                start_pos = sum(len(lyrics[i][1]) + 1 for i in range(current_position))
                end_pos = start_pos + len(lyrics[current_position][1])
                self.lyric_display.SetSelection(start_pos, end_pos)
                self.lyric_display.ShowPosition(start_pos)
            except:
                pass  # If highlighting fails, continue without it
            return True
        else:
            # No lyric yet, find the most recent one
            if lyrics:
                recent_lyrics = [lyric for lyric in lyrics if lyric[0] <= current_note_time]
                if recent_lyrics:
                    self.current_single_lyric = recent_lyrics[-1][1]
                else:
                    self.current_single_lyric = lyrics[0][1]  # Use first lyric if none match
            else:
                self.current_single_lyric = None
        
        return False

    def get_current_lyrics(self):
        if self.current_pair >= len(self.timed_lyrics):
            return []
        return self.timed_lyrics[self.current_pair]

    def update_status_display(self):
        if not self.notes or self.current_pair >= len(self.notes):
            self.status_display.SetValue(lang.get('no_track_pair'))
            return
            
        notes = self.notes[self.current_pair]
        lyrics = self.get_current_lyrics()
        
        if not notes:
            self.status_display.SetValue(lang.get('no_notes_pair'))
            return
        
        status_text = f"{lang.get('note')} {self.current_note_index + 1}/{len(notes)}\n"
        status_text += f"{lang.get('pair_prefix')} {self.current_pair + 1}/{len(self.track_pairs)}\n"
        
        # Show track pair info
        if self.current_pair < len(self.track_pairs):
            notes_track, lyrics_track = self.track_pairs[self.current_pair]
            status_text += f"{lang.get('notes')}: {lang.get('track')} {notes_track + 1}\n"
            status_text += f"{lang.get('lyrics')}: {lang.get('track')} {lyrics_track + 1 if lyrics_track is not None else lang.get('none')}\n"
        
        status_text += f"{lang.get('lyrics_in_pair')} {len(lyrics)}\n"
        status_text += f"{lang.get('midi_status')} {lang.get('yes') if MIDI_AVAILABLE and self.output_port else lang.get('no')}\n"
        status_text += f"{lang.get('metronome')}: {lang.get('on') if self.metronome_enabled else lang.get('off')}\n"
        status_text += f"{lang.get('auto_announce')}: {lang.get('on') if self.auto_announce_lyrics else lang.get('off')}"
        
        self.status_display.SetValue(status_text)

    def apply_track_properties(self):
        if MIDI_AVAILABLE and self.output_port and self.current_pair in self.track_properties:
            props = self.track_properties[self.current_pair]
            try:
                self.output_port.send(Message('program_change', channel=props['channel'], program=props['instrument']))
                self.output_port.send(Message('control_change', channel=props['channel'], control=7, value=props['volume']))
                if props['bank'] > 0:
                    self.output_port.send(Message('control_change', channel=props['channel'], control=0, value=props['bank']))
            except:
                pass

    def play_note(self, note, channel=0):
        if MIDI_AVAILABLE and self.output_port:
            try:
            # Send all notes off first to stop any previous notes
                self.output_port.send(Message('control_change', channel=channel, control=123, value=0))
            # Play the note
                self.output_port.send(Message('note_on', note=note, velocity=100, channel=channel))
            # For single note preview, still use the short duration
                time.sleep(0.1)
                self.output_port.send(Message('note_off', note=note, velocity=100, channel=channel))
            except:
                pass    
    def play_metronome_beat(self, is_downbeat=True):
        if MIDI_AVAILABLE and self.output_port and self.metronome_enabled:
            try:
                note = self.downbeat_note if is_downbeat else self.upbeat_note
                self.output_port.send(Message('note_on', note=note, velocity=127, channel=9))
                time.sleep(0.1)
                self.output_port.send(Message('note_off', note=note, velocity=127, channel=9))
            except:
                pass
    
    def start_metronome(self, tempo, time_sig_num=4, start_time=None):
        """Start synchronized metronome thread"""
        def _metronome():
            beat_interval = 60.0 / tempo  # Seconds per beat
            
            # Wait for start_time if provided
            if start_time:
                while time.time() < start_time and self.playing:
                    time.sleep(0.01)
            
            metronome_start = start_time if start_time else time.time()
            beat_count = 0
            
            while self.playing and self.metronome_enabled:
                current_time = time.time()
                elapsed_time = current_time - metronome_start
                expected_beat_time = beat_count * beat_interval
                
                # If we're ahead of schedule, wait
                if elapsed_time < expected_beat_time:
                    sleep_time = expected_beat_time - elapsed_time
                    while sleep_time > 0 and self.playing and self.metronome_enabled:
                        chunk = min(sleep_time, 0.01)  # Check every 10ms
                        time.sleep(chunk)
                        sleep_time -= chunk
                        current_time = time.time()
                        elapsed_time = current_time - metronome_start
                
                # Play the beat if we're still playing
                if self.playing and self.metronome_enabled:
                    is_downbeat = (beat_count % time_sig_num == 0)
                    self.play_metronome_beat(is_downbeat)
                    beat_count += 1
        
        if self.metronome_enabled:
            self.metronome_thread = threading.Thread(target=_metronome, daemon=True)
            self.metronome_thread.start()

    def get_time_signature_and_tempo(self):
        """Extract time signature and tempo changes from MIDI file"""
        time_signatures = []
        tempo_changes = []
        
        for track in self.midi_data.tracks:
            accumulated_time = 0
            for msg in track:
                accumulated_time += msg.time
                
                if msg.type == 'time_signature':
                    # MIDI time signature: numerator/denominator, clocks_per_click, notated_32nd_notes_per_beat
                    time_signatures.append((accumulated_time, msg.numerator, msg.denominator))
                
                elif msg.type == 'set_tempo':
                    # Convert microseconds per beat to BPM
                    bpm = 60000000 / msg.tempo
                    tempo_changes.append((accumulated_time, bpm))
        
        # Set defaults if not found
        if not time_signatures:
            time_signatures = [(0, 4, 4)]  # Default 4/4 time
        if not tempo_changes:
            tempo_changes = [(0, 120)]  # Default 120 BPM
            
        return time_signatures, tempo_changes

    def get_current_time_signature(self, current_tick, time_signatures):
        """Get the current time signature based on current position"""
        current_sig = (4, 4)  # Default
        for tick, numerator, denominator in time_signatures:
            if tick <= current_tick:
                current_sig = (numerator, denominator)
            else:
                break
        return current_sig

    def get_current_tempo(self, current_tick, tempo_changes):
        """Get the current tempo based on current position"""
        current_tempo = 120  # Default
        for tick, bpm in tempo_changes:
            if tick <= current_tick:
                current_tempo = bpm
            else:
                break
        return current_tempo

    def play_current_track(self):
        def _play():
            self.playing = True
            
            if not self.midi_data or self.current_pair >= len(self.track_pairs):
                self.playing = False
                return
            
            notes_track_idx, _ = self.track_pairs[self.current_pair]
            if notes_track_idx >= len(self.midi_data.tracks):
                self.playing = False
                return
            
            track = self.midi_data.tracks[notes_track_idx]
            
            # Get time signatures and tempo changes from the file
            time_signatures, tempo_changes = self.get_time_signature_and_tempo()
            
            # Get current position in the track
            current_tick = 0
            if self.current_note_index > 0 and self.current_note_index < len(self.notes[self.current_pair]):
                current_tick = self.notes[self.current_pair][self.current_note_index][0]
            
            # Find where we are in the actual MIDI track
            accumulated_time = 0
            start_message_index = 0
            
            for i, msg in enumerate(track):
                accumulated_time += msg.time
                if accumulated_time >= current_tick:
                    start_message_index = i
                    break
            
            # Get initial tempo and time signature for metronome
            current_tempo = self.get_current_tempo(accumulated_time, tempo_changes)
            time_sig_num, time_sig_den = self.get_current_time_signature(accumulated_time, time_signatures)
            
            # Calculate synchronized start time (both threads start at same moment)
            playback_start_time = time.time() + 0.1  # Small delay to ensure both threads sync
            
            # Start synchronized metronome
            self.start_metronome(current_tempo, time_sig_num, playback_start_time)
            
            # Wait until synchronized start time
            while time.time() < playback_start_time and self.playing:
                time.sleep(0.01)
            
            # Play from current position
            accumulated_time = 0
            for i, msg in enumerate(track):
                if i < start_message_index:
                    accumulated_time += msg.time
                    continue
                    
                if not self.playing:
                    break
                
                # Get current tempo for MIDI playback timing
                current_tempo = self.get_current_tempo(accumulated_time, tempo_changes)
                
                # Sleep for the message timing
                if msg.time > 0:
                    sleep_time = (msg.time / self.midi_data.ticks_per_beat) * (60.0 / current_tempo)
                    
                    # Only break into chunks if sleep time is significant (>100ms)
                    if sleep_time > 0.1:
                        while sleep_time > 0 and self.playing:
                            chunk = min(sleep_time, 0.05)  # 50ms chunks
                            time.sleep(chunk)
                            sleep_time -= chunk
                    else:
                        time.sleep(sleep_time)
                
                if not self.playing:
                    break
                
                accumulated_time += msg.time
                
                # Send the MIDI message
                if MIDI_AVAILABLE and self.output_port:
                    try:
                        # Apply track properties if available
                        if msg.type in ['note_on', 'note_off', 'program_change', 'control_change']:
                            # Create a copy of the message with potentially modified channel
                            msg_dict = msg.dict()
                            if self.current_pair in self.track_properties:
                                if 'channel' in msg_dict:
                                    msg_dict['channel'] = self.track_properties[self.current_pair]['channel']
                            
                            modified_msg = Message(**msg_dict)
                            self.output_port.send(modified_msg)
                        else:
                            # Send other messages as-is
                            self.output_port.send(msg)
                            
                    except Exception as e:
                        pass  # Continue playing even if individual messages fail
                
                # Update UI position for note_on messages
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Find corresponding note index
                    for note_idx, (note_time, note, channel) in enumerate(self.notes[self.current_pair]):
                        if abs(note_time - accumulated_time) < self.midi_data.ticks_per_beat / 4:  # Within quarter beat
                            self.current_note_index = note_idx
                            if note_idx % 5 == 0:  # Update UI every 5 notes
                                wx.CallAfter(self.update_displays)
                                wx.CallAfter(self.announce_lyric_if_changed)
                            break
            
            # Clean up - send all notes off
            if MIDI_AVAILABLE and self.output_port:
                try:
                    for ch in range(16):
                        self.output_port.send(Message('control_change', channel=ch, control=123, value=0))
                except:
                    pass
            
            wx.CallAfter(self.update_displays)
            self.playing = False

        self.play_thread = threading.Thread(target=_play, daemon=True)
        self.play_thread.start()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MidiLyricChecker()
    frame.Show()
    app.MainLoop()