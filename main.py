#Importing libs
from utime import gmtime, sleep_ms
from machine import Pin, I2C
import ssd1306
import BME280


#Defining display pins
sda_oled = Pin(14)
scl_oled = Pin(15)

#Defining display objects
i2c_oled = I2C(1, sda=sda_oled, scl=scl_oled, freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c=i2c_oled)

#Defining sensor pins
sda_bme = Pin(16)
scl_bme = Pin(17)

#Defining sensor objects
i2c_bme = I2C(0, sda=sda_bme, scl=scl_bme, freq=200000)
bme = BME280.BME280(i2c=i2c_bme)

#Main loop
while True:
    #Clear the display every iteration
    oled.fill(0)

    #Read values from the sensors
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure

    #Uncomment for debug
    #print("Temperature: ", temp)
    #print("Pressure: ", pres)
    #print("Humidity: ", hum)

    #Output to the display
    oled.text("TempPi v0.1", 0, 0)
    oled.text("T: " + str(temp), 0, 15)
    oled.text("P: " + str(pres), 0, 30)
    oled.text("H: " + str(hum), 0, 45)
    oled.show()

    #Repeat in 1 second
    sleep_ms(1000)