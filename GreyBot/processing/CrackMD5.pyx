# crack.pyx
from cython.parallel import prange
from libc.string cimport memcpy
from libc.stdlib cimport malloc, free
from libcpp.vector cimport vector
from libcpp.string cimport string

import hashlib
cimport cython

cdef extern from "Python.h":
    void Py_BEGIN_ALLOW_THREADS()
    void Py_END_ALLOW_THREADS()

@cython.boundscheck(False)
@cython.wraparound(False)
def crack_range(unsigned long long start, unsigned long long end, set targets):
    cdef unsigned long long i
    cdef bytes sid_bytes
    cdef str sid
    cdef str hashed
    cdef list matches = []

    # Convert targets to Python set outside nogil for fast lookup
    # We keep it as Python set since md5.hexdigest() returns Python str

    # Parallel loop, release GIL
    with nogil, parallel():
        # We can't append to list in nogil, so use a C++ vector temporarily
        cdef vector[tuple] local_matches
        for i in prange(start, end, nogil=True):
            # Can't call Python functions inside nogil, so we must reacquire GIL for hashlib
            Py_BEGIN_ALLOW_THREADS()
            sid = str(i)
            hashed = hashlib.md5(sid.encode()).hexdigest()
            Py_END_ALLOW_THREADS()

            # Check match and store (must reacquire GIL)
            # We check here with GIL to access Python set
            with gil:
                if hashed in targets:
                    matches.append((i, hashed))

    return matches
