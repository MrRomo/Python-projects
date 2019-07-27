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

import rospy
import sys
from face.srv import FaceDetector
from face.srv import FaceMemorize
from face.srv import FaceRecognize
from Class.face_id import FaceID
try:
    from robot_toolkit_msgs.srv import vision_tools_srv
    from robot_toolkit_msgs.msg import camera_parameters_msg, depth_to_laser_msg, vision_tools_msg
except ImportError, e:
    print("Error on %s" % e)

if __name__ == '__main__':
    try:
        rospy.init_node('robot_face')
        params = []
        try:
            params.append('webcam' if sys.argv.index('webcam') else 'pepper')
        except:
            try:
                params.append('file' if sys.argv.index('file') else 'pepper')
            except:
                params.append('pepper')
        try:
            params.append(str(sys.argv[sys.argv.index('local')]))
        except:
            params.append('cloud')
        face = FaceID(params[0], params[1])
        print(params)
        rospy.Service('robot_face_detector', FaceDetector, face.detectFace)
        rospy.Service('robot_face_recognize',FaceRecognize, face.recognizeFace)
        rospy.Service('robot_face_memorize', FaceMemorize, face.memorizeFace)
        print("robot face node started")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
