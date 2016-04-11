__author__ = 'veselt12'
import numpy
import sys
import io
import gzip
from gzip import GzipFile

if sys.version_info < (3, 0):
    import synonyms.in_out.large_file_hack

    numpy.lib.format.read_array = large_file_hack.read_array


class GzipFileFixed(GzipFile):
    def read1(self, size=-1):
        return self.read(size)


def open22(filename, mode="rb", compresslevel=9, encoding=None, errors=None, newline=None):
    if "t" in mode:
        if "b" in mode:
            raise ValueError("Invalid mode: %r" % (mode,))
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if errors is not None:
            raise ValueError("Argument 'errors' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")

    gz_mode = mode.replace("t", "")
    if isinstance(filename, (str, bytes)):
        binary_file = GzipFile(filename, gz_mode, compresslevel)
    elif hasattr(filename, "read") or hasattr(filename, "write"):
        binary_file = GzipFile(None, gz_mode, compresslevel, filename)
    else:
        raise TypeError("filename must be a str or bytes object, or a file")

    if "t" in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    else:
        return binary_file


if sys.version_info < (3, 3):
    gzip.GzipFile=GzipFileFixed