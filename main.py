import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from fastapi import HTTPException

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Establish connection to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()


@app.on_event("shutdown")
def shutdown_event():
    # Close the database connection on application shutdown
    conn.close()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


@app.get("/index", response_class=HTMLResponse)
async def get_students(request: Request):
    # Fetch the data from the database
    cursor.execute("SELECT firstname, lastname, checkintime FROM students")
    rows = cursor.fetchall()

    # Convert the fetched data to a list of dictionaries
    records = [{'firstname': row[0], 'lastname': row[1], 'checkintime': row[2]} for row in rows]

    return templates.TemplateResponse("index.html", {"request": request, "records": records})


@app.route("/student", methods=["GET", "POST"])
async def create_student(request: Request):
    if request.method == "GET":
        # Handle GET request for student creation form
        return templates.TemplateResponse("create-student.html", {"request": request})
    elif request.method == "POST":
        # Handle POST request to create a new student
        form_data = await request.form()
        # Process the form data and insert into the database
        # ...
        # Return the appropriate response
        firstname = form_data.get("firstname")
        lastname = form_data.get("lastname")
        checkintime = form_data.get("checkintime")

        # Insert the new student record into the database
        cursor.execute("INSERT INTO students (firstname, lastname, checkintime) VALUES (?, ?, ?)",
                       (firstname, lastname, checkintime))
        conn.commit()
        return templates.TemplateResponse("create-student.html", {"request": request})

@app.put("/changelastname/{student_id}")
async def update_student(request: Request, student_id: int):
    data = await request.json()
    lastname = data.get("lastname")

    # Update the last name of the student with the given student_id in the database
    cursor.execute("UPDATE students SET lastname = ? WHERE id = ?", (lastname, student_id))
    conn.commit()

    # Return the updated student record or a success message
    return {"message": f"Last name of student with ID {student_id} updated successfully."}


@app.put("/changefirstname/{student_id}")
async def update_student(request: Request, student_id: int):
    data = await request.json()
    firstname = data.get("firstname")

    # Update the last name of the student with the given student_id in the database
    cursor.execute("UPDATE students SET firstname = ? WHERE id = ?", (firstname, student_id))
    conn.commit()

    # Return the updated student record or a success message
    return {"message": f"First name of student with ID {student_id} updated successfully."}

@app.delete("/deletestudent/{student_id}")
async def delete_student(student_id: int):
    # Check if the student exists in the database
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Delete the student from the database
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    return {"message": f"Student with ID {student_id} has been deleted"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
