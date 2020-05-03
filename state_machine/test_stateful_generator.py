from enum import Enum, auto
from queue import PriorityQueue
from unittest import TestCase

from state_machine.stateful_generator import Transitions, stateful_generator, Event, exec_next_action
from state_machine.generate_transitions_template import generate_transitions_template


class TestStates(Enum):
    Stopped = auto()
    Running = auto()
    Jumping = auto()


class TestTransitions(TestCase):
    def test_init(self):
        ts = Transitions(generate_transitions_template(TestStates))
        lq = PriorityQueue()
        initial_state = TestStates.Stopped.value
        g: stateful_generator = stateful_generator(initial_state, ts, q=lq, exec_wait_result=True)
        print('State', r := next(g))  # atm goes to the first state triggered, that is to self
        ev: Event = ('ev1', ('arg1', 'arg2'))
        print('State', r := g.send(ev))
        print('State', r := g.send(('ev1', ('arg1', 'arg2'))))
        print(it := exec_next_action(lq))  # even going to self runs all the transition actions
        print(it := exec_next_action(lq))  # check the done3->3 messages
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(it := exec_next_action(lq))
        print(r := g.close(), 'closing')
        import numpy as np
        print(np.array(ts))
