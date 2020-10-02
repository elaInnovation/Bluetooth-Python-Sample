from ela.bluetooth.TagBase import TagBase
import binascii

## 
# @class TagAng
# @brief tag Angular class to wrap data for ELA ANG Tags
class TagAng(TagBase):
    def __init__(self, payload):
        super().__init__(payload)
        self.formattedDataSensor = self.parsePaylaod(payload)
    
    def parsePaylaod(self, payload):
        result = ""
        ## implement parsing
        parse = binascii.b2a_hex(self.payload[0:32]).decode('ascii')
        X_int=int((parse[16:18] + parse[14:16]),16)
        Y_int=int((parse[20:22] + parse[18:20]),16)
        Z_int=int((parse[24:26] + parse[22:24]),16)
        X =str(bin(X_int))
        Y = str(bin(Y_int))
        Z =str(bin(Z_int))
        axe_X = (TagBase.integer(self, X[2: len(X)]))
        axe_Y = (TagBase.integer(self, Y[2: len(Y)]))
        axe_Z = (TagBase.integer(self, Z[2: len(Z)]))
        result = (" axe X=" + str(axe_X) + "  Y=" + str(axe_Y) + "  Z=" + str(axe_Z))
        ## end of implement parsing
        return result