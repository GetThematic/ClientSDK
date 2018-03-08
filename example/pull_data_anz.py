# pylint: disable=W0703
import sys

from thematic_client_sdk import Auth, ThematicClient



def main():
    # get token and args from command line
    if len(sys.argv) < 3:
        print("Usage: "+sys.argv[0]+' <refresh_token> <survey_id> <result_id>')
        exit()
    refresh_token = sys.argv[1]
    survey_id = sys.argv[2]
    result_id = None
    output_format = None
    if len(sys.argv) > 3:
        output_format = sys.argv[3]
    # swap token for an access token
    auth = Auth()
    access_token = auth.swap_refresh_token(refresh_token)

    # create a client and upload the data
    client = ThematicClient(access_token, api_url='https://client.anz.getthematic.com/api')


    # get the processed file
    try:
        save_location = str(survey_id)+'_'+str(result_id)
        client.data.download_data(save_location+'_processed.csv',
                                  survey_id,
                                  result_id=result_id,
                                  output_format=output_format)
        client.data.download_themes(save_location+'_processed.json', survey_id, result_id=result_id)
    except Exception as exc:
        print("Failed to get results: "+str(exc))
        exit()


if __name__ == "__main__":
    main()
