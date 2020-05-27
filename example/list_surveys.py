import sys
from thematic_client_sdk import Auth, ThematicClient



def main():
    # get token from command line
    if len(sys.argv) < 3:
        print("Usage: "+sys.argv[0]+' <refresh_token> <organization>')
        exit()
    refresh_token = sys.argv[1]
    organization = None
    if len(sys.argv) > 2:
        organization = sys.argv[2]
    # swap token for an access token
    auth = Auth()
    access_token = auth.swap_refresh_token(refresh_token)

    # create a client and list the surveys that are available
    client = ThematicClient(access_token)

    if organization:
        client.organization(organization)
    surveys = client.surveys.get()
    print('Surveys:')
    for survey in surveys:
        print(str(survey["id"]) + " : " + survey['name'])
        print('\tVisualizations:')
        for vis in survey['visualizations']:
            print("\t" + str(vis["id"]) + " : " + vis['name'])
        print('\tResults:')
        for result in survey['results']:
            print("\t" + str(result['status']) + " : " + str(result['jobID']))


if __name__ == "__main__":
    main()
