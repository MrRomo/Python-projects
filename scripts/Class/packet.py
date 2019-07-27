# -*- coding: utf-8 -*-
#!/usr/bin/env python
# license removed for brevity
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
