import threading
import serial


class Connection:

    def __init__(self, port_name, baud_rate):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.ser = None

        self.running = True

        self.dict = {}
        self.thread = threading.Thread(target=self.receive)
        self.lock = threading.Lock()

    def open(self):
        try:
            self.ser = serial.Serial(self.port_name, self.baud_rate)
        except serial.serialwin32.SerialException:
            print('[ERROR] could not open port')
            return -1
        return 0

    def start(self):
        self.thread.start()

    def receive(self):
        print('start thread')
        while self.running:
            line = self.ser.readline()
            try:
                line_str = line.decode('utf-8')
            except UnicodeDecodeError:
                print('[ERROR] invalid start byte')
                continue
            clean_str = line_str.replace('\r\n', '')
            can_data = clean_str.split(",")

            if can_data is None:
                continue
            if len(can_data) < 2:
                continue
            if can_data[1] is None:
                continue
            self.lock.acquire()
            self.dict[int(can_data[0], base=10)] = int(can_data[1], base=2)
            self.lock.release()

    def get_data(self):
        self.lock.acquire()
        result = self.dict.copy()
        self.lock.release()
        return result

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()
        if self.thread.is_alive():
            self.thread.join()
        if self.ser is not None:
            if self.ser.isOpen():
                self.ser.close()
