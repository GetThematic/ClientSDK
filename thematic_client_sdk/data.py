import requests

class Data(object):
    def __init__(self,access_token,api_url):
        self.api_url = api_url
        self.access_token = access_token

    def upload_data(self,survey_id,file_location):
        '''
        Uploads data and provides an identifier that can be used for checking on the status of an upload in progress
        '''
        url = self.api_url+'/survey/'+str(survey_id)+'/upload'
        files = {'file': open(file_location,'rb')}

        response = requests.post(url,headers={'Authorization':'bearer '+self.access_token},files=files)
        print (response.text)
        if response.status_code != 200:
            raise Exception('Could not upload data: '+str(response.text))

        if not response.json() or 'data' not in response.json() or 'upload_id' not in response.json()['data']:
            raise Exception('Could not upload data: response did not have required format')
        return response.json()['data']['upload_id']

    def check_uploaded_data(self,survey_id,upload_id):
        '''
        Returns the current status of the upload
        '''
        url = self.api_url+'/survey/'+str(survey_id)+'/upload/'+upload_id+'/status'
        response = requests.get(url,headers={'Authorization':'bearer '+self.access_token})

        if response.status_code != 200:
            raise Exception('Could not check status: '+str(response.text))

        if not response.json() or 'data' not in response.json():
            raise Exception('Could not check status: response did not have required format')
        return response.json()['data']

    def download_data(self,download_location,survey_id,result_id=None):
        '''
        If result_id is not provided then the latest results will be downloaded
        '''
        url = self.api_url+'/survey/'+str(survey_id)+'/data_csv'
        if result_id:
            url = self.api_url+'/survey/'+str(survey_id)+'/result/'+str(result_id)+'/data_csv'
        response = requests.get(url,headers={'Authorization':'bearer '+self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception('Could not retrieve data: '+str(response.text))

        with open(download_location,'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        return True

    def download_themes(self,download_location,survey_id,result_id=None):
        '''
        If result_id is not provided then the latest results will be downloaded
        '''
        url = self.api_url+'/survey/'+str(survey_id)+'/data_themes'
        if result_id:
            url = self.api_url+'/survey/'+str(survey_id)+'/result/'+str(result_id)+'/data_themes'
        response = requests.get(url,headers={'Authorization':'bearer '+self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception('Could not retrieve data: '+str(response.text))

        with open(download_location,'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        return True
