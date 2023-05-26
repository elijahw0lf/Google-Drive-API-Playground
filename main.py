import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# global variables
app_scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly'] # the scopes we'll use in this script
service = None # holds the service object for interacting with the API

def clear_screen():
    """
        This function clears the terminal of all text, we use this to clean up the terminal between menu options.
    """
    os.system("cls" if os.name=="nt" else "clear")

def use_oauth(credential_file):
    """
        This function receives a string containing the location of the oauth credentials (in .json format).
        The create_service() function is called automatically at the end of this function, so that func might detect an error from this func (if the error relates to the Credentials file).
        Returns nothing because the create_service() func sets the global variable "service".
    """

    global app_scopes
    creds = None

    # check for token.json which stores the user's access and refresh tokens (auto-created on login)
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", app_scopes)

    # check if there are no creds, or they're invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # refresh the creds
            creds.refresh(Request())
        else:
            # let the user log in
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, app_scopes)
            creds = flow.run_local_server(port=0)

        # save the creds for the next run in token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    # now we have credentials, build the service object
    create_service(creds)

def use_service_account(credential_file):
    """
        This function receives a string containing the location of the service account credentials (in .json format). Errors loading the credential file will be detected in this function.
        The create_service() function is called automatically at the end of this function.
        Returns nothing because the create_service() func sets the global variable "service".
    """

    global app_scopes
    
    try: 
        creds = service_account.Credentials.from_service_account_file(credential_file, scopes=app_scopes)
        creds = creds.with_subject("elijah@w0lf.digital")
    except Exception as e: 
        print(f"ERROR: Could not load service account: {e}")
        exit(1)
    
    # now we have credentials, build the service object
    create_service(creds)

def create_service(creds):
    """
        This function receives a Credentials object from the imported libraries and creates a service object.
        Normally this function is called by another function that creates the Credentials object, then passes it to this function to create the service object. You probably don't need to call this function yourself.
        Returns nothing because it sets the global variable "service" for other functions to use.
    """

    global service

    # try to create the service object and store it in the global variable
    try:
        service = build('drive', 'v3', credentials=creds) # call the Drive v3 API
    except HttpError as e:
        # TODO(developer) - Handle errors from drive API.
        print(f"ERROR (HTTPError): Could not construct Drive v3 service: {e}")
        exit(1)
    except Exception as e:
        print(f"ERROR (Unknown): Could not construct Drive v3 service: {e}")
        exit(1)

def test_speed():
    """
        This function will get all of the files in a Shared Drive, and will time the whole operation so that you see how long it took.
        You can change which files it gets by changing the "results" variable inside the while loop.
    """

    global service

    try:
        token = None # stores the nextPageToken value to get the next page of results when the loop restarts
        cycle = 1 # just keeps track of the number of times we loop inside the while loop below
        total_files = 0 # holds the number of files we've retrieved
        loop_stats = [] # holds the time it took to complete a loop, so we can see how long it took to run in total
        while True:
            # get start time
            loop_start_time = time.perf_counter()

            # make the API call and store the list of files into "all_files", update our "total_files" total
            results = service.files().list(pageToken=token, fields="nextPageToken, files", teamDriveId="0AM0wdzT81rNpUk9PVA", includeItemsFromAllDrives=True, corpora="drive", supportsAllDrives=True).execute()
            all_files = results.get("files", [])
            total_files += len(all_files)

            # count the time taken to finish and then add it into the list
            loop_time = time.perf_counter() - loop_start_time
            loop_time = round(loop_time, 4) # round to 4 decimal places
            loop_stats.append(loop_time)

            # print a message to show the loop is progressing
            print(f"Loop #{cycle:02} ({loop_time:.4f} sec) ... got {len(all_files)} files...")

            # check for "nextPageToken" in results
            if "nextPageToken" in results.keys():
                # there's another page to retrieve, set the token variable
                token = results["nextPageToken"]

                # increase cycle count
                cycle += 1
            else:
                # no more pages to retrieve, break the loop now
                print(f"All pages downloaded, exiting the loop now ...")
                break


        # count each loop time
        app_total_time = 0
        for t in loop_stats:
            app_total_time += t
        app_total_time = round(app_total_time, 2) # round to 2 decimal places

        # print some stats
        print(f"\nTotal files retrieved: {total_files}")
        print(f"Total app runtime: {app_total_time}")

    except Exception as e:
        print(f"ERROR: Encountered a problem while trying to fetch files and time the operation. Error message is: {e}")
        exit(1)
    
    # pause for the user to read the screen
    input("\n\nPress ENTER to return to the menu ... ")

def list_files():
    """
        This function will get all of the files in a Shared Drive, and then prints some info about each file to the console.
        You can change which files it gets by changing the "results" variable inside the while loop.
    """

    global service

    try:
        token = None # stores the nextPageToken value to get the next page of results when the loop restarts
        cycle = 1 # just keeps track of the number of times we loop inside the while loop below
        while True:

            # make the API call and store the list of files into "all_files"
            results = service.files().list(pageToken=token, fields="nextPageToken, files", teamDriveId="0AM0wdzT81rNpUk9PVA", includeItemsFromAllDrives=True, corpora="drive", supportsAllDrives=True).execute()
            all_files = results.get("files", [])

            # print a message to show the loop is progressing
            print(f"Loop #{cycle:02} got {len(all_files)} files...")

            # check we retrieved files
            if len(all_files) > 0:
                # loop through each file and print it
                for file in all_files:
                    ### START simple method to just print the file ID, name and parents ###
                    parents_string = ", ".join(file["parents"])
                    print(f"ID: {file['id']}, Name: {file['name']}, Parents: {parents_string}")
                    ### END simple method ###

                    ### BELOW IS THE ADVANCED "PRINT EVERY META DATA VALUE" METHOD, THIS PRINTS LOTS OF INFORMATION ###
                    ### BE CAREFUL BEFORE ACTIVATING THIS, CONSIDER INSERTING A LOOP LIMIT OR SOMETHING SIMILAR ###

                    # for key, value in file.items():
                    #     # check what kind of variable we have in "value"
                    #     if isinstance(value, list):
                    #         # this value is a list, join the list contents together into a string
                    #         list_to_str = ", ".join(value)
                    #         print(f"{key}: {list_to_str}")
                    #     elif isinstance(value, dict):
                    #         # this value is a dict, iterate through it and print each with a small indent
                    #         print(f"{key}:")
                    #         for key2, value2 in value.items():
                    #             print(f"{' '*10}{key2}: {value2}")
                    #     else:
                    #         # the value is a normal string/bool/etc, just print normally
                    #         print(f"{key}: {value}")
            else:
                print(f"WARNING: Found no files in results we retrieved. Exiting loop now for safety!")
                break

            # check for "nextPageToken" in results
            if "nextPageToken" in results.keys():
                # there's another page to retrieve, set the token variable
                token = results["nextPageToken"]

                # increase cycle count
                cycle += 1
            else:
                # no more pages to retrieve, break the loop now
                print(f"All pages downloaded, exiting the loop now ...")
                break


    except Exception as e:
        print(f"ERROR: Encountered a problem while trying to fetch files and print them. Error message is: {e}")
        exit(1)

    # pause for the user to read the screen
    input("\n\nPress ENTER to return to the menu ... ")


def main():
    global service

    # use either oauth or service account to authenticate with the Drive API    
    # use_oauth("oauth-wolf-playground.json") # using oauth
    use_service_account("service.account-wolf-playground.json") # using "service account"

    # create a loop for user to input commands
    while True:
        clear_screen() # clear the screen

        # show the available commands
        print(f"\n\nAvailable Commands:")
        print(f"{' '*10} \"time\" - fetch all files and time the whole operation")
        print(f"{' '*10} \"list\" - fetch all files and print file information to the console")
        print(f"{' '*10} \"exit\" - quits the app\n")
        
        # request user input, then clear the screen to prepare for the next function's output (or error message)
        input_command = input("Enter a command: ").strip().lower()
        clear_screen()
        
        # check if the user entered a valid command
        if input_command == "time":
            test_speed() # run a test to see how long it takes to retrieve all the files
        elif input_command == "list":
            list_files() # retrieve all the files and print them to the console
        elif input_command == "exit":
            print(f"Thanks for using my app. I hope you have a great day!\n")
            print(f"Merci d'utiliser mon application. J'espère que tu as passé une bonne journée!\n\n")
            time.sleep(1)
            exit(0)
        else:
            input(f"\nWARNING: Invalid command, please choose a command from the menu.\n\nPress ENTER to continue ... ")

if __name__ == '__main__':
    main() # run the main function when this app starts for the first time