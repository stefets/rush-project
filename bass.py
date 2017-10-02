#-----------------------------------------------------------------------------------------------------------
# SCENES SECTION
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Reset",  reset),
    2: SceneGroup("Bass cover", [
            Scene("Toto - Rossana", play >> System(player + "toto_rossana_no_bass.mp3")),
            Scene("Toto - Africa", play >> System(player + "toto_africa_no_bass.mp3")),
            Scene("Yes - Owner of a lonely heart", play >> System(player + "yes_owner_lonely_heart.mp3")),
            Scene("Queen - I want to break free", play >> System(player + "queen_want_break_free.mp3")),
            Scene("Queen - Under Pressure", play >> System(player + "queen_under_pressure.mp3")),
            Scene("Queen - Crazy little thing called love", play >> System(player + "queen_crazy_little_thing_called_love.mp3")),
            Scene("Queen - Another one bites the dust", play >> System(player + "queen_another_on_bites_dust.mp3")),
            Scene("ZZ Top - Sharp dressed man", play >> System(player + "zz_top_sharp_dressed_man.mp3")),
            Scene("T4F - Head over heels", play >> System(player + "t4f_head_over_heels.mp3")),
            Scene("T4F - Head over heels - Synth", Transpose(-12) >> LatchNotes(False,reset='E2') >> lowsynth2),
            Scene("Tears for fears - Everybody wants to rule the world", play >> System(player + "t4f_everybody.mp3")),
            Scene("Police - Walking on the moon", play >> System(player + "police_walking_moon.mp3")),
            Scene("Police - Message in a bottle", play >> System(player + "police_message_bottle.mp3")),
            Scene("Led Zeppelin - Rock and roll", play >> System(player + "led_zeppelin_rock_and_roll.mp3")),
            Scene("Bon Jovi - Livin on a prayer", play >> System(player + "bon_jovi_prayer.mp3")),
            Scene("Pat Metheny - Letter from home", play >> System(player + "letter_from_home.mp3")),
            Scene("Muse - Uprising", play >> System(player + "uprising.mp3")),
       ]),
}
