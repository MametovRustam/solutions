from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def cycle(obj: Iterable[T]) -> Generator[T, None, None]:
    """Пишите ваш код здесь."""
    while True:
        for item in obj:
            yield item


class Cycle:
    def __init__(self, obj: Iterable[T]):
        self.obj = obj
        self.iterator = iter(obj)


    def __iter__(self):
        return self


    def __next__(self) -> T:
        while True:
            try:
                return next(self.iterator)
            except StopIteration:
                self.iterator = iter(self.obj)