# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 10, 2020
# Modified: May 25, 2020

import os
from siki.basics import FileUtils, TimeTicker
from werkzeug.datastructures import FileStorage


def allowed_ext(filename, file_extensions):
    """
    the file extension is allowed to upload to server
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in file_extensions


def rename_file(filename: str):
    ext = filename.rsplit('.', 1)[1]

    # 创建以时间为蓝本的文件名    
    unix_time = TimeTicker.time_now_with_foramt("%Y%m%d%H%M%S%f")

    # 修改文件名
    new_filename = unix_time + '.' + ext

    return new_filename


def upload(directory: str, file: object, rename: bool, *allow_extensions):
    """
    file-upload interface, given a folder and a file from request, then saving it!

    @Args:
    * [directory] str
    * [file] request.files
    * [rename] bool
    * [allow_extensions] list of str

    @Returns:
    * [bool] if file saved, return true, else false
    * [str] if success, return the filename, else the failure message
    """

    # folder not exists, create one
    if not FileUtils.exists(directory):
        FileUtils.mkdir(directory)

    if not file:
        return False, "file is null"

    if allowed_ext(file.filename, allow_extensions):

        if rename:
            success_name = rename_file(file.filename)
            file.save(os.path.join(directory, success_name))
        else:
            success_name = file.filename
            file.save(os.path.join(directory, success_name))

        return True, success_name

    return False, "file extension is not allowed"


def update(directory: str, file: object, *allow_extensions):
    """
    file-update interface, to update a server-side file by given the filename, file object, and file-stored folder path

    @Args:
    * [directory] str
    * [file] object
    * [allow_extensions] list of str

    @Returns:
    * [bool] if file saved, return true, else false
    * [str] if success, return the filename, else the failure message
    """

    # folder not exists, return false, no file could found in a vacant folder
    if not FileUtils.exists(directory):
        return False, "the folder not exists"

    if file and allowed_ext(file.filename, allow_extensions):

        # if no file exists
        if not FileUtils.exists(os.path.join(directory, file.filename)):
            return False, "the file not exists"

        # save and update the target file
        file.save(os.path.join(directory, file.filename))

        # return to caller
        return True, os.path.join(directory, file.filename)


def download(directory: str, filename: str):
    """
    file-download interface, download a file from the server

    @Args:
    * [directory] str
    * [filename] target file name

    @Returns:
    * [bool] if file saved, return true, else false
    * [str/link] if success, return the download file link, else the failure message
    """

    # folder not exists, return false, no file could found in a vacant folder
    if not FileUtils.exists(directory):
        return False, "the folder not exists"

    # file is vacant
    if not FileUtils.exists(os.path.join(directory, filename)):
        return False, "the file not exists"

    # given caller the download link
    return True, FileUtils.gen_file_path(directory, filename)


def read(file_handler: FileStorage):
    """
    read contents from handler

    @Returns:
    * [bytes] the content of file in bytes
    """
    if file_handler is None:
        return None

    if isinstance(file_handler, FileStorage):
        return file_handler.read()

    # else
    return None
