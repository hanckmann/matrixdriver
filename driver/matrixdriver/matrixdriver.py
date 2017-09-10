# rm matrixdriver.py; nano matrixdriver.py; python matrixdriver.py
import spidev
import time
import copy


def set_bit(index: int, value: int=0x00) -> int:
    """
    Set the bit on index to one.

    Parameters
    ----------
    index : int
        The index of the bit to set to one
    value : int
        The initial byte (as int) in which to set the index bit to one (default=0x00)

    Returns
    -------
    int
        The changed value (with the set bit)
    """
    return value | (1 << index)


def clear_bit(index: int, value: int=0x00) -> int:
    """
    Set the bit on index to zero.

    Parameters
    ----------
    index : int
        The index of the bit to set to zero
    value : int
        The initial byte (as int) in which to set the index bit to zero (default=0x00)

    Returns
    -------
    int
        The changed value (with the cleared bit)
    """
    return value & ~(1 << index)


def set_bits_from_list(sequence: list) -> int:
    """
    Set the bits asprovided in the sequence list.

    Parameters
    ----------
    sequence : list
        A list of integers representing the binary sequence of a byte (represented by an int)

    Returns
    -------
    int
        The created value as represented by the sequence
    """
    value = 0xFF
    for index, bit in enumerate(sequence):
        if not bit:
            value = clear_bit(index, value)
    return value


def get_bit(value: int, index: int) -> int:
    """
    Get the bit on index.

    Parameters
    ----------
    index : int
        The index of the bit to get
    value : int
        The value of the byte (represented by an int) from which to get the index bit

    Returns
    -------
    int
        The changed value (with the set bit)
    """
    return ((value & (1 << index)) != 0)


def get_bits_as_list(value: int) -> list:
    """
    Get the bits as list.

    Parameters
    ----------
    value : int
        The value of the byte (represented by an int) from which to get the binary sequence

    Returns
    -------
    list
        A list of integers representing the binary sequence of a byte
    """
    bits = [0, 0, 0, 0, 0, 0, 0, 0]
    for index in range(8):
        if get_bit(value, index):
            bits[index] = 1
    return bits


def decode_stream(writebytes: list) -> tuple:
    """
    Decode the spi->writebytes data to the frame representation.

    *Note* that the input color order is different from the output color order (see below).

    Parameters
    ----------
    writebytes : list
        The list of integers as send via spi->writebytes (==[red: int, blue: int, green: int, column:int])

    Returns
    -------
    tuple
        A tuple with the frame representation per color in the order red, green, blue
    """
    red = get_bits_as_list(writebytes[0])
    green = get_bits_as_list(writebytes[1])
    blue = get_bits_as_list(writebytes[2])
    column = get_bits_as_list(writebytes[3])
    empty_frame = [[2 for _ in range(8)] for _ in range(8)]
    frame_red = copy.deepcopy(empty_frame)
    frame_green = copy.deepcopy(empty_frame)
    frame_blue = copy.deepcopy(empty_frame)
    # Check which column we are working on
    for x_index, x_bit in enumerate(column):
        if x_bit:
            # Check which LED we are working on
            for y_index, y_bit in enumerate(red):
                frame_red[x_index][y_index] = y_bit
            for y_index, y_bit in enumerate(green):
                frame_green[x_index][y_index] = y_bit
            for y_index, y_bit in enumerate(blue):
                frame_blue[x_index][y_index] = y_bit

    return (frame_red, frame_green, frame_blue)


def print_rgb(red: list, green: list, blue: list, mirror=True) -> None:
    """
    Print the RGB frames to screen

    Parameters
    ----------
    red : list
        A frame representation of the matrix representing the red color
    green: list
        See red
    blue: list
        See red

    Returns
    -------
    None
    """
    print(' RED:                        GREEN:                      BLUE:')
    print('+----------------------+    +----------------------+    +----------------------+')
    for x in range(8):
        print('{red}    {green}    {blue}'.format(red=str(red[7 - x]), green=str(green[7 - x]), blue=str(blue[7 - x])))
    print('+----------------------+    +----------------------+    +----------------------+')


class MatrixDriver(object):
    """
    Driver for the 8x8 RPI-RGB-LED-Matrix based on the 74HC595 chip.

    *See:* http://wiki.52pi.com/index.php/RPI-RGB-LED-Matrix_SKU:EP-0075

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

    Note that more examples of this representation can be seen when starting the driver directly. Starting the driver directly initiates the test mode and will print each frame to the screen.

    *Note:* at this moment only 8x8 LED matrix displays are supported. It should be trivial to update the code to accomodate larger displays.
    """

    def __init__(self, bus: int, device: int, spi_max_speed_hz: int=None, debug: int=0) -> None:
        """
        Initialisation

        Parameters
        ----------
        bus : int
            The bus value to make the connection with (see py-spidev: https://github.com/doceme/py-spidev)
        device : int
            The device value to make the connection with (see py-spidev: https://github.com/doceme/py-spidev)
        spi_max_speed_hz : int
            The max spi update speed (default=None) (see py-spidev: https://github.com/doceme/py-spidev)
        debug : int
            Debug status (default=0). If set to >0, each frame will be printed to screen (verbose). If set to >1, each spi write will be printed to screen (very verbose).

        Returns
        -------
        None
        """
        self.spi = spidev.SpiDev()
        self.bus = bus
        self.device = device
        self.spi_max_speed_hz = spi_max_speed_hz
        empty_frame = [[1 for _ in range(8)] for _ in range(8)]
        self.frame_red = copy.deepcopy(empty_frame)
        self.frame_green = copy.deepcopy(empty_frame)
        self.frame_blue = copy.deepcopy(empty_frame)
        self.debug = debug

    def draw(self, iterations: int=1) -> None:
        """
        Draw the current RGB frames to the LED matrix.

        Parameters
        ----------
        iterations : int
            The number of repetitions for reprinting the RGB frame.

        Returns
        -------
        None
        """
        try:
            self.spi.open(self.bus, self.device)
            if self.spi_max_speed_hz and self.spi_max_speed_hz > 0:
                self.spi.max_speed_hz = self.spi_max_speed_hz
            for i in range(iterations):
                # This is iteration i
                for line in range(8):
                    red = set_bits_from_list(self.frame_red[line])
                    green = set_bits_from_list(self.frame_green[line])
                    blue = set_bits_from_list(self.frame_blue[line])
                    column = set_bit(line)
                    if not column:
                        continue
                    if red == 255 and green == 255 and blue == 255:
                        continue
                    self.spi.writebytes([red, blue, green, column])  # Actually wants to have RBG
                    if self.debug > 1:
                        print('COLUMN')
                        print("column={0:8b} \t red={1:8b} \t green={2:8b} \t blue={3:8b}".format(column, red, green, blue))
                        print_rgb(*decode_stream([red, blue, green, column]))
                    time.sleep(0.002)
        except Exception:
            raise
        finally:
            self.spi.close()

    def frames(self, red: list, green: list, blue: list, mirror=True) -> None:
        """
        Set a new set of RGB frames.

        Parameters
        ----------
        red : list
            A frame representation of the matrix representing the red color
        green: list
            See red
        blue: list
            See red

        Returns
        -------
        None
        """
        if mirror:
            old_red = copy.deepcopy(red)
            old_green = copy.deepcopy(green)
            old_blue = copy.deepcopy(blue)
            for index in range(8):
                red[index] = old_red[7 - index]
                green[index] = old_green[7 - index]
                blue[index] = old_blue[7 - index]
        self.frame_red = red
        self.frame_green = green
        self.frame_blue = blue
        if self.debug > 0:
            print('FRAME')
            print_rgb(self.frame_red, self.frame_green, self.frame_blue)


if __name__ == "__main__":
    md = MatrixDriver(0, 0, debug=1)
    empty_frame = [[1 for _ in range(8)] for _ in range(8)]
    iterations = 2
    print('Testing the driver and the LED matrix. Infinite loop.')
    while(1):
        print('Sequence of RED LEDs.')
        for x in range(8):
            for y in range(8):
                frame = [[1 for _ in range(8)] for _ in range(8)]
                frame[x][y] = 0
                md.frames(red=frame, green=empty_frame, blue=empty_frame)
                md.draw(iterations=iterations)
        print('Sequence of RED LEDs.')
        for x in range(8):
            for y in range(8):
                frame = [[1 for _ in range(8)] for _ in range(8)]
                frame[x][y] = 0
                md.frames(red=empty_frame, green=frame, blue=empty_frame)
                md.draw(iterations=iterations)
        print('Sequence of RED LEDs.')
        for x in range(8):
            for y in range(8):
                frame = [[1 for _ in range(8)] for _ in range(8)]
                frame[x][y] = 0
                md.frames(red=empty_frame, green=empty_frame, blue=frame)
                md.draw(iterations=iterations)
