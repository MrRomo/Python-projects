#!/usr/bin/env python
# //======================================================================//
# //  This software is free: you can redistribute it and/or modify        //
# //  it under the terms of the GNU General Public License Version 3,     //
# //  as published by the Free Software Foundation.                       //
# //  This software is distributed in the hope that it will be useful,    //
# //  but WITHOUT ANY WARRANTY; without even the implied warranty of      //
# //  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..  See the      //
# //  GNU General Public License for more details.                        //
# //  You should have received a copy of the GNU General Public License   //
# //  Version 3 in the file COPYING that came with this distribution.     //
# //  If not, see <http://www.gnu.org/licenses/>                          //
# //======================================================================//
# //                                                                      //
# //      Copyright (c) 2019 SinfonIA Pepper RoboCup Team                 //
# //      Sinfonia - Colombia                                             //
# //      https://sinfoniateam.github.io/sinfonia/index.html              //
# //                                                                      //
# //======================================================================//


import cv2
import os
import sys
import face_recognition
import uuid
import json
from neural_class import NeuralClass
from utils import Utils
from packet import Packing


class PersonLocal:

    def __init__(self):
        self.ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
        self.packing = Packing()
        self.fileName = ["personGroup.pckl", "personModel.pckl"]
        self.personGroup = self.packing.unpack(self.fileName[0])
        self.personModel = self.packing.unpack(self.fileName[1])
        self.frame = None
        self.tolerance = self.get_parameters()

    def get_parameters(self):
        with open(self.ROOT_PATH+"/Resources/interaction_parameters.json") as f:
            secretInfo = json.load(f)
            print("Tolerance: ", secretInfo["tolerance"])
            return secretInfo["tolerance"]

    def detectPerson(self, frame):
        
        self.frame = frame
        neural = NeuralClass([frame])
        people = neural.detect()
        return people

    def detectAllPerson(self, frame):
        self.frame = frame
        neural = NeuralClass([frame])
        people = neural.detectAll()
        return people

    def enrol(self, name, frame):
        self.image = frame
        neural = NeuralClass(frame)
        person = None
        if len(neural.detect()):
            person_encoding = neural.encode_one()
            self.personModel.append(person_encoding)
            person = neural.people[0]
            faceAtr = {
                "race": neural.getRace()["res"],
                "gender": neural.getGender()["res"],
                "age": neural.getAge()["res"],
                "hair": {
                    "hairColor": neural.getHair()["res"]
                },
                "glasses":  neural.getGlass()["res"]
            }
            person["name"] = name
            person["faceAttributes"] = faceAtr
            person["personId"] = str(uuid.uuid1())
            print ("person ATTRIBUTES{}".format(person))
            self.personGroup.append(person)
            self.packing.pack(self.personGroup, self.fileName[0])
            self.packing.pack(self.personModel, self.fileName[1])
        return person

    def identifyPerson(self, frame):

        self.frame = frame
        neural = NeuralClass([frame])
        people = None
        if(neural.detect()):
            people = neural.compare(self.personModel, self.personGroup)
            print people
            faceAtr = {
                "race": neural.getRace()["res"],
                "gender": neural.getGender()["res"],
                "age": neural.getAge()["res"],
                "hair": {
                    "hairColor": neural.getHair()["res"]
                },
                "glasses":  neural.getGlass()["res"]
            }
            people["faceAttributes"] = faceAtr
            print people
        return people
        

    def persons_in_group(self):
        personsList = self.personGroup
        return personsList

    def deleteAll(self):
        self.personGroup = list()
        self.packing.pack(self.personGroup)
        return 0


class Less_Blurred:
    def __init__(self, nImages):
        self.nImages = nImages
        self.fm = qe.PriorityQueue(100)
        self.frames = []

    def sort_less_blurred(self, images):
        self.fm = qe.PriorityQueue(100)
        self.frames = []
        if type(images) == dict:
            for imgID in images:
                self.fm.put((1/cv2.Laplacian(images[imgID], cv2.CV_64F).var(), imgID))
            for i in range(self.nImages):
                dat = self.fm.get()
                nIma = dat[1]
                self.frames.append(images[nIma])
        else:
            print('review images type')
