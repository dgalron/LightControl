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
    off_state = struct.pack('L', 0)

    def __init__(self):
        self.warm = 0
        self.cool = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.color_pattern = BitVector64(0)

    def __setattr__(self, name, value):
        if name != 'color_pattern':
            if 0 <= value <= 255:
                self.__dict__[name] = value
            else:
                raise ValueError('can\'t set %s to %s. value must be between 0 and 255!' % (name, value))
        else:
            self.__dict__[name] = value

    def marshal(self):
        # bitshift values then 'or' them
        p = (int(self.warm ) << 8 * 7) |  \
            (int(self.cool ) << 8 * 6) |  \
            (int(self.red  ) << 8 * 5) |  \
            (int(self.green) << 8 * 4) |  \
            (int(self.blue ) << 8 * 3) |  \
            int(self.color_pattern)
        return struct.pack('L', p)

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5}' \
            .format(self.warm, self.cool, self.red, self.green, self.blue, self.color_pattern)
