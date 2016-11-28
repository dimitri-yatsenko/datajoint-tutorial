# Critique of SQL

If you are new to database programming and your mind has not been polluted with SQL, you should skip this section. 

This section assumes essential familiarity with SQL and the relational database theory.  We do not introduce SQL basics but rather clarify why DataJoint needed to introduce its own data definition and manipulation languages.  We also hope to convince the reader that DataJoint is a far superior way to interact with data than SQL.  Furthermore, this section might help SQL programmers unlearn some SQL concepts and habits that contradict DataJoint's approach.

So why not just use the good ol' SQL?


## SQL is not quite relational

### Relational Data Model
Relational databases rest on the foundation of the **Relational Data Model** (RDM).
In RDM, all data are manipulated in the form of **relations** --- a mathematical construct from the theory of sets.  Defined formally, a relation is a subset of the Cartesian product of several **domains**.   The elements of a relations are called **tuples** and the elements of tuples, drawn from each domain, are called **attributes**.  Rather than identifying attributes by their position in the tuple, it is common to identify them by names corresponding to each domain.

### Relational algebras
A set of operators are defined to produce new **derived relations** from a given collection of **base relations**.  Together these operators comprise a **relational algebra**.  Operators in a relational algebra accept relations and yield relations.  Known as **algebraic closure**, this property makes relational algebras flexible for building new queries from existing simple queries.

Formal relational algebras may be used as query languages to precisely define the exact slice of the data requested by the query.  DataJoint's query language is one such algebra carefully designed for maximum clarity and explicitness. 


### SQL falls short 
SQL is rather unique among computer programming languages in its overwhelming dominance of an entire popular computational concept: the relational data model.  Many historical reasons have led to this monopolization, including standardization of SQL by regulatory agencies and deference to the early authorities of the relational data model who defined the tenets of a relational query language.

Surprisingly, SQL is not a particularly faithful incarnation of the relational data model nor is it meant to be.  Because it deviates from the relational model, SQL uses a different terminology with the terms **table**, **row**, and **column** loosely corresponding to the respective terms *relation*, *tuple*, and *attribute* from the relational data model.  

In SQL, tables are not sets in the mathematical sense: they may contain duplicate entries. 
The result of an SQL query or subquery may have the form of another table, or a single row, or a scalar value.  

In SQL, subqueries and views emulate algebraic closure.  Yet they fall short of true algebraic closure.  Subqueries may not be assigned to named variables for incremental buildup of a complex query.  As a result, SQL queries with subqueries tend to grow in size and complexity.  Although views are meant to fill the role of named derived relations, they are a rather heavy construct that cannot be easily defined on demand mid-transaction.  The creation of a query typically may evoke an implicit commit of the current transaction, for example.

Rather than using a set of relational operators, SQL queries take the form of a `SELECT` statement which combines into one several relational operators: project, rename, extend, restrict, aggregate, and restrict again.  This design choice may reflect the 1970s' vision of future programming languages as having the form of English sentences.  Although SQL queries do read like English prose, they may lack the succinctness and clarity of algebraic expressions.

SQL and most relational algebras do not have a consistent way by which attributes (columns) are identified in relational operators and their results.  In some cases, attributes (columns) are identified by names and sometimes by their position in the result.  Some computed columns may not have a well-defined name and sometimes duplicate names appear which must be resolved by prefixing the name of the table or subquery from which each originates.

SQL usually has multiple ways of expressing logically equivalent queries, sometimes with considerable differences in performance.  For example, *correlated subqueries* are often highly inefficient and may often be re-written as more efficient join queries.

## DataJoint's philosophy

### Scrupulously relational

DataJoint adheres faithfully to the relational data model. *All* DataJoint relations, including *base relations* (tables) and *derived relations* (results of expressions) are proper relations (sets of tuples) with a well-defined primary key and unambiguous attribute names.

### Entity integrity
*Entity integrity* in relational database design stems from the understanding that each relation represents either a class of entities or or a relationship between classes of entities in the model universe.  As such, each relation must clearly identify each entity.  The *entity integrity constraint* therefore states that every relation must have a primary key and NULLs are not allowed in primary key attributes. 

Such constraints ensure entity integrity in the base relations 


### Algebraic closure
DataJoint's operators 

### Simplified algebra

### Sensible restrictions


