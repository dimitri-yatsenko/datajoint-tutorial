class Experiment(dj.Manual):
    definition = """ # daily experiment
    exp_date : date   # experiment date
    --- 
    -> Scientist
    notes="" : varchar(255)  # free notes about the experiment
    """
