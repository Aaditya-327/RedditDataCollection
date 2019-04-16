import dropbox
import json


# dbx.users_get_current_account()
# for entry in dbx.files_list_folder('/jsonFiles').entries:
#     print(entry.name)

def upload(TOKEN, filename, data): 
    dbx = dropbox.Dropbox(TOKEN)
    string = json.dumps(data)
    upload = bytes(string ,encoding='utf8')
    dbx.files_upload(upload, '/jsonFiles/'+filename+'.json')
    return [_.name for _ in dbx.files_list_folder('/jsonFiles').entries]
