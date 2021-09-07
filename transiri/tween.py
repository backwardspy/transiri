import time
from typing import Any, Optional, Callable
from dataclasses import dataclass


Callback = Callable[[Any], None]


@dataclass(frozen=True)
class Tween:
    # object & attribute to work on
    target: Any
    attribute: str

    # start & end values of the object's attribute
    start_value: float
    end_value: float

    # how long the tween should take in seconds
    duration: float

    # time when the tween was started
    start_time: float

    # optional callback to invoke when tween finishes
    on_complete: Optional[Callback]


# all active tweens are stored in this list
tweens: list[Tween] = []


def interpolate(start_value: float, end_value: float, progress: float) -> float:
    # you could add fancy easing functions in here
    return start_value + (end_value - start_value) * progress


def start(
    target: Any,
    attribute: str,
    *,
    start_value: float,
    end_value: float,
    duration: float,
    on_complete: Optional[Callback] = None,
) -> None:
    tweens.append(
        Tween(
            target=target,
            attribute=attribute,
            start_value=start_value,
            end_value=end_value,
            duration=duration,
            start_time=time.perf_counter(),
            on_complete=on_complete,
        )
    )


def update() -> None:
    now = time.perf_counter()

    finished: list[Tween] = []
    for tween in tweens:
        progress = (now - tween.start_time) / tween.duration
        if progress >= 1:
            finished.append(tween)
            continue

        value = interpolate(tween.start_value, tween.end_value, progress)
        setattr(tween.target, tween.attribute, value)

    # this isn't very efficient, consider using a pool with tweens marked as dead that can be reused
    for tween in finished:
        if tween.on_complete:
            tween.on_complete(tween.target)
        tweens.remove(tween)
