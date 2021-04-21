import serial

# Indentify serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)

count = 0
while True:
    if ser.in_waiting > 0:
        count += 1

        # Read serial stream
        line = ser.readline()

        # avoid first n-line of serial information
        if count > 10:
            # setup serial stream of extra chars
            line = line.rstrip().lstrip()
            print(line)

            line = str(line)
            line = line.strip(',')
            line = line.strip("b'")
            print(line)

            # return float
            line = float(line)

            print(line, "\n")



