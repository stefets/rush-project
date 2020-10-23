    2: SceneGroup("Big Country", [
            Scene("Test", init_patch=P14A, patch=violon),
            Scene("In a Big Country", init_patch=P14A, patch=big_country_pipe),
        ]),
    3: SceneGroup("Compositions", [
            Scene("Centurion - no guitar, no synth", play >> System(play_file("centurion.mp3"))),
            Scene("Centurion - Synth", centurion_patch),
            Scene("Cool Boy - no guitar, no synth", play >> System(play_file("cool_boy.mp3"))),
            #Scene("Cool Boy - Synth", analogkid),
            #Scene("Centurion - Patch et Video", centurion_patch, [centurion_video]),
            Scene("Shadow - no bass", play >> System(play_file("shadow.mp3"))),
            Scene("Voleur - no guitar", play >> System(play_file("voleur.mp3"))),
        ]),
    4: SceneGroup("Super60", [
            Scene("S60A", init_patch=S60A, patch=piano),
            Scene("S60B", init_patch=S60B, patch=piano),
            Scene("S60C", init_patch=S60C, patch=piano),
            Scene("S60D", init_patch=S60D, patch=piano),
        ]),
