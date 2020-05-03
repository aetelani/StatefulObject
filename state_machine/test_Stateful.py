import asyncio
import itertools
from asyncio import AbstractEventLoop
from concurrent.futures._base import Future
from contextvars import ContextVar
from enum import Enum, auto
from itertools import combinations, chain
from queue import PriorityQueue
from unittest import TestCase

from state_machine.Stateful import Transition, Transitions, stateful_generator, Event, exec_next_action, \
    generate_transitions_template


class TestStates(Enum):
    Stopped = auto()
    Running = auto()
    Jumping = auto()


class TestTransitions(TestCase):
    def test_init(self):
        ts = Transitions(generate_transitions_template(TestStates))
        lq = PriorityQueue()
        initial_value = TestStates.Stopped.value
        g: stateful_generator = stateful_generator(initial_value, ts, q=lq, exec_wait_result=True)
        print(r := next(g))
        ev: Event = ('ev1', ('arg1', 'arg2'))
        print(r := g.send(ev))
        print(r := g.send(('ev1', ('arg1', 'arg2'))))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(r := g.close(), 'closing')

        import numpy as np
        print(np.array([i for i in transitions]))
        print(np.array(ts))
