from model.module import Module, Difficulty, SpecificClass
import fake.module as data

def get_all()->list[Module]:
    return data.get_all()

def get_by_id(id:int)->Module:
    return data.get_by_id(id)   

def create(module:Module)->Module:
    return data.create(module)

def replace(id:int,module:Module)->Module:
    return data.modify(id,module)

def modify(id:int,module:Module)->Module:
    return data.modify(id,module)

def delete(id:int)->bool:
    return data.delete(id)

