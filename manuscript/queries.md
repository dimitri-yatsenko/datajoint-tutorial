# Queries 

## Forming a query

Data queries in DataJoint have the following form (in both MATLAB and Python):

```matlab
data = rel.fetch()
```

where `rel` is a relation object (a *base relation* or a *derived relation*); whereas `fetch` is one of several variants of fetch methods.  

In MATLAB, the more flexible syntax is 

```matlab
data = fetch(rel)
```

Relation objects are only symbolic representations of the data.  They allow a quick preview but do not contain the data itself.  Hence, repeated executions of the `fetch` method may yield different results as the state of the database changes.

The `fetch` methods transfer the desired data from the database to the namespace of the host language.

The relational expressions have very similar syntax and meaning in MATLAB, Python, and `dj2sql`. The `fetch` methods have several variations and parameters that are specific to the host language.

## Base relations
In simplest queries, `rel` is a *base relation* representing a table in the database.  Each table has a dedicated class in the host language.

For example, the following code fetches the entire contents of the table represented by class `experiment.Image`:

{title="Getting all data from `experiment.Image` in Python", lang=python}
~~~~~~~~~
rel = experiment.Image()
data = rel.fetch()    
~~~~~~~~~

{title="Getting all data from `experiment.Image` in MATLAB", lang=matlab}
~~~~~~~~~
rel = experiment.Image;
data = rel.fetch('*');
~~~~~~~~~

