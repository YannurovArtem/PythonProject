from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import cv2

face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class Test(MDApp):
    def build(self):
        self.Flayout = FloatLayout()
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.capture = cv2.VideoCapture(1)
        self.image = Image()
        self.GlassImage = Image(source="glass3.png", size_hint=(.25, .35))
        Clock.schedule_interval(self.Video, 1.0/60.0)
        self.Flayout.add_widget(self.image)
        self.Flayout.add_widget(self.GlassImage)
        return self.Flayout

    def Video(self, *args):
        ret, frame = self.capture.read()
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 0)
            self.GlassImage.size_hint = (float(w / 630), float(h / 630))
            a = 425-int(y)

            print(w, x, y, a)
            self.GlassImage.pos = (int(x)+60, int(a))
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
        self.image.texture = texture


if __name__ == "__main__":
    Test().run()