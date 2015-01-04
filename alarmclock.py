__author__ = 'josephelliott'

import time
import datetime
from piglow import PiGlow


def wakeSequence(wakeSeconds,seconds):

    #begin the wake sequence

    #start with just the orange LEDs
    orangeStart = 0
    orangeRampDuration = wakeSeconds
    orangeRamp = orangeRampDuration/100 #power per second

    #The then yellow at 10 min
    yellowStart = (wakeSeconds*(1/3))
    yellowRampDuration = wakeTime - yellowStart
    yellowRamp = yellowRampDuration/100

    #then the white at 5 min
    whiteStart = (wakeSeconds*(2/3))
    whiteRampDuration = wakeTime - whiteStart
    whiteRamp = whiteRampDuration/100

    #end with all LEDs at 100.

    orangeBrightness = 0
    yellowBrightness = 0
    whiteBrightness = 0

    if orangeBrightness < 100 and seconds > orangeStart:
        orangeBrightness = orangeRamp*seconds

    if yellowBrightness < 100 and seconds > yellowStart:
        yellowBrightness = yellowRamp*seconds

    if whiteBrightness < 100 and seconds > whiteStart:
        whiteBrightness = whiteRamp*seconds

    piglow.orange(orangeBrightness)
    piglow.yellow(yellowBrightness)
    piglow.white(whiteBrightness)



#Run the script
piglow = PiGlow()

hours = 7
minutes = 0

#Takes 15 minutes to fully wake up
wakeDuration = datetime.timedelta(minutes=15)

#shut off after 10 min at full power
totalDuration = wakeDuration + datetime.timedelta(minutes=10)


try:
    while True:
        #set the wake time then enter the loop
        currentTime = datetime.datetime.now()

        wakeTime = currentTime.replace(hour=hours, minute=minutes)

        shutoffTime = wakeTime + totalDuration

        if currentTime > wakeTime and currentTime < shutoffTime:
            seconds = currentTime - wakeTime
            wakeSequence(wakeDuration.seconds, seconds.seconds)

        else:
            #shut off after 10 min at full power
            piglow.all(0)

        # sleep for a bit, don't go too fast!
        time.sleep(1)


except KeyboardInterrupt:
    # set all the LEDs to "off" when Ctrl+C is pressed before exiting
    piglow.all(0)