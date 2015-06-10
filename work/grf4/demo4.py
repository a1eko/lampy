#!/usr/bin/python

from apps import App
import physics
import scene

#app = App("demo", scene.PoolBottom(), physics.DrivenLamprey())
app = App("demo", scene.Underwater(), physics.DrivenLamprey())
app.run()
