# -*-coding:utf-8-*-

# подключение необходимых библиотек
import serial
import time

ser = serial.Serial("/dev/ttyUSB3", 9600)  # инициализация сериал порта(связь с ардуино)
ser.baudrate = 9600  # скорость чтения данных с порта

# дистанция
distance = {'front': 0, 'right': 0, 'left': 0}

# Переменная для записи значения взависимости ,от которого коптер будет лететь в ту или иную сторону
side = {'left': 0, 'right': 0, 'front': 0}

fly_side = 0

volume_check = ""

flag = True
ident = False

def write_read(number, words=1, timesleep=0.5):
    if number == 0:
        ser.write(bytes(words))
        time.sleep(timesleep)
    elif number == 1:
        return ser.readline()


def get_direction(symbol):
    volume_check = write_read(1)
    if volume_check[0] == symbol:
        print(int(volume_check[1:]))
        return int(volume_check[1:])


def check_distance(value):
    if value != 0 and value != 357:
        return True


def fly():
    statement = True
    while statement:
        if set_orintation(b"1", "f"):
            print('Полетели вперед')
        elif set_orintation(b"2", "r"):
            print('Полетели вперед')
        elif set_orintation(b"3", "l"):
            print('Полетели вправо')
        else:
            statement = False
            print('Чет не летим')

# def choise_of_direction():
#     write_read(0, b"2")
#     flag = 0
#     while True:
#         if check_distance(value1) and flag == 0:
#             flag = 1
#         elif flag == 0:
#             value1 = get_direction("r")
#
#         if check_distance(value2) and flag == 1:
#             flag = 2
#         elif flag == 1:
#             value2 = get_direction("l")
#
#         if flag == 2:
#             if value1 > value2:
#                 value_direction = 1
#             else:
#                 value_direction = 2
#             flag = 3
#
#         if flag == 3:
#             fly(value_direction)


def stopSend():
    state = False
    write_read(0, b"4")
    print("stop")
    return state


def set_orintation(word, char):
    write_read(0, word)
    global flag
    global ident
    ident = bool(ident)
    while flag:
        value = get_direction(char)
        if check_distance(value):
            if value <= 100:
                flag = stopSend()
                ident = False
                break
            else:
                print("fly")
                ident = True
        else:
            print("датчик врёт")
            ident = False

    return ident

fly()
