import os
import requests
import json
import subprocess
import google.auth
import google.auth.transport.requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

def prepare_header():
    #os.popen('gcloud auth list')
    #auth_out = subprocess.run(['gcloud','auth','list'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    #print(auth_out)

    #token = os.popen('gcloud auth application-default login --quiet && gcloud auth --account=terra-api@maximal-dynamo-308105.iam.gserviceaccount.com print-access-token').read().rstrip()
    #token = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token').json().get('access_token')
    #token = subprocess.run(['curl', '-s','http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token','-H','Metadata-Flavor: Google'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    #data = json.loads(token)
    #token_val = data["access_token"]
    #print(token_val)
    
    CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/cloud-platform","https://www.googleapis.com/auth/cloud-billing"] 

    def get_creds():
        credentials, project_id = google.auth.default(scopes=CREDENTIAL_SCOPES)
        credentials.refresh(google.auth.transport.requests.Request())
        return credentials

    creds = get_creds()
    print(creds.service_account_email)
    
    token = creds.token
    
    head = {'accept': '*/*',"Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(token)}
    print(head)
    return head
    

def submit_workflow(workspaceNamespace, workspaceName, submissionEntityType, submissionEntityName, submissionExpression):
    data={
      "methodConfigurationNamespace": "singlem",
      "methodConfigurationName": "singlem-single-task",
      "entityType": submissionEntityType,
      "entityName": submissionEntityName,
      "expression": submissionExpression,
      "useCallCache": False,
      "deleteIntermediateOutputFiles": True,
      "useReferenceDisks": False,
      "workflowFailureMode": "NoNewCalls"
    }
    
    head = prepare_header()
    
    myUrl = f'https://api.firecloud.org/api/workspaces/{workspaceNamespace}/{workspaceName}/submissions'
    response = requests.post(myUrl, data=json.dumps(data), headers=head)
    return response

def get_workflow_config(workspaceNamespace, workspaceName, methodConfigNamespace, methodConfigName):
    
    myUrl = f'https://api.firecloud.org/api/workspaces/{workspaceNamespace}/{workspaceName}/method_configs/{methodConfigNamespace}/{methodConfigName}'
    print(myUrl)
    head = prepare_header()

#    req = requests.Request('GET', myUrl, header=head)
#    prepared = req.prepare()
#    pretty_print_POST(prepared)
#    s = requests.Session()
#    response = s.send(prepared)
#    print(response)

    response = requests.get(myUrl, headers=head)
    print('terra api request submitted')
    return response
#    return None

def set_workflow_config(workspaceNamespace, workspaceName, methodNamespace, methodName, methodVersion, methodConfigRootEntityType, methodConfigVersion):

    myUrl = f'https://api.firecloud.org/api/workspaces/{workspaceNamespace}/{workspaceName}/method_configs/{methodNamespace}/{methodName}'

    data = {
      "deleted": False,
      "inputs": {
        "SingleM_SRA.GCloud_User_Key_File": "\"gs://fc-833c2d81-556a-4c83-aed7-21f884f6fec0/sa-private-key.json\"",
        "SingleM_SRA.AWS_User_Key": "",
        "SingleM_SRA.metagenome_size_in_GB": "this.metagenome_size_in_GB",
        "SingleM_SRA.SRA_accession_num": "this.sra_accession",
        "SingleM_SRA.GCloud_Paid": "false",
        "SingleM_SRA.metagenome_size_in_gbp": "this.metagenome_size_in_gbp",
        "SingleM_SRA.Download_Method_Order": "\"aws-http prefetch\"",
        "SingleM_SRA.AWS_User_Key_Id": ""
      },
      "methodConfigVersion": methodConfigVersion,
      "methodRepoMethod": {
        "methodName": methodName,
        "methodVersion": methodVersion,
        "methodNamespace": methodNamespace,
        "methodUri": f"agora://{methodNamespace}/{methodName}/{methodVersion}",
        "sourceRepo": "agora"
      },
      "name": methodName,
      "namespace": methodNamespace,
      "outputs": {
        "SingleM_SRA.SingleM_tables": "this.singlem_table"
      },
      "prerequisites": {},
      "rootEntityType": methodConfigRootEntityType
    }
    
    head = prepare_header()

    response = requests.put(myUrl, data=json.dumps(data), headers=head)
    return response

def get_method(methodConfigNamespace, methodConfigName, methodConfigVersion):

    myUrl = f'https://api.firecloud.org/api/methods/{methodConfigNamespace}/{methodConfigName}/{methodConfigVersion}?onlyPayload=false'
    
    head = prepare_header()

    response = requests.get(myUrl, headers=head)
    return response

def import_entity_from_tsv(file_path):
    token = os.popen('gcloud auth --account=terra-api@maximal-dynamo-308105.iam.gserviceaccount.com print-access-token').read().rstrip()

    url = 'https://api.firecloud.org/api/workspaces/firstterrabillingaccount/singlem-pilot-2/flexibleImportEntities'

    m = MultipartEncoder(
        fields={"workspaceNamespace": "firstterrabillingaccount","workspaceName": "singlem-pilot-2",
                'entities': ('filename', open(file_path, 'rb'), 'text/plain')}
        )

    head = {'accept': '*/*','Content-Type': m.content_type, 'Authorization': 'Bearer {}'.format(token)}

    response = requests.post(url, data=m, headers=head)
    return response
