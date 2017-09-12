# MatrixDriver

MatrixDriver is a powerful Python API to control 8x8 RPI-RGB-LED-Matrix based on the 74HC595 chip. For more information on the hardware, see: [http://wiki.52pi.com/index.php/RPI-RGB-LED-Matrix_SKU:EP-0075](http://wiki.52pi.com/index.php/RPI-RGB-LED-Matrix_SKU:EP-0075)

*Note:* at this moment only 8x8 LED matrix displays are supported. It should be trivial to update the code to accomodate larger displays.

Development, updates, feature requests, etc. see [https://github.com/hanckmann/MatrixDriver](https://github.com/hanckmann/MatrixDriver). The Python code is tested on Python 3.x.


## API

    # import as follows:
    import matrixdriver.matrixdriver

The MatrixDriver class can be used to communicate with the LED matrix.

Make sure you have installed the dependencies:

    pip install -r requirements.txt


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
    from matrixdriver import matrixdriver
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


## Example application imagedriver.py

The example application reads all images from the images folder and will try to show these on the matrix. To get the example application working:

    $ pip install -r requirements
    $ python3 imagedriver.py


## Finally

It would be great if you can use this for any of your projects, and I would be happy to hear how you used it.

Also feel free to bug me with update/bugfix/feature requests. I will add those if possible.

~~ Patrick
