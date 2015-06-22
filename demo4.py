#!/usr/bin/python

from apps import App
import physics
import scene

#app = App("demo", scene.Underwater(), physics.DrivenLamprey())
app = App("demo", physics=physics.DrivenLamprey())
app.run()
