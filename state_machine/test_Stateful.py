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


# Awaitable alias to https://docs.python.org/3/library/typing.html#typing.Generator

def action_tmpl(p):
    print('action running', p)


# If priority not set, using default priority := number of transitions. Lower is higher priority.
# In case of even priority, first scheduled actions are executed first
def pact(priority=None, action=action_tmpl):
    return priority, action  # Action running order pact


action_range = range(1, len(TestStates) + 1)
transitions = [(f, t, lambda v: 'ev1' in v, pact(), lambda v: print(f'done{f}->{t}', v))
               for f, t in sorted(set(combinations(chain(action_range, reversed(action_range)), 2)))]
print(*transitions)


class TestTransitions(TestCase):
    def test_init(self):
        t1: Transition = (0, 1, lambda v: 'ev1' in v, pact, lambda v: print('done1', v))
        t2, t3 = (1, 2, lambda v: True, pact, lambda v: print('done2', v)), \
                 (2, 3, lambda v: True, pact, lambda v: print('done3', v))

        # ts = Transitions([t1, t2, t3])
        ts = Transitions(generate_transitions_template(TestStates))
        lq = PriorityQueue()
        g: stateful_generator = stateful_generator(TestStates.Stopped.value, ts, q=lq, exec_wait_result=True)
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
