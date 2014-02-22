import struct


class BitVector64(object):
    def __init__(self, val=0):
        self.__bit_vector = ''.join(['0' for _ in xrange(64)])
        self.set_bits(0, val)

    def get_bits(self, start, end):
        return self.__bit_vector[start:end]

    def set_bits(self, location, value):
        assert type(value) == int
        s = '{0:b}'.format(value)
        self.__bit_vector = self.__bit_vector[:location] + s + self.__bit_vector[location + len(s):]
        assert len(self.__bit_vector) == 64

    def bitwise_and(self, other):
        assert len(other.__bit_vector) == 64
        r = ['1' if int(i) + int(j) == 2 else '0' for i, j in zip(self.__bit_vector, other.__bit_vector)]
        assert len(r) == 64
        return r

    def __str__(self):
        return self.__bit_vector

    def __int__(self):
        return int(self.__bit_vector, 2)


# TODO: Make this a singleton
class LightState(object):
    def __init__(self):
        self.power = BitVector64(0)
        self.white = BitVector64(0)
        self.white_texture = BitVector64(0)
        self.white_dimness = BitVector64(0)
        self.color = BitVector64(0)
        self.red_val = BitVector64(0)
        self.green_val = BitVector64(0)
        self.blue_val = BitVector64(0)
        self.color_pattern = BitVector64(0)

    def set_power(self, val):
        prev_val = int(self.power.get_bits(0, 1))
        self.power.set_bits(0, val)
        return prev_val != val

    def set_white(self, val):
        pass

    def set_dimness(self, val):
        pass

    def set_color_pattern(self, val):
        pass

    def set_white_texture(self, val):
        pass

    def marshal(self):
        p = int(self.power) | int(self.white) | int(self.white_texture) | int(self.white_dimness) | \
            int(self.color) | int(self.red_val) | int(self.green_val) | int(self.blue_val) | \
            int(self.color_pattern)
        return struct.pack('L', p)

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7} {8}' \
            .format(self.power, self.white, self.white_texture, self.white_dimness, self.color, self.red_val,
                    self.green_val, self.blue_val, self.color_pattern)
