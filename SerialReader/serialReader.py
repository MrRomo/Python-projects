import serial 
import serial.tools.list_ports as port_list


#Serial Controller
def lookPorts():
    ports = list(port_list.comports())
    for p in ports:
        print (p)

def readPorts():
    print("Reading ports ...")
    ports = list(port_list.comports())
    i = 0
    for p in ports:
        print ("Port [{}] : {}".format(i,p))
        portDirection = p[0]
        print(type(portDirection))
        print((portDirection))
        ser = serial.Serial(portDirection, 9600)
        ser.write('a')     # write a string
        try:
            action = ser.read()
            if(action=='4'):
                print "Controller finded: {} ".format(portDirection)
                return portDirection
            else:
                ser.close()
        except ValueError:
            pass
        i+=1

def serialKey(): 
    try:
        action = int(float(ser.read().strip()))
    except ValueError:
        action = 4
    return action


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    while True:
        print(ser.readline().strip())