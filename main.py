
__author__ = 'Marcelo dos Santos'
__version__ = '1.0'
__app__ = 'IP Cam with Python and Kivy'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class PageInitial(Screen):
    def __init__(self):
        super().__init__(name='initial')
        self.box = BoxLayout()
        self.button = Button(text='Start server...')
        self.box.add_widget(self.button)
        self.add_widget(self.box)
        
class PageCam(Screen):
    def __init__(self):
        super().__init__(name='cam')
        self.box = BoxLayout(orientation='vertical')
        self.button = Button(text='Page Cam...')
        self.camera = self.image()
        self.box.add_widget(self.camera)
        #self.video = Video(source='20180304_014208.mp4')
        #self.add_widget(self.video)
        self.box.add_widget(self.button)
        self.add_widget(self.box)

    def image(self):
        self.img1 = Image(source='logoCL.jpg')
        layout = BoxLayout()
        layout.add_widget(self.img1)  
        self.capture = cv2.VideoCapture(0)  #criamos um objeto de capture de vídeo. Associamos à primeira camera
        ret, frame = self.capture.read() 
        Clock.schedule_interval(self.atualizaImagem, 1.0/30.0) 
        return layout
  
    def atualizaImagem(self, dt):
        ret, frame = self.capture.read()   #captura uma imagem da camera
         
        buf1 = cv2.flip(frame, 0)   #inverte para não ficar de cabeça para baixo
        buf = buf1.tostring() # converte em textura
         
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
         
        self.img1.texture = texture1 #apresenta a imagem

class Manager(ScreenManager):
    def __init__(self):
        super().__init__()
        obj_page_initial = PageInitial()
        obj_page_cam = PageCam()
        self.add_widget(obj_page_initial)
        self.add_widget(obj_page_cam)
        obj_page_initial.button.bind(on_press=self.page_cam)
        obj_page_cam.button.bind(on_press=self.page_initial)
        
    def page_cam(self, button):
        self.current = 'cam'

    def page_initial(self, button):
        self.current = 'initial'

class Main(App):

    def build(self):
        #self.icon = 'name_img.jpg' #definindo o icone do app
        return Manager()

if __name__ == '__main__':

    Main().run()

