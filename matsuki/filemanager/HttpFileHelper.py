# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 10, 2020
# LastChg: Apr 10, 2020

import os
from flask import send_from_directory
from werkzeug import FileStorage
from siki.basics import FileUtils, TimeTicker


def allowed_ext(filename, fileExts):
    """
    the file extension is allowed to upload to server
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in fileExts


def rename_file(filename:str):
    ext = filename.rsplit('.', 1)[1]
   
    # 创建以时间为蓝本的文件名    
    unix_time = TimeTicker.time_now_foramt("%Y%m%d%H%M%S%f")

    # 修改文件名
    new_filename = unix_time + '.' + ext   

    return new_filename


def upload(dirPath: str, file: FileStorage, rename: bool, *allowFileExts):
    """
    file-upload interface, given a folder and a file from request, then saving it!

    @Args:
    * [dirPath] str
    * [file] request.files
    * [rename] bool
    * [allowFileExts] list of str

    @Returns:
    * [bool] if file saved, return true, else false
    * [str] if success, return the filename, else the failure message
    """

    # folder not exists, create one
    if not FileUtils.exists(dirPath):
        FileUtils.mkdir(dirPath)
    
    if not isinstance(file, FileStorage):
        return False, "file is not the type of werkzeug.FileStorage"

    if allowed_ext(file.filename, allowFileExts):
        success_name = None

        if rename:
            success_name = rename_file(file.filename)
            file.save(os.path.join(dirPath, success_name))
        else:
            success_name = file.filename
            file.save(os.path.join(dirPath, success_name))

        return True, success_name
    
    return False, "file extension is not allowed"




def update(dirPath: str, file: FileStorage, targetName: str, *allowFileExts):
    """
    file-update interface, to update a server-side file by given the filename, file object, and file-stored folder path

    @Args:
    * [dirPath] str
    * [file] FileStorage
    * [targetName] target file name
    * [allowFileExts] list of str

    @Returns:
    * [bool] if file saved, return true, else false
    * [str] if success, return the filename, else the failure message
    """
    
    # folder not exists, return false, no file could found in a vacant folder
    if not FileUtils.exists(dirPath):
        return False, "the folder not exists"
    
    if file and allowed_ext(file.filename, allowFileExts):
        
        # if no file exists
        if not FileUtils.exists(os.path.join(dirPath, file.filename)):
            return False, "the file not exists"
        
        # save and update the target file
        file.save(os.path.join(dirPath, file.filename))

        # return to caller
        return True, os.path.join(dirPath, file.filename)


    

def download(dirPath: str, filename: str, as_attachment = True):
    """
    file-download interface, download a file from the server

    @Args:
    * [dirPath] str
    * [filename] target file name

    @Returns:
    * [bool] if file saved, return true, else false
    * [str/link] if success, return the download file link, else the failure message
    """

    # folder not exists, return false, no file could found in a vacant folder
    if not FileUtils.exists(dirPath):
        return False, "the folder not exists"

    # file is vacant
    if not FileUtils.exists(os.path.join(dirPath, filename)):
        return False, "the file not exists"
    
    # given caller the download link
    return True, send_from_directory(dirPath, filename, as_attachment = as_attachment)

