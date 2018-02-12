# pylint: disable=W0703
import sys
import time

from thematic_client_sdk import Auth, ThematicClient



def main():
    # get token and args from command line
    if len(sys.argv) != 4:
        print("Usage: "+sys.argv[0]+' <refresh_token> <survey_id> <data_file_path>')
        exit()
    refresh_token = sys.argv[1]
    survey_id = sys.argv[2]
    data_file = sys.argv[3]
    # swap token for an access token
    auth = Auth()
    access_token = auth.swap_refresh_token(refresh_token)

    # create a client and upload the data
    client = ThematicClient(access_token)

    try:
        upload_id = client.data.upload_data(survey_id, data_file)
    except Exception as exc:
        print("Failed to upload data: "+str(exc))
        exit()

    # wait for the data to complete processing
    data = None
    while True:
        try:
            status = client.data.check_uploaded_data(survey_id, upload_id)
            if status == "ProcessingJobStatus.errored" or status == "ProcessingJobStatus.invalidated":
                print("Upload processing has failed with status: "+status)
                print("Retrieving logs...")
                logs = client.data.log_uploaded_data(survey_id, upload_id)
                print(logs)
                
            elif status == "ProcessingJobStatus.completed":
                print("Processing complete")
                break

        except Exception as exc:
            print("Failed to check status: "+str(exc))
            exit()
        time.sleep(2)


    # get the processed file
    try:
        save_location = data_file+'processed.csv'
        client.data.download_upload_results(save_location, survey_id, upload_id)
    except Exception as exc:
        print("Failed to get results: "+str(exc))
        exit()


if __name__ == "__main__":
    main()
