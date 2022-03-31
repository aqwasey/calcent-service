import random


class RussianRoullete:
    def complain_code():
        return str(''.join(random.choice('0123456789ABCDEFGH') for i in range(6)))

    def access_pin():
        return str(''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for k in range(5)))
