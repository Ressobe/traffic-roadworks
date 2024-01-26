from time import sleep
from random import randint
from queue import Queue
import platform
import threading
import os

system_type = platform.system()
globalLock = threading.Lock()
screenLock = threading.Lock()
car_id = 1

north_duration = float(input("Enter the duration for light north traffic (seconds), or press Enter (default 3s): ").strip() or 3)
south_duration = float(input("Enter the duration for light south traffic (seconds), or press Enter (default 3s): ").strip() or 3)
amount_of_cars = float(input("Enter the number of cars, or press Enter (default 20): ").strip() or 20)

current_traffic_light = "North"
file_name = "logi.txt"
plik_logi = open(file_name, 'w')



class Line():
    def __init__(self, capacity, direction):
        self.mutex = threading.Semaphore()
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.finished = False
        self.line = Queue()
        self.direction = direction

    def put(self, item):
        self.empty.acquire()
        self.mutex.acquire()

        self.line.put(item)

        self.mutex.release()
        self.full.release()

    def get(self):
        self.full.acquire()
        self.mutex.acquire()

        item = self.line.get()

        self.mutex.release()
        self.empty.release()
        return item

    def getQueue(self):
        return list(self.line.queue)

    def isQueueEmpty(self):
        with self.mutex:
            return self.line.empty()

    def end(self):
        return self.finished and self.isQueueEmpty()


def printTrafficInfo(current_direction, north_line, south_line):
    with screenLock:
        if system_type == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        print(f"\nCurrent Traffic Light: {current_direction}")
        print(f"North line: {north_line.getQueue()}")
        print(f"South line: {south_line.getQueue()}")


def northLineProducer(north_line, south_line):
    global car_id
    global current_traffic_light


    while car_id <= amount_of_cars:

        with globalLock:
            car = car_id
            north_line.put(f"N-{car}")
            printTrafficInfo(current_traffic_light, north_line, south_line)
            plik_logi.write(f"North traffic: Car N-{car} has entered\n")
            car_id += 1

        sleep(randint(1, 4))

    with north_line.mutex:
        north_line.finished = True
        north_line.empty.release()    


def southLineProducer(south_line, north_line):
    global car_id
    global current_traffic_light

    sleep(0.5)
    while car_id <= amount_of_cars:

        with globalLock:
            car = car_id
            south_line.put(f"S-{car}")
            printTrafficInfo(current_traffic_light, north_line, south_line)
            plik_logi.write(f"South traffic: Car S-{car} has entered\n")
            car_id += 1

        sleep(randint(1, 4))

    with south_line.mutex:
        south_line.finished = True
        south_line.empty.release() 


def trafficLightConsumer(north_line, south_line, light_north, ligth_south):
    global current_traffic_light
    sleep(1)

    while True:
        cars = []

        while not north_line.isQueueEmpty():

            car = north_line.get()
            plik_logi.write(f"North traffic: Car {car} has exited road\n")
            cars.append(car)

        sleep(light_north)

        with globalLock:
            if cars:
                current_traffic_light = "South"
                printTrafficInfo(current_traffic_light, north_line, south_line)


        cars = []

        while not south_line.isQueueEmpty():
            car = south_line.get()
            plik_logi.write(f"South traffic: Car {car} has exited road\n")
            cars.append(car)

        sleep(ligth_south)

        with globalLock:
            if cars:
                current_traffic_light = "North"
                printTrafficInfo(current_traffic_light, north_line, south_line)


        if north_line.end() and south_line.end():
            break


def main():
    if amount_of_cars > 0:
        northLine = Line(amount_of_cars, 'north')
        southLine = Line(amount_of_cars, 'south')

        northSideThread = threading.Thread(target=northLineProducer, args=(northLine, southLine))
        southSideThread = threading.Thread(target=southLineProducer, args=(southLine, northLine))

        trafficLightThread = threading.Thread(target=trafficLightConsumer, args=(northLine, southLine, north_duration, south_duration))

        northSideThread.start()
        southSideThread.start()
        trafficLightThread.start()

        northSideThread.join()
        southSideThread.join()
        trafficLightThread.join()


if __name__ == '__main__':
    main()

plik_logi.close()
