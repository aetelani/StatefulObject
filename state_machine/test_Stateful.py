from enum import Enum, auto
from unittest import TestCase

from state_machine.Stateful import Transition, Transitions, stateful_generator, Event


class TestStates(Enum):
    Running = auto()
    Stopped = auto()


conditions = [[lambda v: False] * len(TestStates)] * len(TestStates)


# Awaitable alias to https://docs.python.org/3/library/typing.html#typing.Generator


class TestTransitions(TestCase):
    def test_init(self):
        t1: Transition = (0, 1, lambda v: 'ev1' in v, lambda v: v, lambda v: print('done', v))
        t2, t3 = (1, 2, lambda: True, None, lambda: print('done')), \
                 (2, 3, lambda: True, lambda: True, lambda: print('done'))

        ts = Transitions([t1, t2, t3])
        g = stateful_generator(0, ts)
        print(r := next(g))
        ev: Event = ('ev1', ('arg1', 'arg2'))
        print(r := g.send(ev))

        import numpy as np
        print(np.array(conditions))
        print(np.array(ts))
