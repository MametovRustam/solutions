from typing import Generator, Iterable, TypeVar

T = TypeVar("T")

def chain(*iterables: Iterable[T]) -> Generator[T, None, None]:
    for iterable in iterables:
        yield from iterable

class Chain:
    def __init__(self, *iterables: Iterable[T]):
        self.iterables = iterables
        self.mark = 0
        self.ex_mark = 0

    def __iter__(self):
        return self
    def __next__(self) -> T:
        while True:
            try:
                current = list(self.iterables[self.ex_mark])
            except IndexError:
                raise StopIteration
            else:
                try:
                    result = current[self.mark]
                except IndexError:
                    self.mark = 0
                    self.ex_mark += 1
                    continue
                else:
                    self.mark += 1
                    return result