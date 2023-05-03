from .DataPacket import DataPacket
import datetime
import json
import os

class DataJSON(DataPacket):
    '''
      A DataPacket implementation that serializes its data to JSON, named according to the current time.
    '''

    def __init__(self,path):
        self.path = path
        super().__init__()
    def transmitData(self):
        filename = str(datetime.datetime.now()).replace(' ','-')
        with open(f'{self.path}/{filename}.json','w') as f:
            json.dump(self._dict(),f)

