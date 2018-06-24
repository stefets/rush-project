    2: SceneGroup("Rush cover", [    
            Scene("Mission", play >> System(play_file("mission.mp3"))),
            Scene("Limelight", play >> System(play_file("limelight.mp3"))),
            Scene("RedBarchetta ", play >> System(play_file("barchetta.mp3"))),
            Scene("FlyByNight ", play >> System(play_file("fly_by_night.mp3"))),
            Scene("Spirit of Radio ", play >> System(play_file("spirit_of_radio.mp3"))),
            Scene("AnalogKid", play >> System(play_file("analogkid.mp3"))),
            Scene("Analog Kid Keyboard", analogkid_main),
            #Scene("Analog Kid Keyboard", [ChannelFilter(2) >> analogkid_main, ChannelFilter(1) >> analogkid_ending ]),
            Scene("TimeStandSteel", play >> System(play_file("time_stand_steel.mp3"))),
            Scene("Time Stand Still Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
            Scene("KidGloves ", play >> System(play_file("kid_gloves.mp3"))),
            Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
            Scene("Freewill ", play >> System(play_file("freewill.mp3"))),
            Scene("FreeWill Keyboard", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
	    	Scene("Territories", play >> System(play_file("territories.mid"))),
	    	Scene("Mission", play >> System(play_file("mission.mid"))),
       ]),
