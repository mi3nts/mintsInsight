import serial

class Cozir(object):
    verbosity = 1   # level of information printed to terminal
    def __init__(self, port, verbosity=1):
        self.ser = serial.Serial(port, timeout=1)
        self.verbosity = verbosity
        if verbosity >= 1:
            print('connected to "{}"'.format(port))
        
    def write(self, com):
        '''write the command `com` (bytes) followed by "\\r\\n"'''
        if verbosity >= 2:
            print('writing "{}"'.format(com))
        self.ser.write(com + b'\r\n')
    
    def readCO2(self, with_filter=True):
        '''CO2 concentration in ppm
        
        with or without the digital smoothing filter
        
        note: the multiplier is *not implemented*.
        
        (Z or z command)
        '''
        if with_filter:
            com = b'Z'
        else:
            com = b'z'
        self.write(com)
        
        res = self.ser.readline().strip()
        assert res.startswith(com + b' ')
        res = float(res[2:])
        
        return res

    def readTemperature(self):
        '''temperature in degrees Celsius
        
        (T command)
        '''
        self.write(b'T')
        res = self.ser.readline().strip()
        assert res.startswith(b'T ')
        res = (float(res[2:]) - 1000)/10.
        return res
    
    def readHumidity(self):
        '''relative humidity in %
        
        (H command)
        '''
        self.write(b'H')
        res = self.ser.readline().strip()
        assert res.startswith(b'H ')
        res = float(res[2:])/10.
        return res