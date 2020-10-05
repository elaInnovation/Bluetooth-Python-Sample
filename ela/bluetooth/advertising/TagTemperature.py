from ela.bluetooth.advertising.TagBase import TagBase
import binascii

## 
# @class TagTemperature
# @brief tag temperature class to wrap data for ELA Temperature Tags  
class TagTemperature(TagBase):
    def __init__(self, payload):
        super().__init__(payload)
        self.formattedDataSensor = self.parsePaylaod(payload)
    
    def parsePaylaod(self, payload):
        result = ""
        ## implement parsing
        parse = binascii.b2a_hex(self.payload[0:32]).decode('ascii')  #parse en hexa
        T = int((parse[16:18] + parse[14:16]), 16)
        T = bin(T)
        T = T[2: len(T)]   #data binaire sur 12 ou 16 bit dont les 4 premiers déterminent le signe
        R = TagBase.integer(self, T)
        r = R / 100
        result = ("T= " + str(r))
        ## end of implement parsing
        return result
    