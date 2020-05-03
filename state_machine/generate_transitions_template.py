from functools import partial
from itertools import combinations, chain
from typing import Sized


def generate_transitions_template(states: Sized):
    def action_tmpl(p):
        print('action running', p)

    # If priority not set, using default priority := number of transitions. Lower is higher priority.
    # In case of even priority, first scheduled actions are executed first
    def pact(priority=None, action=action_tmpl):
        return priority, action  # Action running order pact

    action_range = range(1, len(states) + 1)
    transitions = [(f, t, lambda v: 'ev1' in v, pact(), partial(print, f, '->', t, ':'))
                   for f, t in sorted(set(combinations(chain(action_range, reversed(action_range)), 2)))]
    return transitions
