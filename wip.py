# RFC2083 https://tools.ietf.org/html/rfc2083#page-15

# Chunk structure
# Length     - 4 bytes
# Chunk type - 4 bytes 
# Chunk data - 4 bytes 
# CRC        - 4 bytes 


# Chunk naming convention
# Ancillary, Private, Reserved, Safe-to-copy 

class PNGExplorer(object):
    
    def __init__(self, file):
        self.file = file
        self.fileBuffer = open(file, 'rb')
        self.chunkDecoders = {
            b'IHDR': self._ihdr_decoder,
        }
        
    def _ensure_is_png(self):
        self.fileBuffer.seek(0, 0)
        file_signature = self.fileBuffer.read(8)
        png_signature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
        for signature, byte in zip(png_signature, file_signature):
            if signature != byte:
                print('File signature not matching PNG.')
                raise BaseException

    def _chunk_reader(self):
        length = int.from_bytes(self.fileBuffer.read(4), 'big')
        chunk_type = self.fileBuffer.read(4)
        data_offset = self.fileBuffer.tell()
        self.fileBuffer.seek(length, 1)
        crc = self.fileBuffer.read(4)
        return length, data_offset, chunk_type, crc
        
    def _ihdr_decoder(self, data_offset):
        carriage = self.fileBuffer.tell()
        self.fileBuffer.seek(data_offset, 0)
        data = {
            'width': self.fileBuffer.read(4),
            'height': self.fileBuffer.read(4),
            'bitDepth': self.fileBuffer.read(1),
            'colorType': self.fileBuffer.read(1),
            'filterMethod': self.fileBuffer.read(1),
            'interlaceMethod': self.fileBuffer.read(1),
        }
        self.fileBuffer.seek(carriage, 0)
        return data
    
    def _type_decoder(self, chunk_type, data_offset):
        if chunk_type in self.chunkDecoders:
            return self.chunkDecoders[chunk_type](data_offset)
        else:
            return None
        
    def run(self):
        self._ensure_is_png()
        while True:
            length, data_offset, chunk_type, crc = self._chunk_reader()
            if chunk_type == b'':
                break
            data = self._type_decoder(chunk_type, data_offset)
            if data is not None:
                print(data)


png = PNGExplorer('cat.png')
png.run()
