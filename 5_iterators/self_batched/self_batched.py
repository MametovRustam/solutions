from typing import Generator, Iterable, TypeVar, Tuple

T = TypeVar("T")

def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
    """Пиши свой код здесь."""
    batch = []
    for element in iterable:
        batch.append(element)
        if len(batch) == n:
            yield tuple(batch)
            batch = []
    if batch:
        yield tuple(batch)

class Batched:
    def __init__(self, iterable: Iterable[T], n: int):
        self.iterable = iterable
        self.n = n
        self.batch = []
        self.iterator = iter(self.iterable)

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[T, ...]:
        while len(self.batch) < self.n:
            try:
                self.batch.append(next(self.iterator))
            except StopIteration:
                break

        if self.batch:
            result = tuple(self.batch)
            self.batch = []
            return result

        raise StopIteration
