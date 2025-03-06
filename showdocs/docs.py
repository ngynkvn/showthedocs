import codecs
import collections
import logging
import os
from collections.abc import MutableSet

from showdocs import config

ExternalDoc = collections.namedtuple("ExternalDoc", "contents".split())

logger = logging.getLogger(__name__)

_filecache = {}


def readone(path):
    return codecs.open(path, encoding="utf-8").read()


def loadall(root=""):
    if not root:
        root = config.ROOT

    root = os.path.normpath(root)
    extdir = os.path.join(root, "external")
    if not os.path.exists(extdir):
        raise RuntimeError(
            "can't find directory 'external' under %r (run getdocs clone?)" % root
        )

    d = {}
    for root, _, files in os.walk(extdir):
        for name in files:
            if os.path.splitext(name)[1] != ".html":
                continue
            fullpath = os.path.join(root, name)
            logger.info("adding %r to docs filecache", fullpath)
            contents = readone(fullpath)
            key = fullpath[len(extdir) + 1 :]

            d[key] = ExternalDoc(contents)

    return d


_init = False


def initfilecache(root=""):
    global _init
    global _filecache
    if _init:
        return _filecache
    # Don't cache anything in testing.
    if not config.TEST:
        _init = True

    logger.info("initializing docs filecache")
    _filecache = loadall(root)
    logger.info("done initializing docs filecache")

    return _filecache


class Collection(MutableSet):
    """A collection represents documentation that was requested by an
    annotator. It is eventually passed to the UI, which returns the HTML in the
    response to a query."""

    def __init__(self):
        # Use a list so order is preserved.
        self._paths = []

        self._filecache = initfilecache()

    def add(self, value):
        if value not in self._filecache:
            raise ValueError("unknown doc %r" % value)
        if value in self._paths:
            return
        logger.info("adding %r to doc collection", value)
        self._paths.append(value)

    def discard(self, value):
        if value in self._paths:
            self._paths.remove(value)

    def __contains__(self, path):
        return path in self._paths

    def __iter__(self):
        return iter(self._paths)

    def __len__(self):
        return len(self._paths)

    def withcontents(self):
        for path in self._paths:
            yield path, self._filecache[path]
