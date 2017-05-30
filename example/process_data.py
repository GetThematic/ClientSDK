import sys
import time

from thematic_client_sdk import Auth,ThematicClient



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
    access_token = auth.swap_refresh_token_for_access_token(refresh_token)

    # create a client and upload the data
    client = ThematicClient(access_token)

    try:
        upload_id = client.data.upload_data(survey_id,data_file)
    except Exception as e:
        print(e)
        print("Failed to upload data: "+str(e))
        exit()

    # wait for the data to complete processing
    data = None
    while True:
        try:
            data = client.data.check_uploaded_data(survey_id,upload_id)
            if 'status' not in data:
                print("Upload processing has failed and given a bad object")
                exit()
            elif data['status'] == "errored" or data['status'] == "invalidated":
                print("Upload processing has failed with status: "+status)
                exit()
            elif data['status'] == "completed":
                print("Processing complete")
                break

        except Exception as e:
            print("Failed to check status: "+str(e))
            exit()
        time.sleep(2)

    # now we need to swap the upload id for the result id to request the download
    result_id = data['result_id']


    # get the processed file
    try:
        save_location = data_file_path+'processed.csv'
        client.data.download_data(save_location,survey_id,result_id=result_id)
    except Exception as e:
        print("Failed to get results: "+str(e))
        exit()


if __name__ == "__main__": main()
