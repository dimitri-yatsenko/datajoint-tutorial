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


## Python  implementation 

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

