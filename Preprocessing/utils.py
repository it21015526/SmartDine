from threading import Thread


# to import the video feed in a separate thread
class VideoGet:
    def __init__(self):
        # self.stream = cv2.VideoCapture('rtsp://admin:OIT@12345@192.168.118.5')
        self.stream = cv2.VideoCapture('real_shanilka_1.mp4')
        self.ret, self.frame = self.stream.read()
        # print("getting frame : ", self.ret)
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.ret:
                self.stop()
            else:
                (self.ret, self.frame) = self.stream.read()
                # print('this is from the inside: ', self.ret)

    def stop(self):
        self.stopped = True


# to complete the label shown in the image
def complete_label(class_name):
    return class_name
