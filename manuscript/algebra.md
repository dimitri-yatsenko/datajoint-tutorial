## Relational operators
Queries have the form of expressions using operators to derive the desired relation.  The expressions themselves do not contain any data.  They represent the desired data symbolically. 

Once a query is formed, the `fetch` methods are used to bring the data into the MATLAB or Python workspace.  Since the expressions are only symbolic representations, repeated `fetch` calls may yield different results as the state of the database is modified.



DataJoint implements a complete algebra of operators on relations:

{title="Summary of relational operators"}
| operator | notation
|:--|:--|
| restriction | `A & cond` |
| difference  | `A - cond` |
| join        | `A * B`    | 
| union       | `A + B`    | 
| projection  | `A.proj(...)` | 
| aggregation | `A.aggr(B, ...)` | 


## Principles of relational algebra
DataJoint's relational algebra improves upon the classical relational algebra and upon other query languages to simplify and enhance the construction and interpretation of precise and efficient data queries.

The clarity of DataJoint's query expressions stems from the concept of *entity integrity*.  Entity integrity states that every relation must have a well-define *primary key*.  Normally, this concept is only applied to *base relation*, which store the data in the database.  DataJoint goes further by extending entity integrity to all relation, including *derived relations*.


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
This is a matching pair of tuples:

![](images/matched_tuples1.png)

and so is this one:

![](images/matched_tuples2.png)

but these tuples do *not* match:

![](images/matched_tuples3.png)

## Join compatibility
All binary operators with other relations as its two operands require that their operands be *join-compatible*, which means that:

1. All common attributes in both operands (attributes with the same name) must be part of the primary key or of a foreign key.
2. All common attributes in the two relations must be of a compatible datatype for equality comparisons.

These restrictions are introduced both for performance reasons and for conceptual reasons.  For  performance, they encourage queries that rely on indexes.  For conceptual reasons, they encourage database design in which entities in different relations are lated to each other by the use of primary keys and foreign keys.
