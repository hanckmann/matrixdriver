# MatrixDriver

MatrixDriver is a powerful Python API to control 8x8 RPI-RGB-LED-Matrix based on the 74HC595 chip. For more information on the hardware, see: [http://wiki.52pi.com/index.php/RPI-RGB-LED-Matrix_SKU:EP-0075](http://wiki.52pi.com/index.php/RPI-RGB-LED-Matrix_SKU:EP-0075)

*Note:* at this moment only 8x8 LED matrix displays are supported. It should be trivial to update the code to accomodate larger displays.

Development, updates, feature requests, etc. see [https://github.com/hanckmann/MatrixDriver](https://github.com/hanckmann/MatrixDriver). The Python code is tested on Python 3.x.


## API

    # import as follows:
    import matrixdriver.matrixdriver

The MatrixDriver class can be used to communicate with the LED matrix.

### Frame representation

This driver uses a frame representation per color channel (red, green, blue).
A color frame represents if the LED with the corresponding color is switched on.

The representation:

    frame = list, with object per LED column;
                  in which the object is a list of statusses per LED (in that column);
                  in which the status is represented by an integer;
                  in which an interger value of 0 represents to *not* switch on the LED.

Example:

    frame = [[1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 1, 0, 1, 0],
             [0, 1, 0, 0, 0, 1, 0, 1]]

    In this example frame the LEDs are alternately on and off.

Note that more examples of this representation can be seen when starting the driver directly. Starting the driver as a python application initiates the test mode and will print each frame to the screen.

### Send frame

Some example code to send a frame to the 8x8 LED matrix:

    # import
    import matrixdriver.matrixdriver
    # usage example
    md = matrixdriver.MatrixDriver(0, 0)
    empty_frame = [[1 for _ in range(8)] for _ in range(8)]
    alt_frame = [[1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 0, 0, 1, 0, 1, 0],
                 [0, 1, 0, 0, 0, 1, 0, 1]]
    md.frames(red=alt_frame, green=empty_frame, blue=empty_frame)
    md.draw(iterations=3)
    md.frames(red=empty_frame, green=alt_frame, blue=empty_frame)
    md.draw(iterations=3)
    md.frames(red=empty_frame, green=empty_frame, blue=alt_frame)
    md.draw(iterations=3)


The ColorGroup and WhiteGroup classes can be used to control groups of RGBW and White light bulbs and strips. It's interface is:

- ColorGroup and WhiteGroup
    + Group(ip_address, port=8899, pause=0.1, group_number=None)
    + on()
    + off()
- ColorGroup
    + white()
    + brightness(value=10)
    + disco(mode='')
    + increase_disco_speed(steps=1)
    + decrease_disco_speed(steps=1)
    + color(value)
- WhiteGroup
    + increase_brightness(steps=1)
    + decrease_brightness(steps=1)
    + increase_warmth(steps=1)
    + decrease_warmth(steps=1)
    + brightmode()
    + nightmode()

Note that when creating a group (__init__) the optional arguments 'port' and 'pause' should not be changed in normal operation.

The interface names should be self explanatory, except for:

*brightness(value=10):* sets the brightness of an RGBW lamp to a value between 0 and 25. Input values are rounded to the value closest within the range 0 to 25.

*disco(mode=''):* if no (valid) mode is selected: start the (next) preset disco mode of an RGBW lamp. A number of disco-modes can be started specifically by providing the mode name as argument.
Disco mode can be stopped by providing a color or setting the lamp into white mode.

- supported disco-modes:
    + color change
    + color fade
    + color blink
    + white blink
    + green blink
    + blue blink
    + red blink
    + rainbow
    + disco

*color(value):* sets the color of an RGBW lamp. The following are valid inputs:

- b'\x00' <= value <= b'\xFF', where type(value) == bytes
- 0 <= value <= 255, where type(value) == int
- a color name which can be found in the list below, where type(value) == str
    + violet
    + royalblue
    + lightskyblue
    + aqua
    + aquamarine
    + seagreen
    + green
    + limegreen
    + yellow
    + goldenrod
    + orange
    + red
    + pink
    + fuchsia
    + orchid
    + lavender

## MCI Parser (mci_parser.py)

    # import as follows:
    import mci.mci_parser

In this file two API's are defined:
- validate_command
- execute_command

The Parser makes it easier to connect and use the MiLight Control Interface from user provided input. It translates the textual arguments into commands. These commands are executed via the MiLight Control Interface.

An example project which uses the parser interface is MiLight-Web [https://github.com/hanckmann/MiLight-Web](https://github.com/hanckmann/MiLight-Web).

### validate_command

The validate_command function can be used to validate the provided textual arguments. It's interface is:

    mci.mci_parser.validate_command(bridge, bulb, group, action, value)

ToDo.

### execute_command

The execute_command function can be used to execute the provided textual arguments. It calls the validate_command function to validate the provided textual arguments.  It's interface is:

    mci.mci_parser.execute_command(bridge, bulb, group, action, value)

For more details on the function arguments see: validate_command.

## milight.py

Is the commandline utility which shows the MCI API. It can  be used as follows:

    milight.py [-h] [-s] [-i [ADDRESS]] [-p [PORT]] [-c RGBW] [-w WHITE]
               [-a ACTION] [--on] [--off] [--ew] [--br [ACTION_BR]]
               [--cc [ACTION_CC]] [--d] [--id] [--dd] [--ib] [--db] [--iw]
               [--dw] [--b] [--n]
    .
    optional arguments:
      -h, --help            show this help message and exit
      -s, --scan            Search wifi bridges.
      -i [ADDRESS], --ip_address [ADDRESS]
                            IP address.
      -p [PORT], --port [PORT]
                            Port number.
      -c RGBW, --rgbw RGBW  Set RGBW target group, default: None (1, 2, 3, 4, ALL)
      -w WHITE, --white WHITE
                            Set White target group, default: None (1, 2, 3, 4,
                            ALL)
      -a ACTION, --action ACTION
                            The desired action, default: None
                            (for white bulbs/strips: ON, OFF,
                                INC_BRIGHTNESS, DEC_BRIGHTNESS,
                                INC_WARMTH, DEC_WARMTH,
                                BRIGHT_MODE, NIGHT_MODE
                            for rgbw bulbs/strips: ON, OFF,
                                DISCO_MODE, INC_DISCO_SPEED, DEC_DISCO_SPEED)
      --on                  Action: ON
      --off                 Action: OFF
      --ew                  Action (rgbw bulbs/strips only): WHITE
      --br [ACTION_BR]      Action (rgbw bulbs/strips only): set brightness
                             (0<= value <= 25)
      --cc [ACTION_CC]      Action (rgbw bulbs/strips only): set color
                             (int: 0 <=value <= 255)
      --d                   Action (rgbw bulbs/strips only): DISCO_MODE
      --id                  Action (rgbw bulbs/strips only): INC_DISCO_SPEED
      --dd                  Action (rgbw bulbs/strips only): DEC_DISCO_SPEED
      --ib                  Action (white bulbs/strips only): INC_BRIGHTNESS
      --db                  Action (white bulbs/strips only): DEC_BRIGHTNESS
      --iw                  Action (white bulbs/strips only): INC_WARMTH
      --dw                  Action (white bulbs/strips only): DEC_WARMTH
      --b                   Action (white bulbs/strips only): BRIGHT_MODE
      --n                   Action (white bulbs/strips only): NIGHT_MODE

## milight2.py

Is a commandline utility which shows the parser API. It can  be used as follows:

    usage: milight2.py [-h] [-s] [-i ADDRESS] [-p PORT] [-c RGBW] [-w WHITE]
                       [-a [ACTION [ACTION ...]]] [--colors] [--disco_modes] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -s, --scan            Search wifi bridges.
      -i ADDRESS, --ip_address ADDRESS
                            IP address.
      -p PORT, --port PORT  Port number.
      -c RGBW, --rgbw RGBW  Set RGBW target group, default: None (1, 2, 3, 4,
                            ALL)
      -w WHITE, --white WHITE
                            Set White target group, default: None (1, 2, 3, 4,
                            ALL)
      -a [ACTION [ACTION ...]], --action [ACTION [ACTION ...]]
                            The desired action, default: None 
                            (for white bulbs/strips: 
                                ON, OFF, INC_BRIGHTNESS, DEC_BRIGHTNESS,
                                INC_WARMTH, DEC_WARMTH, BRIGHT_MODE, NIGHT_MODE
                            for rgbw bulbs/strips: 
                                ON, OFF, DISCO_MODE,
                                INC_DISCO_SPEED, DEC_DISCO_SPEED, as arguments
                            )
      --colors              Show supported colors
      --disco_modes         Show supported disco modes
      -v, --verbose         Show some (more) details of what is happening

## Finally

It would be great if you can use this for any of your projects, and I would be happy to hear how you used it.

Also feel free to bug me with update/bugfix/feature requests. I will add those if possible.

~~ Patrick
