#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess
from mididings import *
from mididings.extra import *
from mididings.engine import *
from mididings.event import *

config(

    client_name = 'Master',

    out_ports = [ 
        ('Q49', '20:0','.*SD-90 Part A'),
        ('PK5', '20:0','.*SD-90 Part A'), ],

    in_ports = [ 
        ('SD90 - MIDI IN 1', '20:2','.*SD-90 MIDI 1'),
        ('SD90 - MIDI IN 2', '20:3','.*SD-90 MIDI 2') ],

    initial_scene = 1,
)

#--------------------------------------------------------------------
# Test
def Chord(ev, trigger_notes=(41, 43), chord_offsets=(0, 4, 7)):
    if ev.type in (NOTEON, NOTEOFF):
        if ev.data1 in trigger_notes:
            evcls = NoteOnEvent if ev.type == NOTEON else NoteOffEvent
            return [evcls(ev.port, ev.channel, ev.note + i, ev.velocity)
                    for i in chord_offsets]
    return ev
#--------------------------------------------------------------------

# For SD-90 only
def SendSysex(ev):
    return SysExEvent(ev.port, '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')
#--------------------------------------------------------------------

# Scene navigation
def NavigateToScene(ev):
    nb_scenes = len(scenes())    
    if ev.ctrl == 20:
        cs=current_scene()
        if ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs+1)
        elif ev.value == 1:
            if cs > 1:
                switch_scene(cs-1)
        elif ev.value == 3:
            #TODO - wrap subscene
            css=current_subscene()
            switch_subscene(css+1)
    elif ev.ctrl == 22:
        subprocess.Popen(['/bin/bash', './kill.sh'])

# Pre/Post
_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')
#--------------------------------------------------------------------

# Controller pour le changement de scene
_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter([20,22]) >> Process(NavigateToScene)
#--------------------------------------------------------------------

# Channel filter base for patche
cf=ChannelFilter(channels=[1,2])
#--------------------------------------------------------------------

# Shortcut
play = Filter(CTRL) >> CtrlFilter(21)
#reset = Filter(CTRL) >> CtrlFilter(22) >> Panic()
#--------------------------------------------------------------------

# FX Section
explosion = Velocity(fixed=80) >> Output('PK5', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth = Velocity(fixed=80) >> Output('PK5', channel=1, program=((99*128),82), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Syhth. generique pour lowbase
lowsynth = cf >> Velocity(fixed=100) >> Output('PK5', channel=1, program=51, volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch pour Closer to the hearth 
closer_high = Output('Q49', 1, program=((99*128),15), volume=100)
closer_base = Output('PK5', 2, program=((99*128),51), volume=100)
closer_main = cf >> KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch pour Time Stand Still
tss_high = Velocity(fixed=90) >> Output('Q49', channel=1, program=((99*128),92), volume=100)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('Q49', channel=1, program=((99*128),92), volume=100)
tss_keyboard_main = cf >> KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=75)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=75)
tss_foot_main = cf >> KeySplit('d#3', tss_foot_left, tss_foot_right)
#--------------------------------------------------------------------

# Patch pour Analog Kid
analogkid=cf >> Transpose(-24) >> Harmonize('c', 'major', ['unison', 'third', 'fifth', 'octave']) >> Output('PK5', channel=1, program=((99*128),50), volume=100)
#--------------------------------------------------------------------

# Patch debug
#debug = (ChannelFilter(1) >> Output('PK5', channel=1, program=((99*128), 1), volume=100)) // (ChannelFilter(2) >> Output('Q49', channel=3, program=((99*128), 10), volume=101))
#piano=Harmonize('c', 'major', ['unison','octave']) >> Output('Q49', channel=1, program=((99*128),1), volume=100)
piano= Output('Q49', channel=1, program=((99*128),1), volume=100)
#--------------------------------------------------------------------

# Liste des scenes
init=Filter(NOTE) >> Filter(NOTEON) >> Process(SendSysex)
_scenes = {
    1: Scene("Initialize",  init),
    2: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> keysynth),
    3: Scene("FreeWill", Transpose(12) >> LatchNotes(False,reset='E4') >> keysynth),
    4: Scene("CloserToTheHeart", [ChannelFilter(1) >> closer_main, ChannelFilter(2) >> Transpose(-24) >> closer_base]),
    5: SceneGroup("The Trees", [
           Scene("Bridge",  play >> System("mpg123 -q /mnt/flash/rush/trees_full.mp3")),
           Scene("Synth", Transpose(-29) >> LatchNotes(False,reset='G0') >> lowsynth),
       ]),
    6: Scene("Time Stand Still", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
    7: SceneGroup("2112", [
           Scene("Intro", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/rush/2112.mp3")),
           Scene("Explosion", explosion),
       ]),
    8: Scene("AnalogKid", analogkid),
    9: SceneGroup("Bass cover", [
           Scene("Toto - Rossana", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/toto_rossana_no_bass.mp3")),
           Scene("Toto - Africa", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/toto_africa_no_bass.mp3")),
           Scene("Yes - Owner of a lonely heart", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/yes_owner_lonely_heart.mp3")),
           Scene("Queen - I want to break free", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_want_break_free.mp3")),
           Scene("Queen - Under Pressure", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_under_pressure.mp3")),
           Scene("Queen - Crazy little thing called love", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_crazy_little_thing_called_love.mp3")),
           Scene("Queen - Another one bites the dust", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_another_on_bites_dust.mp3")),
           Scene("ZZ Top - Sharp dressed man", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/zz_top_sharp_dressed_man.mp3")),
           Scene("Tears for fears - Head over heels", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/t4f_head_over_heels.mp3")),
           Scene("Tears for fears - Everybody wants to rule the world", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/t4f_everybody.mp3")),
           Scene("Police - Walking on the moon", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/police_walking_moon.mp3")),
           Scene("Police - Message in a bottle", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/police_message_bottle.mp3")),
           Scene("Led Zeppelin - Rock and roll", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/led_zeppelin_rock_and_roll.mp3")),
           Scene("Bon Jovi - Livin on a prayer", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/bon_jovi_prayer.mp3")),
       ])
}

# ---------------------------
run(
    control=_control,
    pre=_pre, 
    #post=_post,
    scenes=_scenes, 
)
# ---------------------------
