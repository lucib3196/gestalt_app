tag_replacer_configs = {
    "pl_question_panel": {
        "target_tag": "pl-question-panel",
        "replacement_tag": "div",
        "attributes": {
            "class": "card mb-4 p-3 bg-light"
        },
        "mapping": {}
    },
    "pl_checkbox": {
        "target_tag": "pl-checkbox",
        "replacement_tag": "fieldset",
        "attributes": {
            "class": "form-check mb-3"
        },
        "mapping": {
            "answers-name": "answers-name",
            "weight": "data-weight",
            "inline": "data-inline"
        }
    },
    "pl_answer": {
        "target_tag": "pl-answer",
        "replacement_tag": "input",
        "attributes": {
            "type": "checkbox",
            "class": "form-check-input me-2"
        },
        "mapping": {
            "correct": "data-correct"
        }
    },
    "pl_number_input": {
        "target_tag": "pl-number-input",
        "replacement_tag": "input",
        "attributes": {
            "type": "number",
            "size": "50",
            "value": "",
            "step": "any",
            "class": "form-control mb-2"
        },
        "mapping": {
            "answers-name": "answers-name",
            "id": "answers-name",
            "comparison": "comparison",
            "digits": "digits",
            "label": "label"
        }
    },
    "pl_solution_panel": {
        "target_tag": "pl-solution-panel",
        "replacement_tag": "div",
        "attributes": {
            "class": "alert alert-info p-3"
        },
        "mapping": {}
    },
    "pl_hint": {
        "target_tag": "pl-hint",
        "replacement_tag": "div",
        "attributes": {
            "class": "alert alert-warning p-3"
        },
        "mapping": {
            "data-type": "data-type",
            "level": "data-level"
        }
    },
    "pl_multiple_choice": {
        "target_tag": "pl-multiple-choice",
        "replacement_tag": "fieldset",
        "attributes": {
            "class": "card p-3 mb-3"
        },
        "mapping": {
            "answers-name": "answers-name",
            "inline": "data-inline",
            "weight": "data-weight"
        }
    },
    "pl_text_input": {
        "target_tag": "pl-text-input",
        "replacement_tag": "input",
        "attributes": {
            "type": "text",
            "size": "50",
            "value": "",
            "class": "form-control mb-2"
        },
        "mapping": {
            "answers-name": "answers-name",
            "label": "aria-label"
        }
    },
    "pl_figure": {
        "target_tag": "pl-figure",
        "replacement_tag": "img",
        "attributes": {
            "alt": "Picture for problem",
            "width": "300",
            "height": "300",
            "class": "img-fluid mx-auto d-block mb-3"
        },
        "mapping": {
            "file-name": "src"
        }
    },
    "pl_input_field": {
        "target_tag": "pl-input-field",
        "replacement_tag": "input",
        "attributes": {
            "type": "number",
            "size": "50",
            "value": "",
            "step": "any",
            "class": "form-control mb-2"
        },
        "mapping": {
            "variable-name": "name",
            "id": "variable-name",
            "label": "aria-label",
            "placeholder": "placeholder"
        }
    },
    "pl_input_panel": {
        "target_tag": "pl-input-panel",
        "replacement_tag": "div",
        "attributes": {
            "class": "card p-3 mb-3"
        },
        "mapping": {}
    }
}
