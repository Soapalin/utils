import os 
import shutil
import subprocess
import sys
import zipfile
import stat
from Logger import log


folders = [
    "C:\Sandbox\Python Learning\log_analysis_tools",
    "C:\Sandbox\Python Learning\web-scraper",
    "C:\Sandbox\Python Learning\launch_test_cycle",
    "C:\Sandbox\CLearning",
    "C:\Sandbox\ObsidianVault",
    "C:\Sandbox\Emulator",
    "C:\Scripts",
    
]
save_to_all_dest = False
destination = [
    r"H:\backup1",
    r"H:\backup2",
    r"H:\backup3"
]
svn = False
svn_link = ""

class Backup:
    def __init__(self, folders, destination, svn, svn_link, save_to_all_dest):
        self.folders = folders
        self.destination = destination
        if not save_to_all_dest:
            # only overwriting earliest destination
            for dest in self.destination:
                if not os.path.exists(dest):
                    os.makedirs(dest)
            self.destination = [min(self.destination, key=os.path.getmtime)]
            log.debug(f"Only overwriting earliest destination: {self.destination}")
        self.svn = svn 
        self.svn_link = svn_link
    
    def backup_files_to_dest(self):
        for arg in folders:
            if os.path.isfile(arg):
                # log.debug(f"{arg} is a file")
                self.copy_file_to_all_dest(source=arg)

            elif os.path.isdir(arg):
                self.copy_dir_to_all_dest(source=arg)
                # log.debug(f"{arg} is a directory")
            

    def backup_files_to_svn(self):
        pass


    def copy_file_to_all_dest(self, source):
        for backup_folder in self.destination:
            dest = os.path.join(backup_folder,source.split("\\")[-1])
            shutil.copyfile(source, dest)
            file = source.split('\\')[-1]
            log.info(f"{file} was successfully backed up")

    def copy_dir_to_all_dest(self, source):
        def on_rm_error( func, path, exc_info):
            # path contains the path of the file that couldn't be removed
            # let's just assume that it's read-only and unlink it.
            os.chmod( path, stat.S_IWRITE )
            os.unlink( path )
        for backup_folder in self.destination:
            dest = os.path.join(backup_folder, source.split("\\")[-1])
            if os.path.exists(dest):
                log.debug(f"Overwriting the folder: {dest}")
                shutil.rmtree(dest, onerror= on_rm_error)
            shutil.copytree(source,dest)
            file = source.split('\\')[-1]
            log.info(f"{file} was successfully backed up")

    def main(self):
        print("MAIN: backing up files to H:/ drive and svn")
        for dest in self.destination:
            if not os.path.exists(dest):
                os.makedirs(dest)
        self.backup_files_to_dest()
        if self.svn:
            self.backup_files_to_svn()


backup = Backup(folders=folders, destination=destination, svn=svn, svn_link=svn_link, save_to_all_dest=save_to_all_dest)


if __name__ == "__main__":
    backup.main()
