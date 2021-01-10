Share Apache Arrow objects between Python and R using rpy2.

This is still early work in progress, with the following
example/demo:

```python
import rpy2.robjects.packages as packages
import pyarrow
import rpy2_arrow.pyarrow_rarrow as pyra

base = packages.importr('base')
rarrow = packages.importr('arrow')


py_array = pyarrow.array(range(10))

# Vanilla rpy2 
r_array = pyra.pyarrow_to_r_array(py_array)
# (r_array is wrapped in an R environment)

print(base.sum(r_array))
print(''.join(r_array['ToString']()))


# --WIP--

# The package rpy2-R6 offers a better integration of R6 objects,
# and conversion rules.

# Create an R external pointer (wrapping the Python C pointer)
r_a = pyra.pyarrow_to_sexpextptr_array(py_array)

# The R6 wrapper comes in two flavors: a and b.
import rpy2_R6.r6a as r6a

# Python proxy for the R6 class
RArray = r6a.R6Class(rarrow.Array)

# Create an instance using our pointer
r_array = RArray['new'](r_a)

# Run an R function on our insance
print(base.sum(r_array))



import rpy2_R6.r6b as r6b

# Python proxy for the R6 class
rarray_factory = r6b.R6DynamicClassGenerator(rarrow.Array)

# Create an instance using our pointer
r_array = rarray_factory.new(r_a)

# Run an R function on our insance
print(base.sum(r_array))

print(''.join(r_array.ToString()))
```
