import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures._base import Future
from contextvars import ContextVar
from enum import Enum, auto
from unittest import TestCase

from state_machine.Stateful import Transition, Transitions, stateful_generator, Event


class TestStates(Enum):
    Running = auto()
    Stopped = auto()


conditions = [[lambda v: False] * len(TestStates)] * len(TestStates)


# Awaitable alias to https://docs.python.org/3/library/typing.html#typing.Generator

TEST = ContextVar('TEST', default=0)

def action(p):
    TEST.set(1)
    print('action running', p)
    return str(TEST.get()) + ' ContextVar'

class TestTransitions(TestCase):
    def test_init(self):
        t1: Transition = (0, 1, lambda v: 'ev1' in v, action, lambda v: v.result())
        t2, t3 = (1, 2, lambda v: True, action, lambda v: print('done', v)), \
                 (2, 3, lambda v: True, action, lambda v: print('done', v))

        ts = Transitions([t1, t2, t3])
        g = stateful_generator(0, ts)
        print(r := next(g))
        print('test', TEST.get())
        ev: Event = ('ev1', ('arg1', 'arg2'))
        print(r := g.send(ev))
        print(r := g.send(('ev2', ('arg1', 'arg2'))))
        print(r := g.send(('ev3', ('arg1', 'arg2'))))
        import numpy as np
        print(np.array(conditions))
        print(np.array(ts))
        print('test', TEST.get())
