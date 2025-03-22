import os

# Function to get a boolean (yes/no) input from the user
def get_boolean_input(prompt):
    while True:
        response = input(prompt + " (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

# Function to get a valid file path input from the user
def get_file_input(prompt):
    while True:
        file_path = input(prompt + " (enter full file path): ").strip()
        if os.path.isfile(file_path):
            return file_path
        else:
            print("File not found. Please enter a valid file path.")

# Main function to collect user input
def main():
    print("Enter user information below:\n")

    user_info = {}  # Dictionary to store user information

    # Collecting basic user details
    user_info["university"] = input("University: ").strip()

    # Validating graduation year input as an integer
    while True:
        try:
            user_info["graduation_year"] = int(input("Graduation Year: ").strip())
            break
        except ValueError:
            print("Please enter a valid year (e.g., 2025).")

    user_info["major"] = input("Major: ").strip()

    # Collecting boolean inputs
    user_info["employed_status"] = get_boolean_input("Are you currently employed?")
    user_info["internships"] = get_boolean_input("Have you had any internships?")
    user_info["grad_school"] = get_boolean_input("Are you planning to attend or currently attending grad school?")

    # Collecting GPA and classes information
    user_info["gpa_range"] = input("GPA Range (e.g., 3.5-4.0): ").strip()
    user_info["classes_teaching"] = input("Classes you're teaching (comma-separated if more than one): ").strip()

    # Collecting bio and links
    user_info["bio"] = input("Short Bio (max 1000 characters): ").strip()
    user_info["linkedin"] = input("LinkedIn Profile URL: ").strip()

    # Collecting file uploads for resume and cover letter
    user_info["resume"] = get_file_input("Upload your resume")
    user_info["cover_letter"] = get_file_input("Upload your cover letter")

    # Displaying collected user information
    print("\nCollected User Information:")
    for key, value in user_info.items():
        print(f"{key}: {value}")

# Entry point for the script
if __name__ == "__main__":
    main()
