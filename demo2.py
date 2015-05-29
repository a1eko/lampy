#!/usr/bin/python

from apps import App
import physics
import scene

app = App("demo2", scene.PoolBottom(level=-1.0), physics.FrozenLamprey())
app.run()
