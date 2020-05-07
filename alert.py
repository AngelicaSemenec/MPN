from resources import get_bucket

class Alert(object):
    def __init__(self, key):
        my_bucket = get_bucket()
        self.alert = my_bucket.Object(key)

    def get_alert(self):
        return

    def update_status(self):
        return
    
    def add_notes(self):
        return
