from ela.bluetooth.TagBase import TagBase
from ela.bluetooth.TagRHT import TagRHT
from ela.bluetooth.TagMag import TagMag
from ela.bluetooth.TagMov import TagMov
from ela.bluetooth.TagTemperature import TagTemperature
from ela.bluetooth.TagAng import TagAng
from ela.bluetooth.TagDI import TagDI
from ela.bluetooth.TagAI import TagAI
from ela.bluetooth.TagDO import TagDO
import binascii

## 
# Constant declaration to decode Bluetooth Advertising payload
# For more information about the frame format, please consult our website 
UUID_SERVICE_TEMPERATURE = "6e2a"
UUID_SERVICE_HUMIDITY = "6f2a"
UUID_SERVICE_MAG = "3f2a00"
UUID_SERVICE_MOV = "3f2a01"
UUID_SERVICE_ANG = "a12a"
UUID_SERVICE_DI = "3f2a02"
UUID_SERVICE_AI = "582a"
UUID_SERVICE_DO = "3f2a"
UUID_SERVICE_BAT = "0f18"

##
# @class Tagfactory 
# @brief tag factory to create tag object to decode data from Bluetooth advertising
class Tagfactory:
    __instance = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Tagfactory.__instance == None:
            Tagfactory()
        return Tagfactory.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if Tagfactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Tagfactory.__instance = self

    ##
    # @fn getTag
    # @brief getter on the tag object according to his payload 
    def getTag(self, payload):
        """ Getter on the target tag """
        tag = TagBase(payload)
        if( isinstance(payload, bytes)):
            tempString = binascii.b2a_hex(tag.payload).decode('ascii')
            if( (UUID_SERVICE_HUMIDITY in tempString) and (UUID_SERVICE_TEMPERATURE in tempString) ):
                print("Debug Tag RHT FOUND")
                tag = TagRHT(payload)
            elif( UUID_SERVICE_TEMPERATURE in tempString):
                print("Debug Tag Temperature FOUND")
                tag = TagTemperature(payload)
            elif( UUID_SERVICE_MAG in tempString):
                print("Debug Tag Mag FOUND")
                tag = TagMag(payload)
            elif( UUID_SERVICE_MOV in tempString):
                print("Debug Tag Mov FOUND")
                tag = TagMov(payload)
            elif( UUID_SERVICE_ANG in tempString):
                print("Debug Tag Ang FOUND")
                tag = TagAng(payload)
            elif( UUID_SERVICE_DI in tempString):
                print("Debug Tag DI FOUND")
                tag = TagDI(payload)
            elif( UUID_SERVICE_AI in tempString):
                print("Debug Tag AI  FOUND")
                tag = TagAI(payload)
            elif( UUID_SERVICE_DO in tempString):
                print("Debug Tag DO  FOUND")
                tag = TagDO(payload)
        return tag