import pygame
from pygame.locals import *
from constants import *
import os

pygame.init()

#z-index with tag (order of the add of tag)
class Objects:
    def __init__(self, root):
        self.tags={}
        self.values=[]
        self.root=root

    def exist(self, tag):
        for i in self.tags:
            if tag==i:
                return True
        return False

    def add(self, surface, posx, posy, tag):
        if self.exist(tag):
            self.values[self.tags[tag]]+=[[surface, posx, posy]]
        else:
            self.tags[tag]=len(self.values)
            self.values+=[[[surface, posx, posy]]]
        self.root.blit(surface, (posx, posy) )

    def del_tag(self, tag):
        if self.exist(tag):
            memo=self.tags[tag]
            del self.values[self.tags[tag]]
            del self.tags[tag]
            for i in self.tags:
                if self.tags[i]>memo:
                    self.tags[i]-=1

    def display(self):
        for groups in self.values:
            for objects in groups:
                self.root.blit(objects[0], (objects[1], objects[2]) )
        pygame.display.flip()

    def move(self, tag, x, y):
        for objects in self.values[self.tags[tag]]:
            objects[1]+=x
            objects[2]+=y

    def len(self, tag):
        return len(self.values[self.tags[tag]])

    def get_valuesoftag(self, tag):
        return self.values[self.tags[tag]]


class Animation():
    def __init__(self, objects):
        self.dico={}
        self.list=[]
        self.load()
        self.objects=objects
        self.ticks = pygame.time.get_ticks
        self.uid = 0

    def load(self):
        for folder in os.listdir("animation"):
            for subfolder in os.listdir(os.path.join("animation",folder)):
                self.dico[folder+"/"+subfolder]=[]
                for i in range(len(os.listdir(os.path.join("animation",folder,subfolder)))):
                    path=subfolder+str(i)+".png"
                    frame=pygame.image.load(os.path.join("animation",folder,subfolder,path)).convert()
                    self.dico[folder+"/"+subfolder]+=[frame]

    def start(self, name, posx, posy, time, repetition, tag):
        path=os.path.join("animation",name)
        N=len(os.listdir(path))
        self.list+=[[name, posx, posy ,time, repetition, tag, N, self.ticks(), tag+self.get_uid()]]
        print(self.list)

    def find(self):
        for i, [name, posx, posy, time, repetition, tag, N, ticks, tag2] in enumerate(self.list):
            nb_img = (N*(self.ticks()-ticks)) // time
            if nb_img < (N*repetition):
                self.objects.del_tag(tag2)
                self.objects.add(self.dico[name][nb_img%N], posx, posy, tag2)
            else:
                self.stop_uid(tag2)

    def move(self, tag, x, y):
        for anim in self.list:
            if anim[5]==tag:
                anim[1]+=x
                anim[2]+=y

    def stop_uid(self, tag2):
        self.objects.del_tag(tag2)
        for i, anim in enumerate(self.list):
            if anim[8]==tag2:
                self.list.pop(i)

    def stop(self, tag):
        self.objects.del_tag(tag)
        for i, anim in enumerate(self.list):
            if anim[5]==tag:
                self.list.pop(i)

    def get_uid(self):
        self.uid += 1
        return str(self.uid - 1)


class Collision():
    def __init__(self, objects):
        self.tags=[]
        self.objects=objects

    def add(self, tag):
        self.tags+=[tag]

    def del_tag(self, tag):
        self.tags.remove(tag)

    def find(self, tag, direction):
        #checking if self.tags (with s) overlap the unique tag in para
        #thank to a boxofsafety to the right/left/top/bottom
        #of the surfaces of the unique tag in para
        for tag2 in self.tags:
            for value in self.objects.get_valuesoftag(tag2):
                box=self.create_boxofsafety(value, direction)
                boxtest=pygame.Surface( (box[2], box[3]) )
                boxtest.fill((255,128,128))
                self.objects.del_tag("boxtest")
                self.objects.add(boxtest, box[0], box[1], "boxtest")
                for value2 in self.objects.get_valuesoftag(tag):
                    if not( (box[0]>value2[1]+value2[0].get_width())
                        or (box[0]+box[2]<value2[1])
                        or (box[1]>value2[2]+value2[0].get_height())
                        or (box[1]+box[3]<value2[2]) ):
                        return True
        return False

    @staticmethod
    def create_boxofsafety(value, direction):
            x=value[1]
            y=value[2]
            width=value[0].get_width()
            height=value[0].get_height()
            if direction==K_w:
               boxofsafety=[x, y-boxofsafety_length, width, boxofsafety_length]
            elif direction==K_s:
               boxofsafety=[x, y+height, width, boxofsafety_length]
            elif direction==K_a:
               boxofsafety=[x-boxofsafety_length, y, boxofsafety_length, height]
            elif direction==K_d:
               boxofsafety=[x+width, y, boxofsafety_length, height]
            return boxofsafety



class Movement():
    def __init__(self, objects, collision):
        self.tags=[]
        self.directions={K_w:[0,1], K_s:[0,-1], K_a:[1,0], K_d:[-1,0]}
        self.objects=objects
        self.collision=collision

    def add(self, tag):
        self.tags+=[tag]

    def del_tag(self, tag):
        self.tags.remove(tag)

    def processing(self, key):
        for direction in self.directions:
            if key==direction:
                for tag in self.tags:
                    if not self.collision.find(tag, direction):
                        self.objects.move(tag, wall_speed*self.directions[direction][0], wall_speed*self.directions[direction][1])


class Perso():
    counter = 0
    def __init__(self, objects, animation):
        self.tag = "perso" + str(Perso.counter)
        Perso.counter += 1
        self.objects = objects
        self.animation = animation
        self.subfolder_sprites = None

    def subfolder_sprites(self, subfolder):
        self.subfolder_sprites = subfolder

    def spawn(self, x ,y):
        self.animation.start(self.subfolder+p_right, x, y, -1, self.tag)


class Fonts:
    def __init__(self):
        self.list=[os.path.join("fonts",file) for file in os.listdir("fonts")]

    def get_class(self, index, size):
        return pygame.font.Font(self.list[index], size)
