Share Apache Arrow objects between Python and R using rpy2.

This is still early work in progress, with the following
example/demo:

```python
import rpy2.robjects.packages as packages
import pyarrow
import rpy2_arrow.sexpextptr as r_ptr
from rpy2_R6.utils import dollar


rarrow = packages.importr('arrow')


py_array = pyarrow.array(range(10))

# Create an R external pointer (wrapping the Python C pointer)
r_a = r_ptr.pyarrow_to_sexpextptr_array(py_array)

# The R6 wrapper comes in two flavors: a and b.
import rpy2_R6.r6a as r6a

# Python proxy for the R6 class
RArray = r6a.R6Class(rarrow.Array)

# Create an instance using our pointer
r_array = dollar(RArray, 'new')(r_a)

# Run an R function on our insance
base = packages.importr('base')
print(base.sum(r_array))



import rpy2_R6.r6b as r6b

# Python proxy for the R6 class
rarray_factory = r6b.R6DynamicClassGenerator(rarrow.Array)

# Create an instance using our pointer
r_array = rarray_factory.new(r_a)

# Run an R function on our insance
base = packages.importr('base')
print(base.sum(r_array))

print(''.join(r_array.ToString()))
```
