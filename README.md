# Ethiopian Developer Community Platform

## Introduction

The Ethiopian developer community, despite its immense talent and potential, faces significant challenges that hinder the recognition and impact of its innovative projects. This platform aims to address these issues by providing a centralized system developed using Django, JavaScript, and SQLite.

## Project Description

This project seeks to facilitate project visibility, enable collaboration among developers, support career advancement opportunities, and facilitate job matching within the tech industry. The main objectives are:

1. **Facilitate Project Visibility:** Develop a feature that allows developers to create comprehensive profiles and upload their projects, showcasing their work to a broader audience and enhancing their visibility within the community.
2. **Enable Peer-to-Peer Messaging:** Implement a real-time direct messaging system using Django Channels and HTMX that facilitates one-on-one communication among developers, enabling them to connect, share insights, and collaborate privately.
3. **Establish Group Messaging Based On Interests:** Create a dynamic functionality using Django Channels and HTMX for developers to form or join interest-based groups where they can engage in discussions, share resources, and collaborate on projects, fostering a sense of community and collective problem-solving.
4. **Event Centralization:** Introduce a feature for developers to easily discover and engage with tech events in Ethiopia, overcoming current visibility challenges and fostering a vibrant tech community.
5. **Develop Intuitive User Interfaces:** Ensure easy navigation and interaction with the application, providing a seamless user experience for Ethiopian developers.
6. **Implement Language Localization:** Enable the platform to switch between multiple languages, ensuring that developers from Ethiopia's diverse linguistic backgrounds can access the website content in their preferred language.

## Folder Structure

The project directory contains the following main components:

- `a_rtchat/`: Contains the implementation of the real-time chat functionality.
- `db.sqlite3`: The SQLite database file.
- `event/`: Contains the implementation of event-related features.
- `group/`: Contains the implementation of group-related features.
- `manage.py`: A command-line utility that lets you interact with this Django project.
- `projects/`: Contains the implementation of project-related features.
- `requirements.txt`: A file listing the Python dependencies required for the project.
- `static/`: Contains static files such as CSS, JavaScript, and images.
- `staticfiles/`: Directory for static files.
- `techsync/`: The main Django application directory.
- `templates/`: Contains HTML templates for the application.
- `users/`: Contains the implementation of user-related features.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Tech_Sync-main
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply the migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

Once the application is running, you can:

- **Create and manage profiles:** Showcase your projects and skills.
- **Message other developers:** Use the real-time peer-to-peer messaging system to collaborate.
- **Join interest-based groups:** Engage in real-time discussions and share resources.
- **Discover tech events:** Stay informed about upcoming tech events in Ethiopia.
- **Navigate the application:** Enjoy an intuitive user interface.
- **Switch languages:** Access the platform in your preferred language.
