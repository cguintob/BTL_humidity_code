OVERVIEW

This is a side-project of the BTL research and development project. The aim is
to measure the relative humidity and temperature in the assembly rooms where
sensor modules are being built and QA/QCed to understand better the environment
in which they're being built.

We use an Arduino circuit with a humidity and temperature sensor to gather the
data. The Arduino code is written in C++ and, once run, sends its data to a
script written in Python, which receives the data from the Arduino and organizes
it into a text file. Then, we use another Python script to graph the data.

This repository contains a few data files, the Python scripts, as well as the
Arduino code. Everything is run in a Linux terminal (except for the Arduino
code, which is run in the Arduino processor), using the commands

python sensorData.py\n
python dataReader.py