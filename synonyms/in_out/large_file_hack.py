__author__ = 'veselt12'
import numpy
from numpy.lib.format import *


def read_array(fp):
    """
    Read an array from an NPY file.

    Parameters
    ----------
    fp : file_like object
        If this is not a real file object, then this may take extra memory
        and time.

    Returns
    -------
    array : ndarray
        The array from the data on disk.

    Raises
    ------
    ValueError
        If the data is invalid.

    """
    version = read_magic(fp)
    if version != (1, 0):
        msg = "only support version (1,0) of file format, not %r"
        raise ValueError(msg % (version,))
    shape, fortran_order, dtype = read_array_header_1_0(fp)
    if len(shape) == 0:
        count = 1
    else:
        count = numpy.multiply.reduce(shape)

    # Now read the actual data.
    if dtype.hasobject:
        # The array contained Python objects. We need to unpickle the data.
        array = pickle.load(fp)
    else:
        if isfileobj(fp):
            # We can use the fast fromfile() function.
            array = numpy.fromfile(fp, dtype=dtype, count=count)
        else:
            # This is not a real file. We have to read it the memory-intensive
            # way.
            # crc32 module fails on reads greater than 2 ** 32 bytes, breaking large reads from gzip streams
            # Chunk reads to 256mb to avoid issue and reduce memory overhead of the read.
            # In non-chunked case count < max_read_count, so only one read is performed.

            max_buffer_size = 2 ** 28
            max_read_count = max_buffer_size / dtype.itemsize

            array = numpy.empty(count, dtype=dtype)

            for i in range(0, count, max_read_count):
                read_count = max_read_count if i + max_read_count < count else count - i

                data = fp.read(int(read_count * dtype.itemsize))
                array[i:i+read_count] = numpy.frombuffer(data, dtype=dtype, count=read_count)

        if fortran_order:
            array.shape = shape[::-1]
            array = array.transpose()
        else:
            array.shape = shape

    return array