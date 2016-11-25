## Union operator +
DataJoint's union operator '+' acts as set union operator or the outer join relational operator depending on its operands.  These two behaviors are not distinct from each other but rather represent special cases of the same operator.

In contrast to SQL and classical relational algebra, attributes are identified by their names rather than by their positions. The operation of the union operator is therefore determined by the composition of its operands' headings.  As always, when we say that two tuples *match*, it means that the attributes with the same names have the same values in both tuples.

### Principles 
1. The result of `a + b` contains all attributes from both `a` and `b`. 
1. The result of `a + b` contains the minimal set of tuples that match all tuples in both `a` and `b` and all combinations of matching tuples of `a` and `b`.
1. The primary key of the result is the union of the primary key attributes of its operands `a` and `b`.
1.  All common attributes in `a` and `b` must be part of the primary key of either `a` or `b`.  An exception will be raised if a non-key attribute with the same name is present in both relations.
1. The common attributes in `a` and `b` must be of compatible datatypes and must belong to the primary key of either `a` or `b`.
1. The common attributes in `a` and `b` must be of a compatible data type for equality comparisons.
1. Attributes that are unique to `a` will be filled with NULLs in tuples that have no match in `a`.  Conversely, attributes that are unique to `b` will be filled with NULLs in tuples that have no match in `b`.


1.  The order of attributes in the operands does not matter and is not guaranteed in the result.

## Equivalence to OUTER JOIN
`a+b` is equivalent to the natural outer join operator in relational algebra.  

## Equivalence to SQL's UNION
`a+b` is equivalent to relational union if `a` and `b` have the same sets of attributes. 

## Implementation of LEFT and RIGHT OUTER JOINs
The natural left join (`a NATURAL LEFT JOIN b`) can now be expressed as
```python
a * b + a
```
or, equivalently, as
```python
(a + b) & a
```
or, equivalently, as
```python
a + (b & a) 
```
or, equivalently
```python
(a - b) + b
``` 

It is difficult to make DataJoint recognize all these patterns and to convert them into efficient SQL, so let's introduce the special syntax indicating left or right joins:

```python
a * ~b      # left outer join  (all rows of `a` are kept).
~a * b      # right outer join (all rows of `b` are kept). 
~a * ~b  # outer join (equivalent to `a+b`)
```

The outer flag `~` survives projections and restrictions but not other operators:
```python
~(a & cond) * b    # equivalent to   (~a & cond) * b
~a.proj() * b    # equivalent to   (~a).proj() * b
```

## Examples
### Example 1:  Simple union
Let relation `a` with primary key (i, k) equal 

| *i    | *k    | 
|:-:    |:-:    |
|   1   |  1    |
|   1   |  2    |
|   2   |  1    |

Let relation `b` with primary key (k) equal 

| *k    |  i    | 
|:-:    |:-:    |
|   1   |   1   |
|   2   |   1   |
|   2   |  3    |

Then `a+b` will be

| *i    | *k    | 
|:-:    |:-:    |
|   1   |  1    |
|   1   |  2    |
|   2   |  1    |
|   3   |  2    |

### Example 2: No matching attributes:  outer join = inner join

Let relation `a` with primary key (i) equal 

| *i    | m | 
|:-:    |:-: |
|   1   |  6  |
|   2   |  6    |

Let relation `b` with primary key (i, k) equal 

|  *k   | n | 
|:-:    |:-: |
|   1   |   8 |
|   2   |   8 |

Then `a+b` will be

| *i    | *k    | m  | n  |
|:-:    |:-:    |:-:  |:-:  |
|   1   |   1   | 6 | 8 |
|   1   |   2   | 6 | 8 |
|   2   |   1   | 6 | 8 |
|   2 |    2  | 6 | 8 |


### Example 3:  Simple outer join

Let relation `a` with primary key (i) equal 

| *i    | m | 
|:-:    |:-: |
|   1   |  6  |
|   2   |  6    |
|   3   |  6    |

Let relation `b` with primary key (i, k) equal 

| *i    |  *k   | n | 
|:-:    |:-:    |:-: |
|   1   |   1   | 8 |
|   1   |   2   | 8 |
|   2   |  3    | 8 |
|   4 |   1  | 8 |

Then `a+b` will be

| *i    | *k    | m  | n  |
|:-:    |:-:    |:-:  |:-:  |
|   1   |   1   | 6 | 8 |
|   1   |   2   | 6 | 8 |
|   2   |  3    | 6 | 8 |
|   4 |   1  | NULL | 8 |
|   3  |  NULL | 6 | NULL

Note `a+b` may produce NULLs in the primary key. 

