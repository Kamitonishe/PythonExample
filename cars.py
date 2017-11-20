import os
import csv

class BaseCar:
    #car_type brand passenger_seats_count photo_file_name body_whl carrying extra
    def __init__(self, brand, photo_file_name, carrying):
        self.car_type = None
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        filename, file_extension = os.path.splitext(self.photo_file_name)
        return file_extension


class Car(BaseCar):
    def __init__(self, brand, passenger_seats_count, photo_file_name, carrying):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "car"
        self.passenger_seats_count = passenger_seats_count



class Truck(BaseCar):
    def __init__(self, brand, photo_file_name, body, carrying):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"

        try:
            body = body.split('x')
            self.body_width = float(body[0])
            self.body_height = float(body[1])
            self.body_length = float(body[2])
        except:
            self.body_width = self.body_height = self.body_length = 0


    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(BaseCar):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "spec_machine"
        self.extra = extra


def get_car_list(path):
    car_list = []

    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter = ';')
        next(reader)
        for row in reader:
            try:
                if row[0] == 'car':
                    car = Car(row[1], int(row[2]), row[3], float(row[5]))
                    car_list.append(car)

                elif row[0] == 'truck':
                    truck = Truck(row[1], row[3], row[4], float(row[5]))
                    car_list.append(truck)
                elif row[0] == 'spec_machine':
                        spec_machine = SpecMachine(row[1], row[3], float(row[5]), row[6])
                        car_list.append(spec_machine)
            except:
                pass

    return car_list


