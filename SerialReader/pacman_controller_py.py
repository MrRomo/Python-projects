#!/usr/bin/env python
import rospy
import random
import serial
import serialReader


from pacman.msg import actions
from pacman.msg import pacmanPos
from pacman.msg import ghostsPos
from pacman.msg import cookiesPos
from pacman.msg import bonusPos
from pacman.msg import game
from pacman.msg import performance
from pacman.srv import mapService


def pacmanPosCallback(msg):
#    rospy.loginfo('# Pacmans: {} posX: {} PosY: {}'.format(msg.nPacman, msg.pacmanPos.x, msg.pacmanPos.y) )
    pass

def ghostsPosCallback(msg):
#    rospy.loginfo('# Ghosts: {} '.format(msg.nGhosts))
#    for i in range(msg.nGhosts):
#        rospy.loginfo('Pos Ghosts {}: PosX {} PosY {}'.format(i, msg.ghostsPos[i].x, msg.ghostsPos[i].y))
    pass

def cookiesPosCallback(msg):
#    rospy.loginfo('# Cookies: {} '.format(msg.nCookies))
#    for i in range(msg.nCookies):
#        rospy.loginfo('Pos Cookies {}: PosX {} PosY {}'.format(i, msg.cookiesPos[i].x, msg.cookiesPos[i].y))
    pass

def bonusPosCallback(msg):
#    rospy.loginfo('# bonus: {} '.format(msg.nBonus))
#    for i in range(msg.nBonus):
#        rospy.loginfo('Pos Bonus {}: PosX {} PosY {}'.format(i, msg.bonusPos[i].x, msg.bonusPos[i].y))
    pass

def gameStateCallback(msg):
#    rospy.loginfo('Game State: {} '.format(msg.state))
    pass

def performanceCallback(msg):
#    rospy.loginfo('Lives: {} Score: {} Time: {} PerformEval: {}'.format(msg.lives, msg.score, msg.gtime, msg.performEval) )
    pass

def pacman_controller_py():
    
    rospy.init_node('pacman_controller_py', anonymous=True)
    pub = rospy.Publisher('pacmanActions0', actions, queue_size=10)
    rospy.Subscriber('pacmanCoord0', pacmanPos, pacmanPosCallback)
    rospy.Subscriber('ghostsCoord', ghostsPos, ghostsPosCallback)
    rospy.Subscriber('cookiesCoord', cookiesPos, cookiesPosCallback)
    rospy.Subscriber('bonusCoord', bonusPos, bonusPosCallback)
    rospy.Subscriber('gameState', game, gameStateCallback)
    rospy.Subscriber('performanceEval', performance, performanceCallback)

    try:
        mapRequestClient = rospy.ServiceProxy('pacman_world', mapService)
        mapa = mapRequestClient("Controller py")
        rospy.loginfo("# Obs: {}".format(mapa.nObs))
        rospy.loginfo("minX : {}  maxX : {}".format(mapa.minX, mapa.maxX))
        rospy.loginfo("minY : {}  maxY : {}".format(mapa.minY, mapa.maxY))

        rate = rospy.Rate(10) # 10hz
        msg = actions();
        msg.action = 4;
        while not rospy.is_shutdown():
            
            move = serialReader.serialKey()
            
            if(move!=4):
                msg.action = move
            print(game())
            print("Action msg.action: {}".format(msg.action))
           
            pub.publish(msg.action)     
            rate.sleep()

    except rospy.ServiceException as e:
        print ("Error!! Make sure pacman_world node is running ")

if __name__ == '__main__':
    try:
        pacman_controller_py()
    except rospy.ROSInterruptException:
        pass
