from fastapi.testclient import TestClient
from ..main import app
import json
import io

client = TestClient(app)


def test_generate_lecture():
    # Prepare the lecture metadata
    lecture_metadata = {
        "lecture_title": "Lecture 11",
        "course_name": "Dynamics",
        "course_code": 103,
        "instructor_name": "Thomas Stahovich",
        "lecture_date": "2025-05-01",
        "semester": "Spring 2025",
    }

    # Combine metadata with the separate_image flag
    lecture_input = {"separate_image": True, "lecture_metadata": lecture_metadata}

    # Serialize the lecture_input to a JSON string
    lecture_data_json = json.dumps(lecture_input)

    # Create a dummy PDF file in memory
    dummy_pdf_content = b"%PDF-1.4\n%Dummy PDF content"
    dummy_pdf_file = io.BytesIO(dummy_pdf_content)
    dummy_pdf_file.name = "dummy.pdf"  # Set a name attribute to mimic an uploaded file

    # Prepare the files dictionary for the multipart/form-data request
    files = {"files": ("dummy.pdf", dummy_pdf_file, "application/pdf")}

    # Prepare the form data
    data = {"lecture_data": lecture_data_json}

    # Send the POST request to the endpoint
    response = client.post("/v2/lecture_processor", data=data, files=files)

    # Assert the response status code
    assert response.status_code == 200

    # Print the response JSON for inspection
    print(response.json())
