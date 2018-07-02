class Memory(object):

    def __init__(self):
        self.mp: int = 0
        self.memory = None

    def load_from_file(self, filename):
        self.memory = bytearray(open(filename, 'rb').read())

    def read(self, bytes_count):
        """
        Read x bytes from memory
        :param bytes_count: int
        :return:
        """
        self.mp += bytes_count
        return bytes(self.memory[self.mp-bytes_count:self.mp])

    def get_pointer(self):
        return self.mp

    def seek(self, offset, offset_type):
        """
        Manage memory pointer by offset and offset_type
        :param offset: int
            offset for memory pointer, interpretation depends on offset_type
        :param offset_type: int
            if 0 set memory pointer to offset
            if 1 add offset to memory pointer
        :return: None
        """
        if offset_type == 0:
            self.mp = offset
        elif offset_type == 1:
            self.mp += offset
