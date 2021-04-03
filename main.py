#Importing libs
import time
import busio
import board
import adafruit_ssd1306
import adafruit_bme280
import adafruit_pcf8523

#Switch for the clock blinking colon
switch = True

#Defining display pins
sda_oled = board.GP14
scl_oled = board.GP15

#Defining display objects
i2c_oled = busio.I2C(scl_oled, sda_oled)
oled = adafruit_ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c_oled)

#Defining sensor pins
sda_bme = board.GP16
scl_bme = board.GP17

#Defining RTC pins
sda_rtc = board.GP20
scl_rtc = board.GP21

#Main loop
while True:

    #Initiliazing BME-280 
    i2c_bme = busio.I2C(scl_bme, sda_bme)
    bme = adafruit_bme280.Adafruit_BME280_I2C(i2c_bme)
    #Formatting the temperature and rounding it 2 d.p. (e.g. 20.3 C => 20.30 C, 20.3456 C => 20.35 C)
    temp = "{:.2f}".format(bme.temperature)
    hum = "{:.2f}".format(bme.humidity)
    pres = "{:.2f}".format(bme.pressure)
    #Very important to deinit the I2C object or the bus can't be used
    i2c_bme.deinit()

    #Initiliazing RTC
    i2c_rtc = busio.I2C(scl_rtc, sda_rtc)
    rtc = adafruit_pcf8523.PCF8523(i2c_rtc)
    #Getting all the values
    hr = rtc.datetime.tm_hour
    min = rtc.datetime.tm_min
    sec = rtc.datetime.tm_sec
    yr = rtc.datetime.tm_year
    mon = rtc.datetime.tm_mon
    day = rtc.datetime.tm_mday

    #Check the string length and attach a zero in front of it if it's less than 2 (e.g. instead of 8:4 you get 08:40)
    if len(str(hr)) != 2:
        hr = "0" + str(hr)
    if len(str(min)) != 2:
        min = "0" + str(min)
    #Very important to deinit the I2C object or the bus can't be used
    i2c_rtc.deinit()


    oled.fill(0)
    oled.text("TempPi v0.2", 0, 0, 1)

    if switch:
        oled.text(str(hr) + ":" + str(min) + " BST " + str(mon) + "/" + str(day) + "/" + str(yr), 0, 10, 1)
        switch = False
    else:
        oled.text(str(hr) + " " + str(min) + " BST " + str(mon) + "/" + str(day) + "/" + str(yr), 0, 10, 1)
        switch = True

    oled.text("Temperature: " + str(temp) + " C", 0, 30, 1)
    oled.text("Pressure: " + str(pres) + " hPa", 0, 40, 1)
    oled.text("Humidity: " + str(hum) + " %", 0, 50, 1)
    oled.show()

    #Repeat in 1 second
    time.sleep(1)


    


    