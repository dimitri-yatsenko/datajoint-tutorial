# Example: "Mysterious blobs"

## Scenario
The intrepid scientists Alice, Bob, and Carol are embarking on a series of groundbreaking experiments.

Acquisition 

: Only one experiments can be done on the same date and only one of the scientists conducts the experiment for that day. In each experiment, the experimenter acquires several grayscale images of mysterious blobs, like so:

![Mysterious blobs](images/blobs.png)

Analysis 

: The analysis detects the blobs in the image and reports their (x,y) positions and amplitudes, like so:

![Blob detection](images/crosses.png)

Report

: Their report will print the number of experiments that a given scientist has conducted, the percentage of images that have been analyzed for that scientist, the average number of blobs per image for that scientist, and the average amplitude of blobs for that scientist.


## Python solution

### Preliminaries
The following Python functions simulate the data acquisition and analysis.  Provided here only for completeness, they are not part of the main discussion.

<<[Preliminary functions](python/experiment_preliminaries.py)

### Create database and declare tables 
First, let's create the database called `blobs`:

{line-numbers=off, lang=python}
~~~~~~~
import datajoint as dj
schema = dj.schema('blobs', locals())
~~~~~~~

### `Scientist` and `Experiment`
Now, let's create the table `Scientist` so that we can refer to individual scientists later.  We will populate it implicitly using the `contents` property.  The table is of type `dj.Lookup`, suggesting that its information is rather static, not meant to be entered for each experiment.

<<[Declare the Scientist table](python/experiment_scientist.py)

The `definition` property defines the structure of the table.  The first line contains the table comment, describing what information is represented by rows in the table.  This table only has one attribute (column) `name` of type variable-length character string up to 8 characters `varchar(8)`.  The column also has a comment describing its meaning.

Now let's define the `Experiment` table containing the information about a day's experiment.

<<[Declare the Experiment table](python/experiment_experiment.py)

The `Experiment` table is of type `dj.Manual`, suggesting that it contains information entered manually in each experiment.

Its definition contains a dividing line `---`.  The attributes above the dividing line comprise the table's *primary key*.  No two entries in a table can have the same values of the primary key attributes.  The primary key attributes are also  indexed to speed up searches by their values.  For our `Experiment`, it means that `exp_date` is the most efficient way to identify experiments.

The definition also contains the reference `-> Scientist`.  This reference pastes the primary key attributes of `Scientist` into the definition of `Experiment`.  The primary key of `Scientist` is `name`.  This reference also sets a *foreign key* constraint, which prevents entering any values that are not also present in the referenced table.

Finally, `Experiment` contains the attribute `notes` of type `varchar(255)`.  The definition also specifies its default value, the empty string  `""`.

Thus `Experiment` has attributes `exp_date`, `name`, and `notes`.
You may confirm this by previewing the table's `heading`:

{lang=python}
~~~~~~~~~
>>> Experiment().heading
# daily experiments
exp_date             : date                         # experiment date
---
name                 : varchar(8)                   # scientist name
notes=""             : varchar(255)                 # free notes about the experiment
~~~~~~~~~

You may also get a quick preview of the contents of the tables:

~~~~~~~~~
>>> Scientist()

scientists in the lab
*name
+-------+
Alice
Bob
Carol
 (3 tuples)
```

{line-numbers=off}
```
>>>  Experiment()

daily experiments
*exp_date    name     notes
+----------+ +------+ +-------+

 (0 tuples)
~~~~~~~~~

The primary key attributes are indicated with an asterisk `*`.

### Entering expriment data
Let's pretend to conduct some experiments by entering data into `Experiments`:

{lang=python}
~~~~~~~~~~~
e = Experiment()

# enter one at a time
e.insert1(dict(exp_date="2016-10-01", name="Carol", notes="awesome data!"))
e.insert1(dict(exp_date="2016-10-02", name="Bob"))
e.insert1(('2016-10-03', 'Alice', 'found a piece of dark matter.'))

# enter several
e.insert((
        ("2016-10-04", "Carol", "stunning!"),
        ("2016-10-05", "Bob", "inexplicable patterns."),
        ("2016-10-06", "Alice", "A boson got loose.")
    ))
~~~~~~~~~~~

Note that the insert

{lang=python}
~~~~~~~~~~~
>>> Experiment().insert1(['2016-10-01', 'Bob', 'I have a bad feeling about this.'])

pymysql.err.IntegrityError: (1062, "Duplicate entry '2016-10-01' for key 'PRIMARY'")
~~~~~~~~~~~
fails because the entry for `2016-10-01` already exists.

The insert

{lang=python}
~~~~~~~~~~~
>>> Experiment().insert1(['2016-10-07', 'Alce', ''])
~~~~~~~~~~~

will fail because the name `Alce` is misspelled and is not found in `Scientist`.

If the `insert` method is used to enter multiple entries at once and any one of the entries is invalid, then none of the entries are inserted.


### Acquisition
Let's now define the table `Acquire` to acquire the results of experiments.

<<[Declare the Acquire table](python/experiment_acquire.py)

Let's unpack what is  going on here.

We defined two new tables `Acquire` and `Acquire.Image`.

`Acquire` makes a foreign key reference to `Experiment` from its primary key and has no other attributes in its primary key.  This means that `Acquire` has a 1:1 relationship to `Experiment`: at most one `Acquire` entry can exist for every `Experiment` entry.

`Acquire` also has the attribute `timestamp` of type `timestamp` and default value of `CURRENT_TIMESTAMP`.

`Acquire` is of type `dj.Imported`, which suggests that its data are populated automatically but by require access to data outside the datajoint database.  The other automatic table type is `dj.Computed`, which work similarly to `dj.Imported` and only use data upstream in the data pipeline already in the database.

The automatic acquisition is performed by calling its `populate` method:

```python
>>> Acquire().populate()
```

    Populating: {'exp_date': datetime.date(2016, 10, 3)}
    ......done
    Populating: {'exp_date': datetime.date(2016, 10, 6)}
    .......done
    Populating: {'exp_date': datetime.date(2016, 10, 2)}
    ...................done
    Populating: {'exp_date': datetime.date(2016, 10, 5)}
    .......done
    Populating: {'exp_date': datetime.date(2016, 10, 1)}
    .................done
    Populating: {'exp_date': datetime.date(2016, 10, 4)}
    .....done



### Analysis
Now let's write the classes `Localize` and `Localize.Blob` that compute the (x,y) locations and amplitudes detected blobs in each image.  They rely on the function `find_blobs` defined earlier. Note that function fails randomly (raises the `BlobFail` exception) to illustrate error recovery.

<<[Declare the Detect table](python/experiment_detect.py)

Similar to `Acquire`, we populate the `Localize` table using the populate method but we set the `suppress_errors` flag to skip the errors that occur in the `_make_tuples` calls:

```python
>>> Localize().populate(suppress_errors=True);
```


    Populating: {'exp_date': datetime.date(2016, 10, 1), 'image_id': 3}
    done
    Populating: {'exp_date': datetime.date(2016, 10, 1), 'image_id': 5}
    done
    Populating: {'exp_date': datetime.date(2016, 10, 1), 'image_id': 7}
    Fail!
                    .
                    .
                    .

    Populating: {'exp_date': datetime.date(2016, 10, 6), 'image_id': 1}
    done
    Populating: {'exp_date': datetime.date(2016, 10, 6), 'image_id': 4}
    done
    Populating: {'exp_date': datetime.date(2016, 10, 6), 'image_id': 5}
    Fail!

We can view the progress of the calculation using the `progress` method:

```python
>>> Localize().progress();
```

   Localize             Completed 32 of 68 (47.1%)   2016-11-21 15:55:32

This shows that 32 of 68 images have populated without errors.  Those that ended in error, were rolled back.  You can execute `populate` again to complete the remaining jobs.

The execution may take some time because each blob is inserted individually, incurring network delays.  We can re-write the `_make_tuples` method to insert into the part table as a single insert, resulting in substantial speedup:

<<[More efficient Detect](python/experiment_detect2.py)

The decision when to enter data as a sequence of `insert1` or a single `insert` must be made individually.  When network delays are negligible compared to the computation times, then inserting one tuple at a time with `insert1` may be preferable because the data are sent to the database as they are computed rather than queued in memory.

### Visualizing the schema
At any point, you may visualize the entire schema using the `dj.ERD` class:

```python
>>> dj.ERD(schema).draw()
```

![](images/erd1.png)

The ERD (entity-relationship diagram) shows all the classes as nodes, color-coded (gray=lookup, green=manual, blue=imported, red=computed, small font=part tables)

## Queries
Let's illustrate a few queries for the results that.

Query: All scientists who have done at least one experiment:

```python
Scientist() & Experiment()
```

Query: All scientists who have not done any experiments:

```python
Scientist() - Experiment()
```

Query: Experiment performed by Alice

```python
Experiment() & {'name' : 'Alice'}
```

Query: Images collected by Alice:

```python
Acquire.Image() & (Experiment() & {'name': 'Alice'})
```

This may be broken up into subqueries:

```python
alices = Experiment() & {'name': 'Alice'}
Acquire.Image() & alices
```

Query: Images with the experiment information included:

```python
Acquire.Image() * Experiment()
```

Query: The number of experiments performed by each scientist:

```python
Scientist().aggr(Experiment(), n='count(exp_date)')
```

Query: The number of experiments performed by Alice:

```python
Scientist().aggr(Experiment(), n='count(exp_date)') & {'name': 'Alice'}
```

Query: Number of images acquired by each scientist:

```python
images = Experiment()*Acquire.Image()   # images with user names
Scientist().aggr(images, n='count(image_id)')
```

Query: Number of images analyzed for each scientist:

```python
images = Experiment()*Localize()   # processed images with user names
Scientist().aggr(images, n='count(image_id)')
```

Query: fraction of images processed for each scientist

```python
analyzed = Scientist().aggr(Experiment()*Localize(), m='count(image_id)')
acquired = Scientist().aggr(Experiment()*Acquire.Image(), n='count(image_id)')

pcent_analyzed=(analyzed*acquired).proj(pcent = '100*m/n')
```

### Equivalent SQL
For each of the above queries, invoke the `make_sql` method to see the resulting SQL code:

```python
>>> pcent_analyzed.make_sql()
```

```sql
SELECT * FROM (
    SELECT `name`, 100*m/n as `pcent`
    FROM (
        SELECT `name`, count(image_id) as `m`
        FROM `tutorial`.`scientist` NATURAL JOIN
            `tutorial`.`experiment` NATURAL JOIN
            `tutorial`.`__localize` GROUP  BY `name`) as `_s8a`
    NATURAL JOIN (
        SELECT `name`,count(image_id) as `n`
        FROM `tutorial`.`scientist` NATURAL JOIN
             `tutorial`.`experiment` NATURAL JOIN
             `tutorial`.`_acquire__image` GROUP  BY `name`) as `_s8b`
    ) as `_s8c`
```

