#! /usr/bin/python
# -*- coding: utf-8 -*-

#    pyNekketsu
#    Copyright (C) 2011  JM Muller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import os
import random
from sprite import Sprite
from sprite import compileimage
from inputs import Inputs
from player import Player


#For the goal keeper (GK)
#always AI-controlled
class Player_GK(Player):
    difficulty=2 #out of 10
    def __init__(self, team, head,pos_init,field_half_length):
        Player.__init__(self,team,head,pos_init,field_half_length)
        self.inputs=Inputs(0)
    def update(self,match):
        #try to catch the ball 
        if ((self.state=="walk") or (self.state=="jump")) and (match.ball.owner==0):
            if (abs(match.ball.pos[0]-self.pos[0]-self.direction*1)<4) \
                and (abs(match.ball.pos[1]-self.pos[1])<5)  \
                and ((match.ball.pos[2]-self.pos[2])<7): #Z
                if (abs(match.ball.speed[0])>10*self.control):#too much in opposite direction : KO
                    self.state="hurt"
                    self.anim_index=0
                    match.ball.speed[0]*=-0.6
                    match.ball.speed[2]+=(match.ball.pos[2]-self.pos[2])
                    Player.snd_pass.play()
                else:#not enought to hurt...
                    if (match.ball.speed[0]*self.direction<10):#speed X must be slow or in opposite direction
                        match.ball.owner=self
                        self.has_ball=match.ball
                        match.ball.speed=[0,0,0]
                
        Player.update(self,match) 
        self.think(match)

    def think(self,match):#press on virtual keys
        #stay close to the goal
        goal_position=(self.team.wing*match.field.half_length,match.field.goal_latitude[self.team.wing])

        if (self.has_ball!=0):
            #look in the other goal's direction
            if (self.team.wing==-1):
                self.inputs.R=True
            else:
                self.inputs.L=True
            #aim in the opposite direction of his goal, to avoid bad rebounce
            if (match.field.goal_latitude[self.team.wing]-10>self.pos[1]) or (random.randint(0, 4)==0):
                self.inputs.D=True
            if (match.field.goal_latitude[self.team.wing]+10<self.pos[1]) or (random.randint(0, 4)==0):
                self.inputs.U=True
            #shoot!
            self.inputs.B=True
        else:#do not have the ball
            if (abs(goal_position[0]-match.ball.pos[0])>abs(goal_position[0]-self.pos[0])):
                #ball is not between GK and the goal

                #stay close to the goal 
                if (self.team.wing==-1):
                    if ((self.pos[0]-goal_position[0])>25):
                        self.inputs.L=True
                    if ((self.pos[0]-goal_position[0])<22):
                        self.inputs.R=True
                    elif (self.direction==-1):
                        self.direction=1#change player without button... just for this time!
                else:
                    if (-(self.pos[0]-goal_position[0])>25):
                        self.inputs.R=True
                    if (-(self.pos[0]-goal_position[0])<22):
                        self.inputs.L=True
                    elif (self.direction==1):
                        self.direction=-1#change player without button... just for this time!

                #jump!
                if (self.pos[2]<match.ball.pos[2]-6) and (abs(self.pos[0]-match.ball.pos[0])<10) and (-self.team.wing*match.ball.speed[0]<0):
                    self.inputs.C=True

                #set y pos to be between ball and goal
                if (abs(match.ball.pos[0]-goal_position[0])<1):
                    between_pos_y=match.ball.pos[1]
                else:
                    between_pos_y=goal_position[1]+(self.pos[0]-goal_position[0])*(match.ball.pos[1]-goal_position[1])/(match.ball.pos[0]-goal_position[0])
                    between_pos_y+=random.randint(Player_GK.difficulty,15)-random.randint(Player_GK.difficulty,15)

                if (self.pos[1]<between_pos_y-2) and (random.randint(0, 13/self.precision)<3+Player_GK.difficulty):
                    self.inputs.U=True
                if (self.pos[1]>between_pos_y+2) and (random.randint(0, 13/self.precision)<3+Player_GK.difficulty):
                    self.inputs.D=True

                    
            else:
                #ball is between GK and the goal
                if (self.pos[0]<match.ball.pos[0]-2) and (random.randint(0, 15)<5+Player_GK.difficulty):
                    self.inputs.R=True
                if (self.pos[0]>match.ball.pos[0]+2) and (random.randint(0, 15)<5+Player_GK.difficulty):
                    self.inputs.L=True
                if (self.pos[1]<match.ball.pos[1]-5) and (random.randint(0, 15)<5+Player_GK.difficulty):
                    self.inputs.U=True
                if (self.pos[1]>match.ball.pos[1]+5) and (random.randint(0, 15)<5+Player_GK.difficulty):
                    self.inputs.D=True
     


            for p in match.player_list:
                if (p!=self):
                    if (p.team!=self.team):#attack!
                        if (abs(p.pos[0]-self.pos[0])<6 and abs(p.pos[1]-self.pos[1])<6):
                            if (random.randint(0, 80/self.agressivity)==0) or (p.has_ball!=0):
                                self.inputs.B=True


