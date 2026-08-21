import os
import shutil
import hashlib
from datetime import datetime

class VersionControlSystem :
    def __init__ (self ,repo_path ):

        self .repo_path =repo_path
        self .versions_path =os .path .join (self .repo_path ,'.versions')
        if not os .path .exists (self .versions_path ):
            os .makedirs (self .versions_path )

    def _hash_file (self ,file_path ):

        hasher =hashlib .sha256 ()
        with open (file_path ,'rb')as f :
            buf =f .read ()
            hasher .update (buf )
        return hasher .hexdigest ()

    def _save_version (self ,file_path ):

        timestamp =datetime .now ().strftime ('%Y%m%d%H%M%S')
        file_hash =self ._hash_file (file_path )
        version_file_name =f'{timestamp}_{file_hash}.bak'
        shutil .copy2 (file_path ,os .path .join (self .versions_path ,version_file_name ))
        print (f'Version saved: {version_file_name}')

    def track_file (self ,file_path ):

        try :
            if os .path .exists (file_path ):
                self ._save_version (file_path )
            else :
                print (f"File {file_path} does not exist.")
        except Exception as e :
            print (f"An error occurred: {e}")

    def list_versions (self ,file_name ):

        try :
            files =os .listdir (self .versions_path )
            versions =[f for f in files if f .endswith ('.bak')]
            for version in versions :
                print (version )
        except Exception as e :
            print (f"An error occurred: {e}")

    def restore_version (self ,file_name ,version_name ):

        try :
            version_path =os .path .join (self .versions_path ,version_name )
            if os .path .exists (version_path ):
                shutil .copy2 (version_path ,os .path .join (self .repo_path ,file_name ))
                print (f'File {file_name} restored to version {version_name}.')
            else :
                print (f'Version {version_name} does not exist.')
        except Exception as e :
            print (f"An error occurred: {e}")

if __name__ =='__main__':

    vcs =VersionControlSystem ('your_repository_directory')

    vcs .track_file ('example.txt')

    vcs .list_versions ('example.txt')