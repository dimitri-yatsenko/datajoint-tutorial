@schema 
class Scientist(dj.Lookup):
    definition = """    # scientists in the lab
    name : varchar(8)   # scientist name
    """    
    contents = [['Alice'], ['Bob'], ['Carol'], ['Dave']]
