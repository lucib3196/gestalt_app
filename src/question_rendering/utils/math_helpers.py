from math import log10, floor
from typing import Callable, Iterable, Mapping, Sequence, Union


Number = Union[int, float]
NumericOrSeq = Union[Number, Sequence[Number]]


def _round_sigfig(value: Number, figs: int) -> Number:
    """Round `value` to `figs` significant figures."""
    if value == 0 or figs <= 0:
        return 0
    return round(value, figs - 1 - floor(log10(abs(value))))


def _round_decimals(value: Number, places: int) -> Number:
    """Round `value` to a fixed number of decimal places."""
    return round(value, places)


# Registry of available rounding strategies ---------------------------------
_ROUND_METHODS: Mapping[str, Callable[[Number, int], Number]] = {
    "sigfigs": _round_sigfig,
    "decimals": _round_decimals,
}


def round_value(
    data: NumericOrSeq, digits: int, method: str = "sigfigs"
) -> NumericOrSeq:
    if method not in _ROUND_METHODS:
        raise ValueError(
            f"Unknown rounding method '{method}'. " f"Available: {list(_ROUND_METHODS)}"
        )

    round_fn = _ROUND_METHODS[method]
    if isinstance(data, (int, float)):
        return round_fn(data, digits)

    rounded = [round_fn(x, digits) for x in data]
    return type(data)(rounded) if not isinstance(data, tuple) else tuple(rounded)  # type: ignore
