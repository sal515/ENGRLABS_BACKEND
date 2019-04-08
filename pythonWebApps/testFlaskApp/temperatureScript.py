import math
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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
RESISTOR = 2550

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)
# print("{:>5}\t{:>5}".format('raw', 'v'))

counter = 0
numberOfValues = 20
values = []

while True:
    counter = counter + 1
    try:
        # 	Vout = Vin * (R2/R1+R1)
        # 	find resistance of thermistor using adc reading.  Simple resistor divider, solving for R1 using	  	R2 = 2890
        resistor = (((4095.0) / (chan.value)) - 1) * RESISTOR
        # solve for temperature using 		1/T = (1/To) + (1/B)*ln(R/Ro)

        # print ("resistor " + str(resistor))

        steinhart = resistor / THERMISTORNOMINAL
        steinhart = math.log(steinhart)
        steinhart = steinhart / BCOEFFICIENT
        steinhart = steinhart + (1 / (TEMPERATURENOMINAL + 273.15))
        steinhart = 1 / steinhart
        steinhart = steinhart - 273.15

        print ("Every Iteration Output: " + str(steinhart))
        values.append(steinhart)

        if counter == numberOfValues:
            steinhart = 0
            for value in values:
                steinhart = steinhart + value

            steinhart = steinhart / numberOfValues
            print("The Average Value: " + str(steinhart) + " C")
            values = []
    except:
        pass

    # print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)
