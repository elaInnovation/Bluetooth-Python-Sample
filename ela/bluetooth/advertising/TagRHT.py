from ela.bluetooth.advertising.TagBase import TagBase
import binascii

## 
# @class TagRHT
# @brief tag Relative humidity and temperature class to wrap data for ELA RHT Tags
class TagRHT(TagBase):
    def __init__(self, payload):
        super().__init__(payload)
        self.formattedDataSensor = self.parsePaylaod(payload)
    
    def parsePaylaod(self, payload):
        result = ""
        ## implement parsing
        parse = binascii.b2a_hex(self.payload[0:32]).decode('ascii')
        T = int((parse[16:18] + parse[14:16]), 16)
        T = bin(T)
        T = T[2: len(T)]   #data binaire sur 12 ou 16 bit dont les 4 premiers déterminent le signe
        R = TagBase.integer(self, T)
        temperature = R / 100
        humidity = int(parse[26:28], 16)
        result = ("T=" + str(temperature) + " RH=" + str(humidity))
        ## end of implement parsing
        return result