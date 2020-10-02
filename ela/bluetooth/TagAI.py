from ela.bluetooth.TagBase import TagBase
import binascii

## 
# @class TagAI
# @brief tag Analog Input class to wrap data for ELA AI Tags
class TagAI(TagBase):
    def __init__(self, payload):
        super().__init__(payload)
        self.formattedDataSensor = self.parsePaylaod(payload)
    
    def parsePaylaod(self, payload):
        result = ""
        ## implement parsing
        parse = binascii.b2a_hex(self.payload[0:32]).decode('ascii')
        data = int((parse[16:18] + parse[14:16]), 16)
        result = ("AI= " + str(data))
        ## end of implement parsing
        return result