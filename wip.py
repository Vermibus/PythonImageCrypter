# RFC2083 https://tools.ietf.org/html/rfc2083#page-15

# Chunk structure
# Length     - 4 bytes
# Chunk type - 4 bytes 
# Chunk data - 4 bytes 
# CRC        - 4 bytes 


# Chunk naming convention
# Ancillary, Private, Reserved, Safe-to-copy

# Local files
from decoder import ChunksDecoder
from memory import Memory   


class PNGExplorer(object):

    def __init__(self):
        self.image = Memory()
        self.decoder = ChunksDecoder(self.image)
        self.chunkData = []

    def load_image(self, filename):
        self.image.load_from_file(filename)

    def ensure_is_png(self):
        if self.image is None:
            print('Image has not been loaded yet. Exiting')
            raise BaseException
        png_signature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
        if any(x != y for x, y in zip(self.image.read(8), png_signature)):
            print('File signature not matching PNG.')
            raise BaseException

    def _chunk_reader(self):
        position = self.image.get_pointer()
        data_length = int.from_bytes(self.image.read(4), 'big')
        chunk_type = self.image.read(4)
        data_offset = self.image.get_pointer()
        self.image.seek(offset=data_length, offset_type=1)
        crc = self.image.read(4)
        return position, data_length, data_offset, chunk_type, crc

    def run(self):
        self.ensure_is_png()
        while True:
            position, data_length, data_offset, chunk_type, crc = self._chunk_reader()
            if chunk_type == b'':
                break

            data = self.decoder.decode(chunk_type, data_length, data_offset)
            self.chunkData.append({
                'type': chunk_type,
                'position': position,
                'data_length': data_length,
                'data_offset': data_offset,
                'data': data,
                'crc': crc,
            })

            computed_crc = self.decoder.crc32(position, data_length)
            if computed_crc.to_bytes(4, 'big') != crc:
                print("Computed CRC is not matching the provided one. Chunk dump:\n"+str(self.chunkData[-1]))


if __name__ == '__main__':
    png = PNGExplorer()
    png.load_image('cat.png')
    png.run()
