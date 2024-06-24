# VisionAttendance

VisionAttendance is a simple, user-friendly web application designed to streamline the attendance-taking process. No sign-up, no setup—just upload pictures of your classroom. This prototype was created in approximately 5 hours to provide an uncomplicated solution for teachers.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Example](#example)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview
VisionAttendance aims to simplify the process of taking attendance by allowing teachers to upload a picture of their classroom. The app recognizes students in the photo and marks their attendance. Unlike other attendance apps that are often complex and disrupt the workflow, VisionAttendance is straightforward and easy to use.

## Features
- **No Sign-Up Required**: Start using the app without any registration.
- **No Setup Needed**: Use it instantly without any initial configuration.
- **Image Upload**: Upload classroom pictures to mark attendance.
- **Face Recognition**: Train the app to recognize students from pictures.
- **Unknown Students**: Automatically marks unidentified students as unknown.

## Getting Started
Follow these steps to set up the project on your local machine.

### Prerequisites
- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/VisionAttendance.git
    cd VisionAttendance
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python3 app.py
    ```

## Usage
1. Open the web app in your browser.
2. Upload a picture of your classroom.
3. Train the app to recognize students by uploading individual pictures of them.
4. The app will automatically mark the attendance of recognized students.
5. Any unidentified students will be marked as unknown.

## Example
Here is an example of how VisionAttendance works. Initially, it was trained to recognize two classmates. When a picture of the classroom was uploaded, it identified the known students and marked the attendance accordingly.

![Example Video](https://www.linkedin.com/posts/harshalsinghcn_in-my-college-a-lot-of-time-is-wasted-taking-activity-7210731188682952705-0l-I?utm_source=share&utm_medium=member_android)

## Future Improvements
VisionAttendance is a basic working prototype and can be improved in several ways:
- Enhanced face recognition accuracy
- Integration with existing attendance systems
- Support for multiple classrooms and sessions
- Detailed reporting and analytics

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
