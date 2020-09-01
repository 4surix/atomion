try: from typing import *
except ImportError:
    class Any: pass
    class NoReturn: pass
    class ClassVar: pass
    class Hashable: pass
    class Awaitable: pass
    class Coroutine: pass
    class AsyncIterable: pass
    class AsyncIterator: pass
    class Iterable: pass
    class Iterator: pass
    class Reversible: pass
    class Sized: pass
    class Container: pass
    class Collection: pass
    class ByteString: pass
    class MappingView: pass
    class KeysView: pass
    class ItemsView: pass
    class ValuesView: pass
    class ContextManager: pass
    class AsyncContextManager: pass
    class Counter: pass
    class ChainMap: pass
    class Generator: pass
    class AsyncGenerator: pass
    class Type: pass
    class Deque: pass


    class __Subscriptable:
        def __getitem__(self, tuple_or_type):
            return None

    Union = Optional = Generic = NamedTuple = Callable     \
    = AbstractSet = MutableSet = Mapping = MutableMapping  \
    = Sequence = MutableSequence = Tuple = List = Set      \
    = FrozenSet = Dict = DefaultDict = IO = __Subscriptable()


    TextIO = IO[str]
    BinaryIO = IO[bytes]


    def cast(typ, val):
        return val