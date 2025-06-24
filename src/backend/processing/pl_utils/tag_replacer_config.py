tag_replacer_configs = {
    "pl_question_panel": {
        "target_tag": "pl-question-panel",
        "replacement_tag": "div",
        "attributes": {"class": "pl-question-panel"},
        "mapping": {},
    },
    "pl_question_panel": {
        "target_tag": "pl-question-panel",
        "replacement_tag": "div",
        "attributes": {"class": "pl-question-panel"},
        "mapping": {},
    },
    "pl_checkbox": {
        "target_tag": "pl-checkbox",
        "replacement_tag": "fieldset",
        "attributes": {"class": "pl-checkbox"},
        "mapping": {
            "answers-name": "answers-name",
            "weight": "data-weight",
            "inline": "data-inline",
        },
    },
    "pl_answer": {
        "target_tag": "pl-answer",
        "replacement_tag": "input",
        "attributes": {"type": "checkbox", "class": "pl-answer"},
        "mapping": {
            "correct": "data-correct",
            "label": "label",
        },
    },
    "pl_number_input": {
        "target_tag": "pl-number-input",
        "replacement_tag": "input",
        "attributes": {
            "type": "number",
            "size": "50",
            "value": "",
            "step": "any",
            "class": "pl-number-input",
        },
        "mapping": {
            "answers-name": "name",
            "id": "id",
            "comparison": "comparison",
            "digits": "digits",
            "label": "label",
        },
    },
    "pl_solution_panel": {
        "target_tag": "pl-solution-panel",
        "replacement_tag": "div",
        "attributes": {"class": "pl-solution-panel"},
        "mapping": {},
    },
    "pl_hint": {
        "target_tag": "pl-hint",
        "replacement_tag": "div",
        "attributes": {"class": "pl-hint"},
        "mapping": {"data-type": "data-type", "level": "data-level"},
    },
    "pl_multiple_choice": {
        "target_tag": "pl-multiple-choice",
        "replacement_tag": "fieldset",
        "attributes": {"class": "pl-multiple-choice"},
        "mapping": {
            "answers-name": "answers-name",
            "inline": "data-inline",
            "weight": "data-weight",
        },
    },
    "pl_text_input": {
        "target_tag": "pl-text-input",
        "replacement_tag": "input",
        "attributes": {
            "type": "text",
            "size": "50",
            "value": "",
            "class": "pl-text-input",
        },
        "mapping": {"answers-name": "name", "label": "aria-label"},
    },
    "pl_figure": {
        "target_tag": "pl-figure",
        "replacement_tag": "img",
        "attributes": {
            "alt": "Picture for problem",
            "width": "300",
            "height": "300",
            "class": "pl-figure",
        },
        "mapping": {"file-name": "src"},
    },
    "pl_input_field": {
        "target_tag": "pl-input-field",
        "replacement_tag": "input",
        "attributes": {
            "type": "number",
            "size": "50",
            "value": "",
            "step": "any",
            "class": "pl-input-field",
        },
        "mapping": {
            "variable-name": "name",
            "id": "variable-name",
            "label": "aria-label",
            "placeholder": "placeholder",
        },
    },
    "pl_input_panel": {
        "target_tag": "pl-input-panel",
        "replacement_tag": "div",
        "attributes": {"class": "pl-input-panel"},
        "mapping": {},
    },
    # Solution Panel Config
    "pl_solution_panel": {
        "target_tag": "pl-solution-panel",
        "replacement_tag": "div",
        "attributes": {"class": "solution-panel"},
        "mapping": {},
    },
    "pl_hint": {
        "target_tag": "pl-hint",
        "replacement_tag": "div",
        "attributes": {"class": "solution-step hidden-step"},
        "mapping": {"level": "data-level", "data-type": "data-type"},
        "wrap_with_button": True,  # <-- Custom flag for rendering logic
    },
}
