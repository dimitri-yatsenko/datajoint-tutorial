# Example: "The Experiment"

## Scenario

Three intrepid scientists Alice, Bob, and Carol are embarking on a series of groundbreaking experiments.

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
Here we provide Python functions that will simulate the data acquisition and analysis.  Provided here only for completeness, they are not part of the main discussion.

```python
# Preliminaries:
# This section provides functions that will be used by your project.
import numpy as np
import time
from scipy import ndimage


def make_image(seed=None, ncells=100, size=256):
    """
    make blob image
    """
    np.random.seed(seed)
    im = np.zeros((size, size))
    points = (size*np.random.random((2, ncells))).astype(np.int)
    im[points[0], points[1]]= 1 + 0.1*np.random.normal(size=ncells)
    return ndimage.gaussian_filter(im, sigma=size/(6.*np.sqrt(ncells)))


class BlobFail(Exception):
    pass


def find_blobs(im, fail_rate=0.01):
    """
    Generates x, y coordinates of blobs detected in image im.
    Intentionally fails (raises BlobFail) randomly at fail_rate.
    """
    for y, x in zip(*np.where(
            im > ndimage.filters.percentile_filter(im, 85, size=3))):
        if np.random.random() < fail_rate:
            print("Fail!", flush=True)
            raise BlobFail
        yield x, y
```

### Create database and declare tables 
First, let's create the database called `blobs`:

```python
import datajoint as dj
schema = dj.schema('blobs', locals())
```

### `Scientist` and `Experiment`
Now, let's create the table `Scientist` so that we can refer to individual scientists later.  We will populate it implicitly using the `contents` property.  The table is of type `dj.Lookup`, suggesting that its information is rather static, not meant to be entered for each experiment.

```python
@schema
class Scientist(dj.Lookup):
    definition = """    # scientists in the lab
    name : varchar(8)   # scientist name
    """
    contents = [['Alice'], ['Bob'], ['Carol']]
```

The `definition` property defines the structure of the table.  The first line contains the table comment, describing what information is represented by rows in the table.  This table only has one attribute (column) `name` of type variable-length character string up to 8 characters `varchar(8)`.  The column also has a comment describing its meaning.

Now let's define the `Experiment` table containing the information about a day's experiment.

```python
@schema
class Experiment(dj.Manual):
    definition = """ # daily experiment
    exp_date : date   # experiment date
    ---
    -> Scientist
    notes="" : varchar(255)  # free notes about the experiment
    """
```

The `Experiment` table is of type `dj.Manual`, suggesting that it contains information entered manually in each experiment.

Its definition contains a dividing line `---`.  The attributes above the dividing line comprise the table's *primary key*.  No two entries in a table can have the same values of the primary key attributes.  The primary key attributes are also  indexed to speed up searches by their values.  For our `Experiment`, it means that `exp_date` is the most efficient way to identify experiments.

The definition also contains the reference `-> Scientist`.  This reference pastes the primary key attributes of `Scientist` into the definition of `Experiment`.  The primary key of `Scientist` is `name`.  This reference also sets a *foreign key* constraint, which prevents entering any values that are not also present in the referenced table.

Finally, `Experiment` contains the attribute `notes` of type `varchar(255)`.  The definition also specifies its default value, the empty string  `""`.

Thus `Experiment` has attributes `exp_date`, `name`, and `notes`.
