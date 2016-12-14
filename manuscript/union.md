## Union operator +
The result of the union operator `a + b` contains all the tuples from both operands.  

### Principles 
1. As in all operators, the order of the attributes in the operands is not significant.  
1. Operands `a` and `b` must have the same primary key attributes.  Otherwise, an error will be raised.
2. Operands `a` and `b` may not have any common non-key attributes.  Otherwise, an error will be raised.
3. The result `a + b` will have the same primary key as `a` and `b`.
4. The result `a + b` will have all the non-key attributes from both `a` and `b`. 
5. For tuples that are found in both `a` and `b` (based on the primary key), the non-key attributes will be filled from the corresponding tuples in `a` and `b`.
6. For tuples that are only found in either `a` or `b`, the other operands' non-key attributes will filled with NULLs.

### Examples

Example 1
:  Note that the order of the arguments does not matter.

![](images/union-example1.png)

Example 2:

Non-key attributes are combined from both relations and filled with NULLs when missing.

![](images/union-example2.png)
