# SocialSync - README

## Github Repository Link
[SocialSync Repository](https://github.com/ali-zargari/SocialSync)

## Installation and Setup

### Prerequisites
- A MacOS System with ARM Architecture (Recommended)
- Python (version 3.9 to 3.12). Ensure PIP/PIP3 package installer is available.
- PyCharm IDE (recommended but optional)
- GitHub CLI

### Recommended Installation Steps

1. **Clone the Repository:**
   - Use the following commands to clone and navigate to the master branch:
     ```bash
     git clone https://github.com/ali-zargari/SocialSync.git
     cd SocialSync
     ```

2. **Setup PyCharm IDE (Optional):**
   - Open the project using PyCharm.
   - Configure Python version between 3.9 to 3.12. PyCharm will automatically create a virtual environment.

3. **Install Dependencies:**
   - Run the following command in the root directory:
     ```bash
     pip3 install -r requirements.txt
     ```

4. **Set Backend Credentials:**
   - Navigate to the `backend` folder.
   - Create a `.env` file. Go to the Canvas submission "Project Code and demo (Group)" and get the README from there to find the Database configuration. *(Cannot upload passwords and keys here).*

5. **Run the Project:**
   - Open two terminal windows; one in the `backend` folder and one in the `ui` folder.
   - Execute the following command in each terminal, starting with the backend:
     ```bash
     python3 main.py
     ```

7. **Success!**
   - SocialSync should be up and running after executing the commands in the `ui` folder.

### Alternative Installation Without PyCharm

1. **Prepare the Environment:**
   - Ensure Python (version 3.9 to 3.12) is installed along with PIP/PIP3.
   - Install GitHub CLI.

2. **Clone the Repository and Navigate:**
   - Use the following commands:
     ```bash
     git clone https://github.com/ali-zargari/SocialSync.git
     cd SocialSync
     ```

3. **Setup Virtual Environment:**
   - Navigate to the project directory.
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Follow Steps 3 to 5 from the Recommended Installation Steps.**


## Building the Project for an Executable:
1. Go to the main directory of SocialSync in a terminal window.
2. In a different window navigate to the build_commands directory.
3. Open file `buildcommand.txt`.
4. If this is your first time building this project, feel free to skip step 5 of this guide.
5. (can skip for first time) In the root directory, run the commands in step 1 in `buildcommands.txt`.
6. In the root directory, run the commands in step 2 in `buildcommands.txt`.
7. Wait for the installation to complete.
8. In the `dist` folder which should be created in the project root, you will find the UNIX executable.
- NOTE: When the app is launched for the first time, it may ask for camera access. Please allow it use the camera.
- You may need to sign out and sing back in, or relaunch the app after the first time you run it.
## Additional Information
For any issues or contributions, please refer to the [issues page](https://github.com/ali-zargari/SocialSync/issues) on the Github repository.

