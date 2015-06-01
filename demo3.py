#!/usr/bin/python

from apps import App
import physics
import scene

app = App("demo", scene.PoolBottom(), physics.DrivenLamprey())
app.run()
