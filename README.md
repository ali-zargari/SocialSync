# SocialSync - README

## Github Repository Link
[SocialSync Repository](https://github.com/ali-zargari/SocialSync)

## Installation and Setup

### Prerequisites
- A MacOS with ARM Architecture (Recommended)
- Python (version 3.9 to 3.12). Ensure PIP/PIP3 package installer is available.
- PyCharm IDE (recommended but optional)
- GitHub CLI

### Recommended Installation Steps

1. **Clone the Repository:**
   - Use the following commands to clone and navigate to the master branch:
     ```
     git clone https://github.com/ali-zargari/SocialSync.git
     cd SocialSync
     ```

2. **Setup PyCharm IDE (Optional):**
   - Open the project using PyCharm.
   - Configure Python version between 3.9 to 3.12. PyCharm will automatically create a virtual environment.

3. **Install Dependencies:**
   - Run the following command in the root directory:
     ```
     pip3 install -r requirements.txt
     ```

4. **Set Backend Credentials:**
   - Navigate to the `backend` folder.
   - Create a `.env` file. Go to the Canvas submission "Project Code and demo (Group)" and get the readme from there to find the Database configuration. (Cannot upload passwords and keys here).

5. **Run the Project:**
   - Open two terminal windows; one in the `backend` folder and one in the `ui` folder.
   - Execute `python3 main.py` in both terminals starting with the backend.

6. **Success!**
   - SocialSync should be up and running after executing the commands in the `ui` folder.

### Alternative Installation Without PyCharm

1. **Prepare the Environment:**
   - Ensure Python (version 3.9 to 3.12) is installed along with PIP/PIP3.
   - Install GitHub CLI.

2. **Clone the Repository and Navigate:**
   - Same as above.

3. **Setup Virtual Environment:**
   - Navigate to the project directory.
   - Create and activate a virtual environment:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Follow Steps 3 to 5 from the Recommended Installation Steps.**

## Additional Information
For any issues or contributions, please refer to the [issues page](https://github.com/ali-zargari/SocialSync/issues) on the Github repository.