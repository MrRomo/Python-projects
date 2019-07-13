
#!/usr/bin/env python
# license removed for brevity

"""
//======================================================================//
//  This software is free: you can redistribute it and/or modify        //
//  it under the terms of the GNU General Public License Version 3,     //
//  as published by the Free Software Foundation.                       //
//  This software is distributed in the hope that it will be useful,    //
//  but WITHOUT ANY WARRANTY; without even the implied warranty of      //
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..  See the      //
//  GNU General Public License for more details.                        //
//  You should have received a copy of the GNU General Public License   //
//  Version 3 in the file COPYING that came with this distribution.     //
//  If not, see <http://www.gnu.org/licenses/>                          //
//======================================================================//
//                                                                      //
//      Copyright (c) 2019 SinfonIA Pepper RoboCup Team                 //
//      Sinfonia - Colombia                                             //
//      https://sinfoniateam.github.io/sinfonia/index.html              //
//                                                                      //
//======================================================================//
"""
import cv2
import os
import sys
import face_recognition
import numpy as np
from packet import Packing



class PersonLocal:

    def __init__(self):

        self.packing = Packing()
        self.fileName = ["personsGroup.pckl","personModel.pckl"]
        self.personGroup = self.packing.unpack(self.fileName[0])
        self.personModel = self.packing.unpack(self.fileName[1])
        self.frame = None

    def detectPerson(self, frame):
        self.frame = frame
        rgb_frame = frame[:, :, ::-1] 
        frame_size = frame.shape[0]*frame.shape[1]
        face_locations = face_recognition.face_locations(rgb_frame)
        print("Face detected ",len(face_locations), face_locations)
        peoples,areas = setDictionary(face_locations)        
        peoples.sort(key=sortDictionary, reverse=True)
        return peoples

    def enrol(self, frame, name):
        person_locations = face_recognition.face_locations(frame)
        if(len(person_locations)):
            peoples, areas = setDictionary(person_locations)        
            indexMax = areas.index(max(areas)) #encuentra la cara mas grande
            person_location = person_locations[indexMax]
            crop_img = frame[person_location[0]:person_location[0]+person_location[2]-person_location[0], person_location[3]:person_location[3]+person_location[1]-person_location[3]]
            # cv2.imshow("cropped", crop_img)
            # cv2.waitKey(0) 
            person_encoding = face_recognition.face_encodings(crop_img)[0]
            person = peoples[indexMax]
            self.personModel.append(person_encoding)
            person["gender"] = None
            person["name"] = name
            self.personGroup.append(person)
            self.packing.pack(self.personGroup,self.fileName[0])
            self.packing.pack(self.personModel,self.fileName[1])
            return self.personGroup[-1]
        else:
            return []
    
    def identify(self, frame):
        face_locations = face_recognition.face_locations(frame)
        person_encoding = face_recognition.face_encodings(frame,face_locations)
        known_faces = self.personModel
        # print(person_encoding)
        # print(type(person_encoding))
        
        for face_encoding in person_encoding:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            print("matches",matches)
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                return self.personGroup[first_match_index]
            else:
                return []
    
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
        selfd.frames = []

    def sort_less_blurred(self, images):
        self.fm = qe.PriorityQueue(100)
        self.frames = []
        if type(images) == dict:
            for imgID in images:
                self.fm.put(
                    (1/cv2.Laplacian(images[imgID], cv2.CV_64F).var(), imgID))
            for i in range(self.nImages):
                dat = self.fm.get()
                nIma = dat[1]
                self.frames.append(images[nIma])
        else:
            print('review images type')

def sortDictionary(val):
    return val['faceRectangle']['width']



