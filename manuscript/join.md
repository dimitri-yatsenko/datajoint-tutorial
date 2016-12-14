## Join operator *
The result of the join operator `a * b` contains all matching combinations of tuples from `a` and `b`.

### Principles
1. The operands `a` and `b` must be *join-compatible*.
2. The primary key of the result is the union of the primary keys of the operands.

### Examples

Example 1
: When the operands have no common attributes, the result is the cross product -- all combinations of tuples.

![](images/join-example1.png)

Example 2
: When the operands have common attributes, only tuples with matching values are kept.

![](images/join-example2.png)


### Left join
A modification of the join operator is the *left join*.  It is implemented as a `a ** b` in Python and `a .* b` in MATLAB.
The left join keeps all the tuples from `a` even in the absence of the matching tuples from `b`.  For tuples with no matches in `b`, the non-key attributes from `b` are filled with NULLs.

Example 3 
: Outer join

![](images/outer-example1.png)
