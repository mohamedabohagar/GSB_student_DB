from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import mariadb
from typing import List
from pydantic import BaseModel, Field

app = FastAPI()

# CORS configuration for allowing cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tables(BaseModel):
    TimeTableID: str
    Moodle_Course: str = Field(..., max_length=256)
    Study_Type: str = Field(..., max_length=256)
    Day: str = Field(..., max_length=256)
    StartDate: str
    FinalExamDate: str
    Semester: str = Field(..., max_length=256)
    Quarter: str = Field(..., max_length=256)
    Location: str = Field(..., max_length=256)
    Week: str = Field(..., max_length=5)


@app.get("/")
def home():
    return "Welcome To My App"

@app.get("/alllocation", status_code=status.HTTP_200_OK)
def alldata():
    #moodle_course: str
    conn = mariadb.connect(
        database="professorsdb",
        host="172.21.117.7",
        port=3306,
        user="Education",
        password="Edu@2017"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT *  FROM All_Contracts_Data")
    all_data = cursor.fetchall()
    Table_all = []
    if all_data:
        for row in all_data:
            Table_all.append(row[10])
        unique_data = list(set(Table_all))
        unique_data.sort()
        return unique_data


@app.get("/tables",  status_code=status.HTTP_200_OK)
async def read_data(
        page: int = Query(default=1, description="Page number", ge=1),
        per_page: int = Query(default=10, description="Items per page", le=100),

        time_table_id: str = Query(None),
        moodle_course: str = Query(None),
        study_type: str = Query(None),
        day: str = Query(None),
        start_date: str = Query(None),
        final_date: str = Query(None),
        semester: str = Query(None),
        quarter: str = Query(None),
        location: str = Query(None),
        week: str = Query(None)
):
    try:
        # Establish a database connection using a context manager
        conn = mariadb.connect(
            database="professorsdb",
            host="172.21.117.7",
            port=3306,
            user="Education",
            password="Edu@2017"
        )
        cursor = conn.cursor()
        columns = ['TimeTableID', 'Moodle_Course', 'Day', 'StartDate', 'FinalExamDate']

        where_conditions = []
        if time_table_id:
            where_conditions.append(f"TimeTableID = '{time_table_id}'")
        if moodle_course:
            where_conditions.append(f"Moodle_Course = '{moodle_course}'")
        if study_type:
            where_conditions.append(f"Study_Type = '{study_type}'")
        if day:
            where_conditions.append(f"Day = '{day}'")
        if start_date:
            where_conditions.append(f"StartDate = '{start_date}'")
        if final_date:
            where_conditions.append(f"FinalExamDate = '{final_date}'")
        if semester:
            where_conditions.append(f"Semester = '{semester}'")
        if quarter:
            where_conditions.append(f"Quarter = '{quarter}'")
        if location:
            where_conditions.append(f"location = '{location}'")
        if week:
            where_conditions.append(f"Week = '{week}'")

        if where_conditions:
            where_clause = " AND ".join(where_conditions)
            query = f"SELECT {', '.join(columns)} FROM All_Contracts_Data WHERE {where_clause}"
        else:
            query = f"SELECT {', '.join(columns)} FROM All_Contracts_Data LIMIT {per_page} OFFSET {(page - 1) * per_page}"
        # Construct and execute the SQL query with pagination
        #query = f"SELECT * FROM All_Contracts_Data LIMIT {per_page} OFFSET {(page - 1) * per_page}"
        cursor.execute(query)

        data = cursor.fetchall()
        result_data = []
        for row in data:
            row_dict = (columns, row)
            result_data.append(row_dict)

        # Calculate total count of records (you may need this for pagination)
        total_count = cursor.rowcount

        # Construct the JSON response
        response_data = {
            #"header": columns,  # Header columns
            "data": result_data,  # Data rows
            #"total_count": total_count  # Total count of records
        }

        # Return the JSON response
        return data

    except mariadb.Error as e:
        # Handle database errors here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    finally:
        # Close the cursor and connection in a finally block
        if cursor:
            cursor.close()
        if conn:
            conn.close()
