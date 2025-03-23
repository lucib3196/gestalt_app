from model.module import Module, Difficulty,SpecificClass
from pydantic import BaseModel, Field
from typing import Optional,List


fake_modules: List[Module] = [
    Module(
        id=1,
        title="Thermal Expansion of Rods",
        topic="Thermodynamics",
        subtopic="Thermal Expansion",
        question="A steel rod of length 2 m is heated from 20°C to 100°C. Calculate the expansion.",
        solution_summary="Using the formula ΔL = αLΔT, we find the change in length.",
        difficulty=Difficulty.EASY,
        tags=["thermal", "expansion", "materials"],
        has_diagram=False,
        created_by="student123",
        reviewed=True,
        specific_class=[
            SpecificClass(
                id=101,
                class_name="ME201 - Thermodynamics I",
                professor="Dr. Smith",
                class_description="Introduction to basic thermodynamic concepts and laws."
            )
        ]
    ),
    Module(
        id=2,
        title="Free Body Diagram of a Beam",
        topic="Statics",
        subtopic="Beams and Supports",
        question="Draw and analyze the FBD of a simply supported beam with a central point load.",
        solution_summary="The beam has two reactions. Use equilibrium equations to solve for the unknowns.",
        difficulty=Difficulty.MEDIUM,
        tags=["FBD", "statics", "beams"],
        has_diagram=True,
        created_by="prof_alex",
        reviewed=False,
        specific_class=[
            SpecificClass(
                id=102,
                class_name="ME101 - Engineering Mechanics",
                professor="Prof. Alex Johnson",
                class_description="Covers statics, forces, and moments in mechanical systems."
            ),
            SpecificClass(
                id=103,
                class_name="ENGR101",
                professor=None,
                class_description="Introductory engineering course with a focus on mechanical applications."
            )
        ]
    ),
    Module(
        id=3,
        title="Internal Energy in a Piston System",
        topic="Thermodynamics",
        subtopic="First Law of Thermodynamics",
        question="A gas expands in a piston-cylinder system doing 200 J of work. The heat added is 500 J. Find the change in internal energy.",
        solution_summary="Use the first law: ΔU = Q - W. Substituting gives ΔU = 300 J.",
        difficulty=Difficulty.HARD,
        tags=["first law", "piston", "energy balance"],
        has_diagram=True,
        created_by="engineer_kate",
        reviewed=True,
        specific_class=[]
    )
]

def get_all()->List[Module]:
    return fake_modules

def get_by_id(id:int)->Module:
    for module in fake_modules:
        if module.id == id:
            return module
    return None

def create(module:Module)->Module:
    module.id = len(fake_modules) + 1
    fake_modules.append(module)
    return module

def modify(id:int,module:Module)->Module:
    for i, m in enumerate(fake_modules):
        if m.id == id:
            fake_modules[i] = module
            return module
    return None

def delete(id:int)->bool:
    for i, m in enumerate(fake_modules):
        if m.id == id:
            del fake_modules[i]
            return True
    return False