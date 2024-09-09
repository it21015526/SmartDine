import torch
# import libraries
import joblib
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from computer_vision.utils import *
import torch.nn.functional as F
import time


class Net(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(300, 300, bias=True)
        self.fc2 = torch.nn.Linear(300, 300, bias=True)
        self.out = torch.nn.Linear(300, 4) # activity classes: eating, ordering, requsting_bill, paying_bill

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.out(x))
        return x


def Inference():
    # loading the trained model
    model = Net()
    model.load_state_dict(torch.load('model.pt'))
    #  loading label encoder configuration
    with open('./models/label_encoder.sav', 'rb') as f:
        label_encoder = joblib.load(f)
    # media pipe drawing tools
    mpDraw = mp.solutions.drawing_utils
    mpHolistic = mp.solutions.holistic
    with mpHolistic.Holistic(min_tracking_confidence=0.5, min_detection_confidence=0.5) as holistic:
        video_getter = VideoGet().start()
        while True:
            # reading frames
            frame = video_getter.frame
            # print("this is from outside : ", ret)
            # setup resolution
            image = cv2.resize(frame, (680, 480))
            # for mediapipe color conversion is essential
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # for better performance media pipe suggest this
            image.flags.writeable = False
            # key points extraction
            results = holistic.process(image)
            # enable write permission
            image.flags.writeable = True
            # change the color back to cv2
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # drawing key points and connections
            mpDraw.draw_landmarks(image, results.face_landmarks, mpHolistic.FACEMESH_TESSELATION,
                                  landmark_drawing_spec=DrawingSpec(color=(30, 144, 255), circle_radius=1),
                                  connection_drawing_spec=DrawingSpec(color=(255, 255, 255), thickness=1))
            mpDraw.draw_landmarks(image, results.right_hand_landmarks, mpHolistic.HAND_CONNECTIONS,
                                  landmark_drawing_spec=DrawingSpec(color=(30, 144, 255), circle_radius=1),
                                  connection_drawing_spec=DrawingSpec(color=(255, 255, 255), thickness=1))
            mpDraw.draw_landmarks(image, results.left_hand_landmarks, mpHolistic.HAND_CONNECTIONS,
                                  landmark_drawing_spec=DrawingSpec(color=(30, 144, 255), circle_radius=1),
                                  connection_drawing_spec=DrawingSpec(color=(255, 255, 255), thickness=1))
            mpDraw.draw_landmarks(image, results.pose_landmarks, mpHolistic.POSE_CONNECTIONS,
                                  landmark_drawing_spec=DrawingSpec(color=(30, 144, 255), circle_radius=1),
                                  connection_drawing_spec=DrawingSpec(color=(255, 255, 255), thickness=1))
            # if any landmark type is invisible the code will throw an error. better bypass it
            # extracting key points values
            if results.pose_landmarks is not None:
                pose = results.pose_landmarks.landmark
                pose_row = list(np.array(
                    [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            else:
                pose_row = [x for x in np.zeros(132)]

            if results.right_hand_landmarks is not None:
                right_hand = results.right_hand_landmarks.landmark
                right_hand_row = list(np.array(
                    [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                     right_hand]).flatten())
            else:
                right_hand_row = [x for x in np.zeros(84)]
            if results.left_hand_landmarks is not None:
                left_hand = results.left_hand_landmarks.landmark
                left_hand_row = list(np.array(
                    [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                     left_hand]).flatten())
            else:
                left_hand_row = [x for x in np.zeros(84)]
            # concatenate all key points
            row = pose_row + right_hand_row + left_hand_row
            # add a dimension to match input to the model
            row = np.array(row).reshape(1, -1)
            # predict
            model.eval()
            y_hat = model(torch.from_numpy(np.float32(row)))
            # 'test after this point'
            # '=========================================================================================='
            # decoding the label
            y_hat = np.argmax(y_hat.cpu().detach().numpy())
            y_hat = [y_hat]
            label = label_encoder.inverse_transform(y_hat)

            # image = fall_alert_detection(image, label, results.pose_landmarks)
            print(label)
            label = complete_label(label[0])

            # display the feed
            cv2.putText(image, str(label),
                        (95, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('image', image)

            if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
                video_getter.stop()
                break


Inference()
