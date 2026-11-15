# MicroPython 1.9.4 compatible runtime injected into `atomion.py`.
# NOTE: Keep free of type annotations, f-strings, and post-3.5 syntax.

_ELEMENT_KEYS = tuple()

def _unescape_el(text):
    if '\\' not in text:
        return text
    out = []
    idx = 0
    end = len(text)
    while idx < end:
        ch = text[idx]
        if ch == '\\' and idx + 1 < end:
            nxt = text[idx + 1]
            if nxt == 'p':
                out.append('|')
            elif nxt == 'n':
                out.append('\n')
            elif nxt == 'c':
                out.append(',')
            else:
                out.append(nxt)
            idx += 2
        else:
            out.append(ch)
            idx += 1
    return ''.join(out)


_EL_UNSET = object()


def _decode_el_scalar(token):
    if not token or token == 'n':
        return None
    if token == 'u':
        return _EL_UNSET
    tag = token[0]
    body = token[1:]
    if tag == 's':
        return _unescape_el(body)
    if tag == 'i':
        return int(body)
    if tag == 'f':
        return float(body)
    if tag == 'b':
        return body == '1'
    return token


def _decode_el_field(token):
    if not token:
        return None
    if token == 'u':
        return _EL_UNSET
    tag = token[0]
    if tag == 't':
        if len(token) == 1:
            return ()
        return tuple([_decode_el_scalar(p) for p in token[1:].split(',')])
    if tag == 'l':
        if len(token) == 1:
            return []
        return [_decode_el_scalar(p) for p in token[1:].split(',')]
    return _decode_el_scalar(token)


class _LazyElement:
    def __init__(self, values):
        self._v = values

    def _raw(self, key):
        try:
            return self._v[_ELEMENT_KEYS.index(key)]
        except ValueError:
            return _EL_UNSET

    def __getitem__(self, key):
        val = self._raw(key)
        if val is _EL_UNSET:
            raise KeyError(key)
        return val

    def get(self, key, default=None):
        val = self._raw(key)
        return default if val is _EL_UNSET else val

    def __contains__(self, key):
        return self._raw(key) is not _EL_UNSET

    def __len__(self):
        return sum(1 for val in self._v if val is not _EL_UNSET)

    def __iter__(self):
        for key, val in zip(_ELEMENT_KEYS, self._v):
            if val is not _EL_UNSET:
                yield key

    def items(self):
        return tuple(
            (key, val) for key, val in zip(_ELEMENT_KEYS, self._v)
            if val is not _EL_UNSET
        )

    def keys(self):
        return tuple(key for key, _ in self.items())

    def values(self):
        return tuple(val for _, val in self.items())

    def copy(self):
        return dict(self.items())

    def __eq__(self, other):
        if isinstance(other, _LazyElement):
            return self._v == other._v
        if isinstance(other, dict):
            return self.copy() == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return repr(self.copy())


class _LazyElements:
    def __init__(self, data, count):
        self._d = data
        self._n = count
        self._ci = -1
        self._cv = None

    def __len__(self):
        return self._n

    def _decode_at(self, index):
        if index == self._ci:
            return self._cv
        start = 0
        pos = 0
        while pos < index:
            start = self._d.index('\n', start) + 1
            pos += 1
        end = self._d.find('\n', start)
        line = self._d[start:] if end == -1 else self._d[start:end]
        vals = tuple([_decode_el_field(tok) for tok in line.split('|')])
        item = _LazyElement(vals)
        self._ci = index
        self._cv = item
        return item

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._n)
            return [self._decode_at(idx) for idx in range(start, stop, step)]
        if index < 0:
            index += self._n
        if index < 0 or index >= self._n:
            raise IndexError('element index out of range')
        return self._decode_at(index)

    def __iter__(self):
        for idx in range(self._n):
            yield self._decode_at(idx)

    def __repr__(self):
        return repr([self._decode_at(idx) for idx in range(self._n)])
