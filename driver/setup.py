from setuptools import setup, find_packages
import sys
import os

version = '0.9.0'

setup(name='matrixdriver',
      version=version,
      description='Driver for the 8x8 RPI-RGB-LED-Matrix based on the 74HC595 chip.',
      long_description='''MatrixDriver is a powerful Python API to control 8x8 RPI-RGB-LED-Matrix based on the 74HC595 chip. For more information on the hardware, see: http://wiki.52pi.com/index.php/RPI-RGB-LED-Matrix_SKU:EP-0075''',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Other Audience',
          'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Home Automation',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: System :: Hardware :: Hardware Drivers'
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='driver 8x8 led-matrix led matrix 74hc595 chip',
      author='Patrick Hanckmann',
      author_email='hanckmann@gmail.com',
      url='https://hanckmann.com',
      license='GNU Lesser General Public License v2 (LGPLv2)',
      packages=find_packages(exclude=['ez_setup']),
      python_requires='>=3',
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'spidev'
      ],
      entry_points='''
      # -*- Entry points: -*-
      ''',
      )
