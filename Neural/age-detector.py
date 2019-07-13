import face_recognition
import cv2

cap = cv2.VideoCapture(0)
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
            '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']


def load_caffe_models():

    age_net = cv2.dnn.readNetFromCaffe(
        'deploy_age.prototxt', 'age_net.caffemodel')
    gender_net = cv2.dnn.readNetFromCaffe(
        'deploy_gender.prototxt', 'gender_net.caffemodel')
    return(age_net, gender_net)


def getPrediction():

    while (1):

        ret, frame = cap.read()

        person_locations = face_recognition.face_locations(frame)

        print("Person detect: {}".format(len(person_locations)))
        if(len(person_locations)):

            people, areas = setDictionary(person_locations)
            indexMax = areas.index(max(areas))  # encuentra la cara mas grande
            person_location = person_locations[indexMax]
            crop_img = frame[person_location[0]:person_location[0]+person_location[2]-person_location[0],
                            person_location[3]:person_location[3]+person_location[1]-person_location[3]]
            blob = cv2.dnn.blobFromImage(frame, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            # Predict Gender
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]
            print("Gender : " + gender)
            # cv2.imshow("cropped", crop_img)
            # cv2.waitKey(0)
            # Predict Age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]
            print("Age Range: " + age)
            overlay_text = "%s %s" % (gender, age)
            image = add_features_to_image(frame, people,{"age":age,"gender":gender})
            cv2.imshow('frame', image)
            # 0xFF is a hexadecimal constant which is 11111111 in binary.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def setDictionary(locations):
    people = list()
    areas = list()
    for face_location in locations:
        width = face_location[1]-face_location[3]
        height = face_location[2]-face_location[0]
        dictionary_of_features = {'faceId': None, 'faceRectangle': {'width': int(width), 'top': int(
            face_location[0]), 'height': int(height), 'left': int(face_location[3])}, 'faceAttributes': None}
        people.append(dictionary_of_features)
        areas.append(width*height)
    return people, areas


def add_features_to_image(frame, people, title):
    frame_size = frame.shape[0]*frame.shape[1]
    percent = []
    isInFront = False
    if people:
        font = cv2.FONT_HERSHEY_SIMPLEX
        props = setProps(people, frame_size)
        for prop in props:
            if props[0]['prop'] > 1:
                isInFront = True
                # Remarca la cara mayor
                cv2.rectangle(frame, props[0]['pi'],
                                props[0]['pf'], (0, 0, 255), 5)
            cv2.rectangle(frame, prop['pi'], prop['pf'], (0, 255, 0), 3)
            cv2.putText(frame, str(title["age"]), prop['pi'], font, 1, (255, 150, 0), 2, cv2.LINE_AA)

            cv2.rectangle(frame, (props[0]['pi'][0], props[0]['pf']
                                    [1]+50), (props[0]['pf']), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, str(title["gender"]), (props[0]['pi'][0]+10,props[0]['pf'][1]+30), font, 1, (255, 150, 0), 2, cv2.LINE_AA)
    return frame

def setProps(people, frame_size):
    props = []
    prop = 0
    for face_detected in people:
        pi = (face_detected['faceRectangle']['left'],
                face_detected['faceRectangle']['top'])
        pf = (face_detected['faceRectangle']['left']+face_detected['faceRectangle']['width'],
                face_detected['faceRectangle']['top']+face_detected['faceRectangle']['height'])
        prop = (face_detected['faceRectangle']['width']
                * face_detected['faceRectangle']['height'])
        # guarda el calculo de las proporciones en cada ciclo
        props.append({"pi": pi, "pf": pf, "prop": round(
            prop*100/float(frame_size), 4)})
    return props
if __name__ == "__main__":
    age_net, gender_net = load_caffe_models()
    getPrediction()
