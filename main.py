import connection
import gui


class Analyzer:

    def __init__(self):
        self.conn = connection.Connection('COM3', 115200)
        self.window = gui.Gui('800x700', 'mk4 CANAnalyzer', self.conn)
        self.window.set_callback(self.update)
        self.table = self.window.get_table()

    def show(self):
        self.window.show()

    def update(self):
        can_data = self.conn.get_data()
        for key in can_data:
            bytes_array = can_data[key].encode()
            if key == 0:
                pass

        self.table.data_update(can_data)


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.show()
