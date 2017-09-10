from PIL import Image
import os
import copy

try:
    # Import from egg
    import matrixdriver.matrixdriver
    print('Imported from egg')
except Exception:
    # Import from egg
    from driver.matrixdriver import matrixdriver
    print('Imported locally')


if __name__ == "__main__":
    subfolder = './images'
    filelist = [file for file in os.listdir(subfolder) if file.endswith('.png')]
    filelist.sort()
    md = matrixdriver.MatrixDriver(0, 0, debug=1)  # , spi_max_speed_hz=50000)
    size_x = 8
    size_y = 8
    for name in filelist:
        print(name)
        im = Image.open(subfolder + '/' + name)  # Can be many different formats
        width, height = im.size
        if not height == size_y and width >= size_x:
            print(' * skipping (image size should be 8x8)')
            continue
        rgb_im = im.convert('RGB')
        # Sliding window over wider images
        for index in range(width - size_x):
            empty_frame = [[1 for _ in range(size_x)] for _ in range(size_y)]
            red = copy.deepcopy(empty_frame)
            green = copy.deepcopy(empty_frame)
            blue = copy.deepcopy(empty_frame)
            for x in range(size_x):
                for y in range(size_y):
                    r, g, b = rgb_im.getpixel((index + x, y))
                    if r > 128:
                        red[x][y] = 0
                    if g > 128:
                        green[x][y] = 0
                    if b > 128:
                        blue[x][y] = 0
            # print('IMAGE')
            # matrixdriver.print_rgb(red, green, blue)
            md.frames(red=red, green=green, blue=blue)
            md.draw(iterations=50)
