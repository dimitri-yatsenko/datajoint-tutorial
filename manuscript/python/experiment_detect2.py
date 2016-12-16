@schema
class Localize(dj.Computed):
    definition = """   # Image data from one experiment
    -> Acquire.Image
    """

    class Blob(dj.Part):
        definition = """
        -> Localize
        blob_id : tinyint unsigned   # blob within each image
        ---
        x : float  # x-coordinate
        y : float  # y-coordinate
        amplitude : float  # blob intensity at (x,y)
        """

    def _make_tuples(self, key):
        print('Populating:', key)
        self.insert1(key)
        img = (Acquire.Image() & key).fetch1['image']
        self.Blob().insert((
                dict(key, blob_id=i, x=x, y=y, amplitude=img[y,x])
                for i, (x, y) in enumerate(find_blobs(img))
            ))
        print('done')
