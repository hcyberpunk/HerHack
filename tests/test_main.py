import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "hello.html" in response.text


def test_get_students():
    response = client.get("/index")
    assert response.status_code == 200
    assert "index.html" in response.text


def test_create_student():
    response = client.get("/student")
    assert response.status_code == 200
    assert "create-student.html" in response.text

    # Test student creation with a POST request
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "checkintime": "2022-01-01",
    }
    response = client.post("/student", data=data)
    assert response.status_code == 200
    assert "create-student.html" in response.text

    # Test student creation with invalid data (missing required fields)
    invalid_data = {
        "lastname": "Doe",
        "checkintime": "2022-01-01",
    }
    response = client.post("/student", data=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_update_student_lastname():
    # Test updating student lastname with a PUT request
    student_id = 1
    data = {
        "lastname": "Smith",
    }
    response = client.put(f"/changelastname/{student_id}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": f"Last name of student with ID {student_id} updated successfully."}


def test_update_student_firstname():
    # Test updating student firstname with a PUT request
    student_id = 1
    data = {
        "firstname": "Jane",
    }
    response = client.put(f"/changefirstname/{student_id}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": f"First name of student with ID {student_id} updated successfully."}


def test_delete_student():
    # Test deleting a student with a DELETE request
    student_id = 1
    response = client.delete(f"/deletestudent/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Student with ID {student_id} has been deleted."}

    # Test deleting a non-existent student
    invalid_student_id = 999
    response = client.delete(f"/deletestudent/{invalid_student_id}")
    assert response.status_code == 404  # Not Found


# Run the tests
if __name__ == "__main__":
    pytest.main()
