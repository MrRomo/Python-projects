import face_recognition
import cv2



class NeuralClass:

    def __init__(self,frame):
        self.age_net, self.gender_net = self.load_caffe_models()

        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

        self.age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)','(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
        self.gender_list = ['Male', 'Female']
        self.frame = self.cropper(frame)

    def load_caffe_models(self):

        age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
        gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')
        return(age_net, gender_net)

    def genderClassifier(self):

        blob = cv2.dnn.blobFromImage(frame, 1, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        
        # Predict Gender
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = self.gender_list[gender_preds[0].argmax()]
        print(gender_preds)
        return gender

    def agePredictor(self):
        
        blob = cv2.dnn.blobFromImage(frame, 1, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        #Predict Age
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        print(age_preds)
        age = self.age_list[age_preds[0].argmax()]
        return age

    def cropper(self,batch):
        faces = list()
        for frame in batch:


neural = NeuralClass()

cap =  cv2.VideoCapture(0)
error, frame = cap.read()

print(neural.genderClassifier(frame))
print(neural.agePredictor(frame))
while 1:
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


