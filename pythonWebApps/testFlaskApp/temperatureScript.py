import math
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import firebase_admin
from firebase_admin import credentials, db



directory = "/home/pi/object-detection-tensorFlow-openData/"


def temperatureReading():
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus
    ads = ADS.ADS1015(i2c)
    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)
    ##print(chan.value, chan.voltage)
    # setting parameters
    TEMPERATURENOMINAL = 25
    BCOEFFICIENT = 3969
    THERMISTORNOMINAL = 10000
    # RESISTOR = 8740
    # RESISTOR = 5780
    # RESISTOR = 2890
    RESISTOR = 2700
    # Create differential input between channel 0 and 1
    # chan = AnalogIn(ads, ADS.P0, ADS.P1)
    # print("{:>5}\t{:>5}".format('raw', 'v'))
    counter = 0
    numberOfValues = 20
    values = []
    # while True:
    while not (counter == (numberOfValues + 1)):
        counter = counter + 1
        try:
            # 	Vout = Vin * (R2/R1+R1)
            # 	find resistance of thermistor using adc reading.  Simple resistor divider, solving for R1 using	  	R2 = 2890
            reading = ((1023 - chan.value)/1023)*4095
            # print(str(chan.value) + "  " + str(reading))
            resistor = (((4095.0) / (reading)) - 1) * RESISTOR
            # solve for temperature using 		1/T = (1/To) + (1/B)*ln(R/Ro)adc 1015
            # print ("resistor " + str(resistor))

            steinhart = resistor / THERMISTORNOMINAL
            steinhart = math.log(steinhart)
            steinhart = steinhart / BCOEFFICIENT
            steinhart = steinhart + (1 / (TEMPERATURENOMINAL + 273.15))
            steinhart = 1 / steinhart
            steinhart = steinhart - 273.15

            # print ("Every Iteration Output: " + str(steinhart))
            values.append(steinhart)

            if counter == numberOfValues:
                steinhart = 0
                for value in values:
                    steinhart = steinhart + value

                steinhart = steinhart / numberOfValues
                # print("The Average Value: " + str(steinhart) + " C")
                save2db(round(steinhart, 2))
                break
                values = []

        except:
            pass

        # print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
        time.sleep(0.5)


def connectAndCreateBlankCollectionAndDB(privateKeyPath):
    try:
        # realtime database connection setup variables
        cred = credentials.Certificate(privateKeyPath)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://engrlabs-10f0c.firebaseio.com/'})
        ref = db.reference('/')

    except ValueError:
        # realtime database connection setup variables
        ref = db.reference('/')
        # print ref.get()

    return ref


def save2db(temperature):
    privateKeyPath = (str(directory) + "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json")
    ref = connectAndCreateBlankCollectionAndDB(privateKeyPath)

    ref_B204DynamicData = ref.child('PUBLIC_DATA/DynamicData/B204')

    ref_B204DynamicData.update({
        u"Temperature": str(temperature)
    })

    # print("dbcalled")


# FIXME
# ### Testing only
temperatureReading()
