import serial.tools.list_ports


def get_port():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    print(N)
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)

        print(strPort)
        if "Espressif Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = splitPort[0]
    return commPort


if get_port() != "None":
    ser = serial.Serial(port=get_port(), baudrate=115200)


def process_data(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("sensor3", splitData[2])
    elif splitData[1] == "H":
        client.publish("sensor1", splitData[2])
    elif splitData[1] == "L":
        client.publish("sensor2", splitData[2])


mess = ""


def read_serial(client):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            process_data(client, mess[start : end + 1])
            if end == len(mess):
                mess = ""
            else:
                mess = mess[end + 1 :]


def write_data(data):
    ser.write(str(data).encode())
