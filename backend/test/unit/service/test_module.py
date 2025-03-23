from model.module import Module
from service import module as code

sample = Module(
    id=1,
    title="Sample Module",
    topic="Sample Topic",
    specific_class=[],
    subtopic="Sample Subtopic",
    question="Sample Question",
    solution_summary="Sample Solution Summary",
    difficulty="easy",
    tags=["sample", "test"],
    has_diagram=False,
    created_by="Sample User",
    reviewed=False
)

def test_create():
    resp = code.create(sample)
    assert resp == sample
    
def test_get_exist():
    resp = code.get_by_id(1)
    assert resp == sample
    
def test_get_missing():
    resp = code.get_by_id(4)
    assert resp == None
    