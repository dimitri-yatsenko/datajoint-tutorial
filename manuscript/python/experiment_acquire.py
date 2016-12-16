import numpy as np

@schema
class Acquire(dj.Imported):
    definition = """   # Image data from one experiment
    -> Experiment
    ---
    timestamp = CURRENT_TIMESTAMP  : timestamp
    """

    class Image(dj.Part):
        definition = """
        -> Acquire
        image_id : tinyint unsigned   # image number within each experiment
        ---
        image : longblob  # acquired image
        """

    def _make_tuples(self, key):
        print('Populating', key)
        self.insert1(key)
        number_of_images = np.random.randint(20)
        part = self.Image()
        for i in range(number_of_images):
            print(end='.')
            part.insert1(
                dict(key, image_id=i, image=make_image()))
        print('done')
