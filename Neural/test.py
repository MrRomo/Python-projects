from identify import PersonLocal
import cv2

personlocal = PersonLocal()

video_capture = cv2.VideoCapture(0)
frame = video_capture.read()[1]
# frame = cv2.imread('Mayra.jpg')
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
sframe = small_frame[:, :, ::-1]


def detect(frame):
    persondetect = personlocal.detectPerson(frame)
    print(persondetect)

def memorize(frame, name):
    personlocal.enrol(frame, name)
    print(personlocal.persons_in_group())

def identify(frame):
    print(personlocal.identify(frame))

def delete():
    personlocal.deleteAll()


# delete()
# detect(sframe)
# memorize(frame,"Ricardo")
# identify(sframe)
print(personlocal.persons_in_group())
