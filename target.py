import os
import sys

from direct.interval.LerpInterval import LerpHprInterval, Point3
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import Filename, Vec3, BitMask32


class Target:

    def __init__(self, render, bulletWorld, loader,pos, hitPoints, addPoints, active):
        self.pos = pos
        self.render = render
        self.bulletWorld = bulletWorld
        self.hitPoints = hitPoints
        self.loader = loader
        self.hitPoints = hitPoints
        self.addPoints = addPoints
        self.active = active

        mydir = os.path.abspath(sys.path[0])

        # Convert that to panda's unix-style notation.
        mydir = Filename.fromOsSpecific(mydir).getFullpath()

        target = self.loader.loadModel(mydir + "/models/poligono1.egg")
        target.setTexture(self.loader.loadTexture(mydir + '/models/tex/textB1!.png'))

        targetParent = self.render.attachNewNode("targetParent")
        targetParent.setPos(pos)  # 0, 15, 0
        targetParent.setScale(0.5, 0.1, 0.5)
        targetParent.lookAt(0, 0, 0)
        target.reparentTo(targetParent)
        target.setPos(0, 0, 5)
        target.setHpr(180,0,0)
        self.target = target

        sciana1 = self.loader.loadModel(mydir + "/models/wall.egg")
        sciana1.reparentTo(targetParent)
        sciana1.setTexture(self.loader.loadTexture(mydir + '/models/tex/brick.jpg'))
        targetParentPos = targetParent.getPos()
        sciana1.setPos(-1.5,2,-2.1)
        sciana1.setScale(1.8)
        sciana1.wrtReparentTo(self.render)
        #sciana1.setHpr(targetParent.getHpr())
        self.targetParent = targetParent


        shape = BulletBoxShape(Vec3(2, 1, 5))

        self.name = str(pos)
        node = CustomBulletBoxShape(self.name, self.onHit)
        # node.setMass(1.0)

        node.addShape(shape)

        np = self.render.attachNewNode(node)
        np.reparentTo(target)
        np.setPos(0, -0.1, 0)
        np.setCollideMask(BitMask32.bit(0))

        self.np = np

        self.bulletWorld.attachRigidBody(node)
        x = targetParent.getHpr().x
        self.y = targetParent.getHpr().y
        if not active:
            LerpHprInterval(targetParent, 0.01, Point3(x, 90, 0)).start()
            #np.setPos(0, -0.1, 100)
            self.np.setCollideMask(BitMask32.bit(1))

    def onHit(self):
        if not self.active:
            return
        x = self.targetParent.getHpr().x
        LerpHprInterval(self.targetParent, 0.2, Point3(x, 90, 0)).start()
        #self.np.setPos(0, -0.1, 100)
        self.np.setCollideMask(BitMask32.bit(1))
        self.addPoints(self.hitPoints)
        self.active = False
        pass

    def activate(self):
        if self.active:
            return
        x = self.targetParent.getHpr().x
        #self.np.setPos(0, -0.1, 0)
        LerpHprInterval(self.targetParent, 0.2, Point3(x, self.y, 0)).start()
        self.np.setCollideMask(BitMask32.bit(0))
        # self.np.reparentTo(self.target)
        print(self.target.getHpr())
        self.active = True

    def deactivate(self):
        x = self.targetParent.getHpr().x
        LerpHprInterval(self.targetParent, 0.2, Point3(x, 90, 0)).start()
        # np.setPos(0, -0.1, 100)
        self.np.setCollideMask(BitMask32.bit(1))
        self.active = False

    def setShapes(self, body):
        shape = BulletBoxShape(Vec3(2, 1, 5.5))


class CustomBulletBoxShape(BulletRigidBodyNode):
    def __init__(self, name, targetFun):
        BulletRigidBodyNode.__init__(self, name)
        self.targetFun = targetFun

    def onHit(self):
        self.targetFun()
