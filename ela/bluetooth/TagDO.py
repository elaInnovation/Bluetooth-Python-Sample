from ela.bluetooth.TagBase import TagBase
import binascii

## 
# @class TagDO
# @brief tag Digital Output class to wrap data for ELA DO Tags
class TagDO(TagBase):
    def __init__(self, payload):
        super().__init__(payload)
        self.formattedDataSensor = self.parsePaylaod(payload)
    
    def parsePaylaod(self, payload):
        result = ""
        ## implement parsing
        parse = binascii.b2a_hex(self.payload[0:32]).decode('ascii')
        data = int(parse[14:16], 16)
        result = ("DO= " + str(data))
        ## end of implement parsing
        return result