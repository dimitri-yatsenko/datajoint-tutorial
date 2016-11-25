# Data queries 

DataJoint implements a complete algebra of operators on relations, or *relational algebra*.
DataJoint's relational algebra, we believe, improves upon the classical relational algebra and upon other query languages to simplify and enhance the construction and interpretation of precise and efficient data queries.

## Principles
1. **Purely relational**: Data are represented and manipulated in the form of *relations*. 
1. **Algebraic closure**: All relational operators operate on relations and yield relations.  Thus relational expressions may be used as operands in other expressions or may be assigned to variables to be used in other expressions.
1. **Attributes are identified by names.**  All attributes of relations have well-defined names. This includes derived relations resulting from relational operators.  Relational operators use attribute names to determine how to perform the operation. The order of the attributes in relations is not significant.
1. **All relations have a primary key.**  This includes derived relations resulting from relational operators, for which the primary key is properly derived from the primary keys of the operands in expressions.  Relational operators use the information about the operands' primary keys to define the query.

## Matching tuples
Binary relational operators in DataJoint are based on the concept of *matching tuples* and we will use this phrase throughout.  

> Two tuples *match* when they have no common attributes or when their common attributes contain the same values.

Here *common attributes* are those that have the same names in both tuples.  It is usually assumed that the common attributes are of compatible data types to allow equality comparisons.

Another way to phrase the same definition is 

> Two tuples *match* when they have no common attributes whose values differ.

It may be conceptually convenient to imagine that all relations always have an additional invisible attribute, `omega` whose domain comprises only one value, 1.  Then the definition of matching tuples is simplified: 

> Two tuples *match* when their common attributes contain the same values.

Matching tuples can be *merged* into a single tuple without any conflicts of attribute names and values.

### Examples
The following two tuples do match:

![](images/matched_tuples1.png)

The following two tuples also match:

![](images/matched_tuples2.png)

But the following tuples do not match:

![](images/matched_tuples3.png)

## Join compatibility
All binary operators with other relations as its two operands require that their operands be *join-compatible*, which means that:

1. All common attributes in both operands (attributes with the same name) must be part of the primary key of at least one of the operands.
2. All common attributes in the two relations must be of a compatible datatype for equality comparisons.

These restrictions are introduced both for performance reasons and for conceptual reasons.  For  performance, they encourage queries that rely on indexes.  For conceptual reasons, they encourage database design in which entities in different relations are lated to each other by the use of primary keys and foreign keys.


## Summary of relational operators
The following table lists DataJoint's relational operators, to be explain in great detail later.

| operator | notation | result
|:------------:|:------------:|:-------------------------------------------------- |
| restriction | `a & cond` | Contains all tuples from `a` that match the condition `cond`.  The condition `cond` may take on various forms, including other relations, mappings, strings, OR-lists, or AND-lists.  When `a` and `cond` are relations with the same headings, it becomes equivalent to set intersection.  Restriction is the only operator necessary to understand for basic use of DataJoint. 
|difference | `a - cond` | Contains all tuples from `a` that do not match the condition `cond`. The condition `cond` may take on various forms, including other relations, mappings, strings, OR-lists, or AND-lists.   When `a` and `cond` are relations with the same headings, it becomes equivalent to set difference.
|join | `a * b` | Contains all possible pairs of matching tuples from `a` and `b` merged together. This operator is known in classical relational algebra as *natural inner join*. If `a` and `b` are relations with the same headings, join becomes equivalent to set intersection.
|union | `a + b` | Contains all tuples and all attributes from both `a` and `b`.  This operator is known in classical relational algebra as *natural full outer product*. When `a` and `b` are relations with the same heading, it becomes equivalent to set union.   
|projection | `a.proj(...)` | Contains the same tuples but with some attributes removed or renamed or new attributes computed.  Primary key attributes cannot be removed but may be renamed.
|aggregation | | `a.aggr(b, ...)` | Similar to projection but allows computing new attributes in the form of aggregation operations on matching tuples from relation `b`.

