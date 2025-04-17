# Checking Attendance System

##  Introduction

**Checking Attendance System** is a facial recognition attendance system built with **FastAPI**, **MTCNN**, **FaceNet**, and **MySQL**. The system supports two cameras: one for **check-in** and one for **check-out**, helping to manage working time automatically and accurately.
# Getting Started 
**Note**: Make sure you have completed [Python basic Tutorial](https://www.w3schools.com/java/) or you are in the process of learning Python

## Step 1: Install and Set Up Required Dependencies
To build and run the Checking Attendance System, you need to install Python, required libraries, and MySQL. If you have already set up these dependencies, skip to Step 2.
1. Install Python
    - Install Python version 3.10.6 from the [Python website](https://www.python.org/downloads/)
    - Ensure pip is installed and added to your system PATH. 
2. Install required libraries. 
    - Install the following Python libraries using pip, which are included in file [requirements.txt](checking_attendance_system/requirements.txt).
      ```bash
      pip install requirements.txt

    - Note: The facenet-pytorch library includes MTCNN and FaceNet for facial recognition. Ensure you have a compatible version of PyTorch installed. 
3. Set up MySQL. 
    - Download and install MySQL Community Server from mysql.com. 
    - Set up a MySQL server instance and note your database credentials (username, password, host, and port).
4. Install Camera Drivers:
    - Ensure your webcam (minimum 720p resolution) is connected and drivers are installed. Most modern webcams are plug-and-play on Windows/Linux.

If you have already installed these dependencies, proceed to Step 2.

## Step 2: Run the program
Follow these steps to clone and run the Checking Attendance System: 
1. Clone the Project:
    - Clone the project from the repository:
    ```bash
    git clone https://github.com/hoanglmv/checking_attendance_system
2. Open Project in Visual Studio Code or other IDE applications
3. Set Up the Database: 
    - Update the database configuration in file [config.py](src\be_src\app\core\config.py) with your MySQL credentials: 
    ``` bash
    DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
    }
4. Run the Application:
    - Locate the main application file [run.py](src\run.py).
    - Run the application
    ```bash 
    python src/run.py
5. Data Update
    - To update data, modify the MySQL database directly or use the application's admin interface to add/edit data. 

## This Application
**Uses**:
- Attendance Tracking: Automatically records employee check-in/check-out using facial recognition.

- Employee Management: Allows admins to add, edit, delete, and view employee information.

- Real-Time Notifications: Displays notifications for successful/failed attendance attempts.

- Reporting: Generates attendance reports by day or month.

- Admin Authentication: Supports secure login, registration, and password recovery for admins.

**Usage**:
#### Login:
- Open the application and enter admin credentials (email and password) on the login screen.
- Click “Login” to access the admin dashboard.
- If you forget your password, click “Forgot Password” to reset it via OTP .
#### Add Employee:
- From the dashboard, click “Add Employee”.
- Enter employee details (name, email, phone, department) and upload face images (JPEG/PNG, ≥720p).
- Click “Save” to add the employee and generate a face embedding.
#### View Employee Information:
- Click “Employee List” to view all employees.
- Select an employee to see detailed information (name, email, department, etc.).
#### Attendance Tracking:
- Employees stand in front of the camera at check-in/check-out points.
- The system automatically detects and records attendance, displaying a notification (e.g., “Check-in successful: [Name], [Time]”).
#### View Attendance Records:
- Click “Daily Attendance”  to view daily attendance records.
- Filter by date or employee to see specific records.
- Click “Monthly Attendance”  to view an employee’s attendance for a selected month.
#### Edit/Delete Employee
- From the employee list, select an employee and click “Edit” to update details or “Delete” to remove them (requires confirmation).
#### Export Reports:
- From the attendance list, click “Export Report” to generate a PDF/Excel report for a specific day or month.
#### Admin Registration:
- Click “Register” on the login screen.
- Enter details (username, email, password, phone) and verify via OTP.
#### Logout:
- Click “Logout” from the dashboard to end the session and return to the login screen.
## Resources:
- Python and PyQt6: For building the user interface.
- FASTAPI: For the backend API.
- MySQL: For database management.
- FaceNet and MTCNN: For facial recognition.
- SMTP Service: For sending OTP emails.

## Developers
Le Mai Viet Hoang [hoanglmv] (https://github.com/hoanglmv):
- System architecture design
- Backend API development
- Facial recognition implementation (FaceNet, MTCNN)
- Facial recognition module testing
- Frontend development (PyQt6)

Duong Minh Kien [PigCassoKien] (https://github.com/PigCassoKien):
- Backend API development
- OTP email integration
- UX development
- Database schema development
- API optimization
- Security implementation (JWT, SHA-256).

Cao Le Phung [caolephung] (https://github.com/caolephung):
- Frontend development (PyQt6)
- UI/UX design
- Testing and debugging

Hung Minh Tuan [8MTi] (https://github.com/8MTI):
- Frontend development (PyQt6)
- UI design and implementation
- System integration

Le Doan Tuan [Tuana2412] (https://github.com/Tuana2412):
- UI design
- Documentation and SRS development
- System integration

## Contributing

- Pull requests are welcome. For major changes, please open an issue on the project repository to discuss proposed changes.

## Troubleshooting

- **Error: “Camera not detected”:**
  - Ensure your webcam is connected and drivers are installed.
  - Check camera permissions in your operating system.
  - Verify the camera resolution is ≥720p.
- **Error: “MySQL connection failed”:**
  - Confirm MySQL server is running and credentials in database.py are correct.
  - Check network connectivity if using a remote MySQL server.
- **Error: “Face recognition failed”:**
   -Ensure lighting conditions are adequate (≥300 lux).
  - Verify employee face data is correctly uploaded (use high-quality images).
  - Check FaceNet/MTCNN library versions for compatibility.
- **Error: “API not responding”:**
  - Ensure the FASTAPI server is running (uvicorn src.main.python.api:app).
  - Check if http://127:0:0:1:8000 is accessible.
  - For additional help, refer to the project’s README or contact the development team.

## Learn More
- To deepen your understanding of the technologies used, explore these resources:
  - Python Tutorial - From basics to advanced Python.
PyQt6 Documentation - Guide to building GUIs with PyQt6.
  - FASTAPI Documentation - Learn to build modern APIs.
  - FaceNet Paper - Understand the facial recognition model.
  - MySQL Tutorial - Database setup and management.

## Project Status
The project is in active development, with Version 1.0 completed as of April 2025. Future versions will include advanced features like real-time email/SMS notifications and multi-camera support.

## Note
This application is developed for educational and enterprise use, aimed at automating attendance tracking with modern computer vision technology.