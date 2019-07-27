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
import sys
import os
import cv2
import math
import pickle
import sklearn
import numpy as np
import pandas as pd
from tqdm import tqdm
import face_recognition
from collections import Counter
from PIL import Image, ImageDraw, ImageFont


class NeuralClass:

    def __init__(self, frame, percent=0.1, tolerance=0.4):

        self.ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
        self.frame = frame
        self.percent = percent
        self.tolerance = tolerance
        self.coord = []
        self.percents = []
        self.people = []
        self.race = []
        self.gender = []
        self.age = []
        self.hair = []
        self.glasses = []
        self.utils = Utils()
        self.COLS = ['Male', 'Asian', 'White', 'Black',  'Baby', 'Child', 'Youth', 'Middle Aged', 'Senior', 'Black Hair', 'Blond Hair','Brown Hair', 'Bald', 'No eyewear', 'Eyeglasses', 'Sunglasses', 'Mustache', 'Smiling', 'Curly Hair', 'Wavy Hair', 'Straight Hair']
        self.N_UPSCLAE = 1
        self.clf, self.labels = self.getModel(self.ROOT_PATH+'/Models/race_and_gender_model.pkl')
        self.personT = []
        # inicializa la clase recortando, guardando las caras y descartando los frames malos
        self.faces = self.cropper()
        self.prediction = self.clasifier()

    def getModel(self, path):

        with open(path) as f:
            clf, labels = pickle.load(f)
            return clf, labels

    def cropper(self):

        faces = list()
        frames = list()
        print("cropping n_images {}".format(len(self.frame)))
        for frame in self.frame:
            frame_area = frame.shape[0]*frame.shape[1]
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            person_loc = face_recognition.face_locations(small_frame)
            person_loc.sort(key=self.utils.sortLocation, reverse = False)
            if(len(person_loc)):  # detecta si hay personas
                print("Person detect: {}".format(len(person_loc)))
                people, areas = self.utils.setDictionary(person_loc)
                facesT = []
                cordT = []
                for person in person_loc:
                    t, r, b, l = self.utils.increase(list(np.asarray(person)*4))
                    # recortar imagenes image[y:y+h, x:x+w]
                    facesT.append(frame[t:b, l:r])
                    cordT.append((t, r, b, l))

                self.personT= [facesT,cordT, people]
                # ordena las caras de mayor a menor detectadas en el frame
                # people.sort(key=self.utils.sortDictionary, reverse=True)
                # encuentra la cara mas grande
                
                person_location = person_loc[np.argmax(areas)]
                people = people[np.argmax(areas)]
                # top, rigth, bottom, left (t,r,b,l)
                t, r, b, l = self.utils.increase(list(np.asarray(person_location)*4))
                percent = max(areas)*100/float(frame_area)
                if(percent >= self.percent):
                    # recortar imagenes image[y:y+h, x:x+w]
                    faces.append(frame[t:b, l:r])
                    frames.append(frame)
                    self.coord.append((t, r, b, l))
                    self.percents.append(round(percent, 2))
                    self.people.append(people)
        # guarda unicamente los frames donde hay caras
        self.frame = frames
        return faces

    def detect(self):
        if len(self.people):
            return self.people
        return []

    def detectAll(self):
        if len(self.people):
            people = self.personT[2]
            return people
        return []

    def encode(self):

        person_encoding = []
        if len(self.detect()):
            for i in range(len(self.faces)):
                person_encoding.append(face_recognition.face_encodings(self.faces[i])[0])

        return person_encoding

    def encode_one(self):
        if len(self.detect()):
            person_encoding = face_recognition.face_encodings(self.faces[0])[0]
            return person_encoding
        else:
            return []

    def compare(self, known_faces, personGroup):

        people = None
        if len(self.detect()): people = self.people[0]
        if len(self.detect()) and len(personGroup):
            person_encoding = self.encode_one()
          
            matches = face_recognition.compare_faces(known_faces, person_encoding, tolerance=self.tolerance)

            face_distances = face_recognition.face_distance(known_faces, person_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                people = personGroup[best_match_index]
                people['accuracy'] = 1-face_distances[best_match_index]*self.tolerance
                people['faceRectangle'] = self.people[0]['faceRectangle']
        print ("people from compare {}".format(people ))
        return people

    def clasifier(self):

        prediction = None
        if len(self.detect()):
            face_encodings = self.encode()
            prediction = pd.DataFrame(self.clf.predict_proba(face_encodings), columns=self.labels)
            prediction = prediction.loc[:, self.COLS]
            self.glasses = prediction[['Eyeglasses', 'Sunglasses']]
            print prediction
            for row in prediction.iterrows():
                self.gender.append('male' if row[1]['Male'] > 0.5 else 'female')
                self.race.append(np.argmax(row[1][1:4]))
                self.age.append(np.argmax(row[1][4:9]))
                self.hair.append(np.argmax(row[1][9:13]))
        return prediction

    def getRace(self):
        return self.getCharacter(self.race)

    def getGlass(self):
        glasses = 'No'
        glass = self.glasses["Eyeglasses"]
        desviacion = glass.std()
        media = glass.mean()
        max =  glass[np.argmax(glass)]
        min =  glass[np.argmin(glass)]
        print glass
        print "Media: {} - Desviacion : {} - Max: {} - Min: {}".format(media,desviacion,max,min)
        if ((media > 0.2)):
            glasses = "Yes"
        res= {"res": glasses, "percent": None}
        return res

    def getAge(self):
        return self.getCharacter(self.age)

    def getHair(self):
        return self.getCharacter(self.hair)

    def getGender(self):
        return self.getCharacter(self.gender)

    def getCharacter(self, val):
        pred = Counter(val)
        count = pred.most_common()[0]
        percent = count[1]*100/float(len(val))
        res = {"res": count[0], "percent": percent}
        return res


class Utils:
    def sortDictionary(self, val):
        return val['faceRectangle']['width']*val['faceRectangle']['left']
    def sortLocation(self, val):
        return val[3]

    def setDictionary(self, locations):
        people = list()
        areas = list()
        for face_location in locations:
            face_location = list(np.array(face_location)*4)
            width = face_location[1]-face_location[3]
            height = face_location[2]-face_location[0]
            faceAtr = {
                "race": None,
                "gender": None,
                "age": None,
                "hair": {
                    "hairColor": None
                },
                "glasses":  None
            }
            dictionary_of_features = {'faceId': None, 'faceRectangle': {'width': int(width), 'top': int(
                face_location[0]), 'height': int(height), 'left': int(face_location[3])}, 'faceAttributes': faceAtr }
            people.append(dictionary_of_features)
            areas.append(width*height)
            print areas
        return people, areas

    def increase(self, dimentions):
        dim = list()
        prop = 1.07
        dim.append(int(dimentions[0]*0.3))
        dim.append(int(dimentions[1]*prop))
        dim.append(int(dimentions[2]*prop))
        dim.append(int(dimentions[3]*0.92))
        return dim
