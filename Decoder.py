from functools import wraps

import zlib


def decoder_decorator(func):
    def _decorator(request, **kwargs):
        carriage = request.fileBuffer.tell()
        request.fileBuffer.seek(kwargs['data_offset'], 0)
        response = func(request, **kwargs)
        request.fileBuffer.seek(carriage, 0)
        return response
    return wraps(func)(_decorator)


class ChunksDecoder(object):

    def __init__(self, fileBuffer):
        self.fileBuffer = fileBuffer
        self.chunkDecoders = {
            b'IHDR': self._ihdr_decoder,
            b'gAMA': self._gama_decoder,
            b'tEXt': self._text_decoder,
        }
        self.crc32_table = self._init_crc32_table()

    def decode(self, chunk_type, length, data_offset):
        if chunk_type in self.chunkDecoders:
            return self.chunkDecoders[chunk_type](length=length, data_offset=data_offset)
        else:
            return None

    @decoder_decorator
    def _ihdr_decoder(self, **kwargs):
        return {
            'width': int.from_bytes(self.fileBuffer.read(4), 'big'),
            'height': int.from_bytes(self.fileBuffer.read(4), 'big'),
            'bitDepth': self.fileBuffer.read(1),
            'colorType': self.fileBuffer.read(1),
            'filterMethod': self.fileBuffer.read(1),
            'interlaceMethod': self.fileBuffer.read(1),
        }

    @decoder_decorator
    def _gama_decoder(self, **kwargs):
        return {
            'imageGamma': float(int.from_bytes(self.fileBuffer.read(4), 'big'))/100000
        }

    @decoder_decorator
    def _text_decoder(self, **kwargs):
        limit = kwargs['data_offset']+kwargs['length']
        keyword = bytearray()
        text = bytearray()

        current_sink = keyword
        while self.fileBuffer.tell() < limit:
            byte = self.fileBuffer.read(1)
            if byte != 0x0:
                current_sink.append(byte)
            else:
                current_sink = text
        return {
            'keyword': keyword,
            'text': text,
        }

    @staticmethod
    def _init_crc32_table():
        crc32table = []
        for byte in range(256):
            crc = 0
            for bit in range(8):
                if (byte ^ crc) & 1:
                    crc = (crc >> 1) ^ 0xEDB88320
                else:
                    crc >>= 1
                byte >>= 1
            crc32table.append(crc)
        return crc32table

    def crc32(self, position, data_length):
        crc = 0xffffffff
        carriage = self.fileBuffer.tell()
        self.fileBuffer.seek(position+4, 0)  # Length of data not included in CRC
        while self.fileBuffer.tell() < position+8+data_length:
            crc = self.crc32_table[(ord(self.fileBuffer.read(1)) ^ crc) & 0xff] ^ (crc >> 8)
        self.fileBuffer.seek(carriage, 0)
        return crc ^ 0xffffffff
