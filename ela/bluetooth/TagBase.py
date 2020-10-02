import binascii

##
# @class TagBase  
# @brief base class to intergrate all informations from ELA tags
class TagBase:
    """ tag base declaration to contain all information to parse ELA BLE frame """
    formattedDataSensor = "VOID"
    formattedDataBattery = "VOID.."

    def __init__(self, payload):
        """ constructor / init """
        self.payload = payload
        #self.parsePaylaodBat(self.payload)

    def getRawData(self):
        """ getter on the raw data payload """
        return self.payload

    def bin2decs(self, data):
        """bin2decs(data): Conversion chaîne binaire signée de longueur quelconque -> nombre entier signé"""
        return int(data,2)-(1<<len(data))
            
    def integer(self, data):
        if len(data) == 16 and data[0] == "1":
            data = data[1:len(data)]
            data = TagBase.bin2decs(self, data)
            return data
        elif len(data) == 16 and data[0:4] == "1111":
            data = data[4:len(data)]
            data = TagBase.bin2decs(self, data)
            return data
        else:
            data = int(data,2)
            data = data
            return data

    def parsePaylaodBat(self, payload):
        result = ""
        ## implement parsing
        print(self.payload)
        parse = binascii.b2a_hex(self.payload).decode('ascii')  #parse en hexa+
        if "0f18" in parse:
            Bat = parse[len(parse)-6: len(parse)]
            if "0f18" in Bat:
                Bat = Bat[len(Bat)-2:len(Bat)]
                lvl_bat = int(Bat,16)
                result = lvl_bat
            else:
                pass
            ## fin implement parsing
            self.formattedDataBattery = result