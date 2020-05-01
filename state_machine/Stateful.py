import asyncio
from asyncio import AbstractEventLoop, Semaphore
from concurrent.futures._base import Executor, Future
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from queue import Queue
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


def stateful_generator(initial: int, ts: Transitions, executor: Executor = None, q: Queue = None):
    pool = executor or ThreadPoolExecutor(max_workers=3)

    next_state = initial

    (f, t, c, a, d) = zip(*ts)

    if q is None:
        local_execution = True
        q = Queue()

    def test(tester: Callable):
        return tester(event)

    def run(action_index) -> bool:
        def wrap(fun, ev, done):
            action_future = pool.submit(fun, ev)
            action_future.add_done_callback(done)
            return action_future

        q.put(partial(wrap, a[action_index], event, d[action_index]))

        if local_execution:
            result_partial: Future = q.get()
            future: Future = result_partial()
            future.result()  # Done cb called
            q.task_done()

        return True

    try:
        while True:
            event: Event = yield next_state
            ss = [t[i] for i in range(len(f)) if f[i] == next_state and test(c[i]) and run(i)]
            next_state = ss and ss[0] or next_state
    finally:
        if local_execution:
            q.join()
