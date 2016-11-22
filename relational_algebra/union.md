So far DataJoint has not offered the union operator and we have not seen dire need for it.  But supply creates demand, so let's provide it.  Additionally, unions enable implementation of outer joins: (left, right, and full)

## Syntax
```python
a + b    # union of relations `a` and `b`
```

## Rules 
As always, datajoint implements things in a somewhat restricted way to ensure high performance and expressiveness and to avoid common programming mistakes.  Note that the datajoint's union is conceptually closer to FULL OUTER JOIN than to UNION in SQL.   Although much thinking goes into formulating the internal rules, the common uses should be simple and intuitive.

1.  The primary key of the expression `a+b`,  will be the union of the primary key attributes of `a` and `b`.
1. Matching attributes (same name) in both arguments must be of compatible datatypes.  
1. The result will contain all tuples from `a` and `b` and all attributes from `a` and `b` but pairs of tuples without conflicts in the primary key attributes will be combined into one.  Thus each tuple in the result comes from `a` or `b` or by combining matching tuples from `a` and `b`. 
1.  If `a` and `b` have a shared attribute, the result will take the value from `a` or `b`, whichever present.  In combined tuples where the share attribute is non-key in both relations, the value will be taken from `a`.  Thus with shared non-key attributes, `a+b` is not equivalent to `b+a`. 
1.  Non-key attributes are taken from their respective relations `a` or `b` and the missing attributes in non-combined tuples are filled with NULLs.  This means that the result may have NULLs in its primary key in attributes that are not in the primary key of the other relation.

## Equivalence to SQL's UNION
When `a` and `b` have the same attributes of the same types and all attributes are in the primary key of either `a` or `b`, then `a + b` is equivalent to UNION.

## Equivalence to LEFT, RIGHT, and FULL JOINS
When defined as above, the union operator can be used to implement `a NATURAL LEFT JOIN b` as
```python
a * b + a
```
Similarly, `a NATURAL RIGHT JOIN b` becomes

```python
a * b + b
``` 
and `a NATURAL FULL OUTER JOIN b` becomes 

```python
a * b + a + b
```
It may be argued that `a*b + a` is easier to explain to new users than the left join.  

Note that MySQL does not support full joins but we will provide them using a combination of left JOIN and a union. 

## Examples
### Example 1:  Simple union
Let relation `a` with primary key (i, k) equal 

| *i    | *k    | 
|:-:    |:-:    |
|   1   |  1    |
|   1   |  2    |
|   2   |  1    |

Let relation `b` with primary key (k, i) equal 

| *k    |  *i   | 
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

### Example 2:  Simple union
Let relation `a` with primary key (i) equal 

| *i    |  k    | 
|:-:    |:-:    |
|   1   |  1    |
|   2   |  2    |
|   3   |  1    |

Let relation `b` with primary key (k) equal 

| *k    |  i    | 
|:-:    |:-:    |
|   1   |   1   |
|   2   |   1   |
|   3   |  3    |

Then `a+b` will be

| *i    | *k    | 
|:-:    |:-:    |
|   1   |  1    |
|  1  | 2  | 
|   2   |  2    |
|   3   |  1    |
|  3  |  3 |


### Example 3:  matching non-key attribute 

Let relation `a` with primary key (i, k) equal 

| *i    | *k    | m | 
|:-:    |:-:    |:-: |
|   1   |  1    | 0 |
|   1   |  2    | 0 |
|   2   |  1    | 0 |

Let relation `b` with primary key (i, k) equal 

| *i    |  *k   | m | 
|:-:    |:-:    |:-: |
|   1   |   1   | 8 |
|   2   |   1   | 8 |
|   2   |  3    | 8 |

Then `a+b` will be

| *i    | *k    | m |
|:-:    |:-:    |:-: |
|   1   |  1    | 0 |
|   1   |  2    | 0 |
|   2   |  1    | 0 |
|   2   |  3    | 8 |

Then `b+a` will be

| *i    | *k    | m |
|:-:    |:-:    |:-: |
|   1   |  1    | 8 |
|   1   |  2    | 0 |
|   2   |  1    | 8 |
|   2   |  3    | 8 |

Note that `a+b` does not equal `b+a`.  This should be avoided by renaming shared attributes that dependent differently on the primary key. 

### Example 4:  Dependent attributes present in one or the other argument

Let relation `a` with primary key (i, k) equal 

| *i    | *k    | *m | 
|:-:    |:-:    |:-: |
|   1   |  1    | 0 |
|   1   |  2    | 0 |
|   2   |  1    | 0 |

Let relation `b` with primary key (i, k) equal 

| *i    |  *k   | n | 
|:-:    |:-:    |:-: |
|   1   |   1   | 8 |
|   2   |   1   | 8 |
|   2   |  3    | 8 |

Then `a+b` will be

| *i    | *k    | *m  | n  |
|:-:    |:-:    |:-:  |:-:  |
|   1   |  1    | 0 |  8 |
|   1   |  2    | 0 | NULL |
|   2   |  1    | 0 | 8 |
|   2   |  3    | NULL | 8 |

Note the NULL in the primary key.

### Example 5:  OUTER JOINs
Let relation `a` with primary key (i, k) equal 

| *i    | *k    | 
|:-:    |:-:    |
|   1   |  1    |
|   1   |  2  |
|   3   |  1  |

Let relation `b` with primary key (i) equal 

| *i    |   n | 
|:-:    |:-:    |
|   1   |   8 |
|   2   |   8 |
|   4   |   8 |

Then `a*b` will be

| *i    | *k    |  n  |
|:-:    |:-:    |:-:  |
|   1   |  1    |  8 |
|   1   |  2    |  8 |

And `a*b + a` will correspond to the LEFT JOIN:

| *i    | *k    |  n  |
|:-:    |:-:    |:-:  |
|   1   |  1    |  8 |
|   1   |  2    |  8 |
|  3  |  1   | NULL |

And `a*b + b` will correspond to the RIGHT JOIN

| *i    | *k    |  n  |
|:-:    |:-:    |:-:  |
|   1   |  1    |  8 |
|   1   |  2    |  8 |
|  2  | NULL | 8 |
|  4  | NULL | 8 |

And `a*b + a + b` will correspond to the FULL OUTER JOIN

| *i    | *k    |  n  |
|:-:    |:-:    |:-:  |
|   1   |  1    |  8 |
|   1   |  2    |  8 |
|  2  | NULL | 8 |
|  3  |  1   | NULL |
|  4  | NULL | 8 |