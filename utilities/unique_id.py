import uuid

"""
purpose: to always crate a unique id for each user
parameters: 
    nothing
output: "1408CEAD-3EF2-4978-A376-05DEDC1C8E14"
"""    
def create_uuid():
    random_uuid = uuid.uuid4()
    print(random_uuid)
    return random_uuid

create_uuid()