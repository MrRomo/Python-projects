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
from packet import Packing
from azure import Azure
import Queue as qe
from edit_files import Group
from edit_files import PersonFiles


class PersonCloud:

    def __init__(self):
        
        self.ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
        self.azureService = Azure()
        self.image = None
        self.packing = Packing()
        self.fileName = ["personGroupCloud.pckl"]
        self.personGroup = self.packing.unpack(self.fileName[0])

    def detectPerson(self, frame):
        self.image = frame
        imgBytes = self.check_img(frame) 
        people = self.azureService.detect(imgBytes)
        return people

    
    def enrol(self, name, frames):
        person_id, self.codeError = self.azureService.create_person(id)
        print("PersonID: ", person_id)
        succes = False
        if person_id is not None:
            self.id_azure = person_id
            for frame in frames:
                imgBytes = self.check_img(frame)
                response = self.azureService.add_face(imgBytes, person_id)
                person = response[1]
                if response[0]:  
                    succes = True
                    person["person_id"] = person_id
                    person["name"] = name
                    print(person)
                        # self.G.add(PersonFiles(id, person_id, self.hairColor, self.glasses, self.gender, self.age))
            # if succes:
            #     self.azureService.train()
            # else:
            #     print('No entrenado')
            # return 
        return []

        person_locations = face_recognition.face_locations(frame)
        if(len(person_locations)):
            peoples, areas = setDictionary(person_locations)        
            indexMax = areas.index(max(areas)) #encuentra la cara mas grande
            person_location = person_locations[indexMax]
            crop_img = frame[person_location[0]:person_location[0]+person_location[2]-person_location[0], person_location[3]:person_location[3]+person_location[1]-person_location[3]]
            cv2.imshow("cropped", crop_img)
            cv2.waitKey(0) 
            person_encoding = face_recognition.face_encodings(crop_img)[0]
            person = peoples[indexMax]
            self.personModel.append(person_encoding)
            person["gender"] = None
            person["person"] = None
            person["name"] = name
            person["personId"] = uuid.uuid1()
            self.personGroup.append(person)
            self.packing.pack(self.personGroup,self.fileName[0])
            self.packing.pack(self.personModel,self.fileName[1])
            return self
        else:
            return []
    
    def identifyPerson(self, frame):
        face_locations = face_recognition.face_locations(frame)
        person_encoding = face_recognition.face_encodings(frame,face_locations)
        known_faces = self.personModel
        
        for face_encoding in person_encoding:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            print("matches",matches)
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

    def check_img(self, frame):
        retval, encoded_image = cv2.imencode('.png', frame)
        return encoded_image.tobytes()


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

def setDictionary(locations):
    peoples = list()
    areas = list()
    for face_location in locations:
            width = face_location[1]-face_location[3]
            height = face_location[2]-face_location[0]
            dictionary_of_features = {'faceId': None, 'faceRectangle': {'width': int(width), 'top': int(face_location[0]), 'height': int(height), 'left': int(face_location[3])}, 'faceAttributes': None}
            peoples.append(dictionary_of_features)
            areas.append(width*height)
    return peoples,areas


    