import asyncio
from asyncio import AbstractEventLoop
from typing import Callable, Any, Tuple, List, NewType, Optional

Condition = Callable[[Any], bool]
Action = Callable[[Any], bool]
ActionDone = Callable[[Any], Any]
State = int
event_name, event_args = str, Optional[Any]
Event = Tuple[event_name, event_args]
from_state, to_state = State, State
Transition = Tuple[from_state, to_state, Condition, Action, ActionDone]
Transitions = NewType('Transitions', List[Transition])


def stateful_generator(initial: int, ts: Transitions):
    loop: AbstractEventLoop = asyncio.get_event_loop()

    next_state = initial

    (f, t, c, a, s) = zip(*ts)

    def test(tester: Callable):
        return tester(event)

    def run(action_index) -> bool:
        task = loop.create_task(a[action_index](event))
        task.add_done_callback(s[action_index])
        loop.run_until_complete(task)
        return True

    while True:
        event: Event = yield next_state
        ss = [t[i] for i in range(len(f)) if f[i] == next_state and test(c[i]) and run(i)]
        next_state = ss and ss[0] or next_state
