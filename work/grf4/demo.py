#!/usr/bin/python

from apps import App
import physics
import scene

app = App("demo", scene.Demo(), physics.Demo())
app.run()
