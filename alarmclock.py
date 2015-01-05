__author__ = 'josephelliott'

import time
import datetime
from piglow import PiGlow


def wakeSequence(wakeSeconds, seconds):

    #begin the wake sequence
    #start with just the orange LEDs
    orangeStart = 0
    orangeRampDuration = wakeSeconds
    orangeRamp = 255.0/orangeRampDuration #power per second

    #The then yellow at 10 min
    yellowStart = (wakeSeconds*(1/3.0))
    yellowRampDuration = wakeTime.second - yellowStart
    yellowRamp = 255.0/yellowRampDuration

    #then the white at 5 min
    whiteStart = (wakeSeconds*(2/3.0))
    whiteRampDuration = wakeTime.second - whiteStart
    whiteRamp = 255.0/whiteRampDuration


    if seconds >= orangeStart:
        orangeBrightness = int(orangeRamp*seconds)
        piglow.orange(orangeBrightness)

    if seconds >= yellowStart:

        yellowBrightness = int(yellowRamp*(seconds - (wakeSeconds - yellowRampDuration)))
        piglow.yellow(yellowBrightness)

    if seconds >= whiteStart:
        whiteBrightness = int(whiteRamp*(seconds - (wakeSeconds - whiteRampDuration)))
        piglow.white(whiteBrightness)



#Run the script
piglow = PiGlow()

hours = 1
minutes = 10

#Takes 15 minutes to fully wake up
wakeDuration = datetime.timedelta(minutes=15)

#shut off after 10 min at full power
totalDuration = wakeDuration + datetime.timedelta(minutes=10)


try:
    while True:
        #set the wake time then enter the loop
        currentTime = datetime.datetime.now()

        wakeTime = currentTime.replace(hour=hours, minute=minutes, second=0)

        shutoffTime = wakeTime + totalDuration

        if wakeTime < currentTime < shutoffTime:
            seconds = currentTime - wakeTime
            print("Wake sequence at %i seconds" % seconds.seconds)
            wakeSequence(wakeDuration.seconds, seconds.seconds)

        else:
            #shut off after 10 min at full power
            print("Sleeping...zzzzz")
            piglow.all(0)

        # sleep for a bit, don't go too fast!
        time.sleep(1)


except KeyboardInterrupt:
    # set all the LEDs to "off" when Ctrl+C is pressed before exiting
    piglow.all(0)