#!/usr/bin/env python
# coding: utf-8

import pickle


class Packing():

    def pack(self, data, file):
        pickling_on = open(file, "wb")
        pickle.dump(data, pickling_on)
        pickling_on.close()

    def unpack(self, file):
        try:
            pickling_on = open(file, "rb")
            data = pickle.load(pickling_on)
            pickling_on.close()
            return data
        except:
            data = []
            pickling_on = open(file, "wb")
            pickle.dump(data, pickling_on)
            return data

    def createFile(self, file):
        try:
            pickling_on = open(file, "rb")
            pickling_on.close()
        except:
            data = []
            pickling_on = open(file, "wb")
            pickle.dump(data, pickling_on)
