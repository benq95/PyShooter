 
from math import pi, sin, cos
import sys,os

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import Vec3
from panda3d.core import Filename

from panda3d.core import TextNode
from cameraController import CameraController
from panda3d.core import TransparencyAttrib
from panda3d.bullet import BulletWorld,  BulletBoxShape, BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode

from panda3d.core import ClockObject
from random import randint

from direct.interval.LerpInterval import  LerpHprInterval

from panda3d.core import Material

from target import Target


class MyApp(ShowBase):
    targets = []

    def __init__(self):
        ShowBase.__init__(self)
        # Disable the camera trackball controls.
        #self.disableMouse()
        mydir = os.path.abspath(sys.path[0])

        # Convert that to panda's unix-style notation.
        mydir = Filename.fromOsSpecific(mydir).getFullpath()
        self.model = self.loader.loadModel(mydir + "/models/M4a1.egg")
        self.model.reparentTo(self.cam)
        self.model.setPos(1,4,-1)
        self.model.setScale(0.4, 0.4, 0.4)
        self.model.setColor(0.1,0.1,0.1,1)
        self.model.setH(self.model,180)
        self.points = 0

        self.clock = ClockObject(0)

        #target.setHpr(targetParent,Vec3(0,-90,0))

        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(50,10,0)
        sciana1.setScale(20)
        sciana1.setHpr(90,0,0)
        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(50, -30, 0)
        sciana1.setScale(20)
        sciana1.setHpr(90, 0, 0)

        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(10, 50, 0)
        sciana1.setScale(20)
        sciana1.setHpr(0, 0, 0)
        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(-30, 50, 0)
        sciana1.setScale(20)
        sciana1.setHpr(0, 0, 0)

        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(10, -20, 0)
        sciana1.setScale(20)
        sciana1.setHpr(0, 0, 0)
        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(-30, -20, 0)
        sciana1.setScale(20)
        sciana1.setHpr(0, 0, 0)

        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(-50, 30, 0)
        sciana1.setScale(20)
        sciana1.setHpr(-90, 0, 0)
        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(self.render)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(-50, -50, 0)
        sciana1.setScale(20)
        sciana1.setHpr(-90, 0, 0)

        sciana1 = self.loader.loadModel(mydir + "/models/Project.egg")
        sciana1.reparentTo(self.render)
        #sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(0, 50, -10)
        sciana1.setScale(20)
        sciana1.setHpr(0, 90, 0)

        sciana1 = self.loader.loadModel(mydir + "/models/Project.egg")
        sciana1.reparentTo(self.render)
        # sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/wall.jpg'))
        sciana1.setPos(0, 50, 30)
        sciana1.setScale(20)
        sciana1.setHpr(0, 90, 0)


        imageObject = OnscreenImage(image=mydir + "/models/tex/target.png", pos=(0, 0, 0.02), scale=0.1)
        imageObject.setTransparency(TransparencyAttrib.MAlpha)

        self.taskMgr.add(self.update, "update")

        self.bk_text = "This is my Demo"
        self.textObject = OnscreenText(text = self.bk_text, pos = (0.95,-0.95),
        scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=1)

        # debugNode = BulletDebugNode('Debug')
        # debugNode.showWireframe(True)
        # debugNode.showConstraints(True)
        # debugNode.showBoundingBoxes(False)
        # debugNode.showNormals(False)
        # debugNP = self.render.attachNewNode(debugNode)
        # debugNP.show()

        self.world = BulletWorld()
        # self.world.setDebugNode(debugNP.node())

        # init targets
        # lvl 1
        self.lvl1Targets = []
        target = Target(self.render,self.world,self.loader,(13,11,-3), 1, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl1Targets.append(target)
        target = Target(self.render, self.world, self.loader, (-13, 11, -3), 1, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl1Targets.append(target)
        target = Target(self.render, self.world, self.loader, (13, -11, -3), 1, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl1Targets.append(target)

        self.activate(1)

        self.lvl2Targets = []
        target = Target(self.render, self.world, self.loader, (0, 22, -3), 2, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl2Targets.append(target)
        target = Target(self.render, self.world, self.loader, (-24, 11, -3), 2, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl2Targets.append(target)
        target = Target(self.render, self.world, self.loader, (24, -11, -3), 2, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl2Targets.append(target)

        self.activate(2)

        self.lvl3Targets = []
        target = Target(self.render, self.world, self.loader, (10, 43, -3), 3, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl3Targets.append(target)
        target = Target(self.render, self.world, self.loader, (-35, 8, -3), 3, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl3Targets.append(target)
        target = Target(self.render, self.world, self.loader, (35, -8, -3), 3, self.addPoints, False)
        MyApp.targets.append(target)
        self.lvl3Targets.append(target)

        self.activate(3)

        self.mouseLook = CameraController(self, self.cam, self.render, self.model)
        self.mouseLook.start()
        self.accept("tab", self.mouseLook.start)
        self.accept("escape", self.mouseLook.stop)

    def activate(self, lvl):
        if lvl == 1:
            lvlTab = self.lvl1Targets
        if lvl == 2:
            lvlTab = self.lvl2Targets
        if lvl == 3:
            lvlTab = self.lvl3Targets

        while True:
            r = randint(0, 2)
            if not lvlTab[r].active:
                lvlTab[r].activate()
                break

    def update(self, task):
        self.bk_text = str(int(self.clock.getRealTime()))
        self.textObject.setText("Time: " + self.bk_text + " Points " + str(self.points))

        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont

    def addPoints(self, p):
        self.points += p
        self.activate(p)

    def processNode(self, node):
        if node is not None:
            print(node.getName())
            for n in MyApp.targets:
                if n.name == node.getName():
                    n.onHit()
                    break

    def reset(self):
        for t in MyApp.targets:
            t.deactivate()

        self.activate(1)
        self.activate(2)
        self.activate(3)

        self.points = 0;
        self.clock.reset()

app = MyApp()
app.run() 
