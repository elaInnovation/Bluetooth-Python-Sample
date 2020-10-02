from ela.bluetooth.TagBase import TagBase
import binascii

## 
# @class TagDI
# @brief tag Digital Input class to wrap data for ELA DI Tags
class TagDI(TagBase):
    def __init__(self, payload):
        super().__init__(payload)
        self.formattedDataSensor = self.parsePaylaod(payload)
    
    def parsePaylaod(self, payload):
        result = ""
        ## implement parsing
        parse = binascii.b2a_hex(self.payload[0:32]).decode('ascii')
        state = int(parse[16:18], 16)   
        count = int(parse[14:16], 16)
        result = ("DI state=" + str(state) + " count=" + str(count))
        ## end of implement parsing
        return result