from time import time
from resources import get_bucket

class Video(object):
    def __init__(self):
        self.frames = get_bucket()

    def get_frame(self):
        ext = int(time()) % 3
        key = 'b0' + str(ext) + '.jpeg'
        return self.frames.Object(key).get() 
