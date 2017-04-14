import os, shutil
from abc import ABCMeta, abstractmethod
from shiftmedia import exceptions as x
from pathlib import Path


class Backend(metaclass=ABCMeta):
    """
    Abstract backend
    This defines methods your backend must implement in order to
    work with media storage
    """

    # TODO: implement s3 backend
    # TODO: implement clearing generated files in backend

    @abstractmethod
    def __init__(self, url='http://localhost'):
        """
        Backend constructor
        Requires a base storage url to build links.
        :param url: string - base storage url
        """
        self._url = url

    def get_url(self):
        """
        Get URL
        Returns base URL of storage
        """
        return self._url

    @abstractmethod
    def put_original(self, src, id, force=False):
        """
        Put original file to storage
        Does not require a filename as it will be extracted from provided id.
        Will raise an exception on an attempt to overwrite existing file which
        you can force to ignore.
        """
        pass

    @abstractmethod
    def put_variant(self, src, id, filename, force=False):
        """
        Put file variant to storage
        Save local file in storage under given id and filename. Will raise an
        exception on an attempt to overwrite existing file which you can force
        to ignore.
        """
        pass

    @abstractmethod
    def retrieve_original(self, id, local_path):
        """
        Retrieve original
        Download file original from storage and put to local temp path
        """
        pass

    @abstractmethod
    def delete(self, id):
        """
        Delete
        Remove file from storage by id
        """
        pass

    @abstractmethod
    def parse_url(self, url):
        """
        Parse url
        Processes url to return a tuple of id and filename. This is being used
        when we create dynamic image resizes to retrieve the original based on
        resize filename.
        :param url: string - resize url
        :return: tuple - id and filename
        """
        pass


class BackendLocal(Backend):
    """
    Local backend
    Stores file locally in a directory without transferring to remote storage
    """

    def __init__(self, local_path=None, url='http://localhost'):
        """
        Backend constructor
        Requires a local storage path and base storage url.
        :param local_path: string - where to store files
        :param url: string - base storage url
        """
        super().__init__(url)
        self._path = local_path

    @property
    def path(self):
        """
        Get path
        Returns path to local storage and creates one if necessary
        """
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        return self._path

    def id_to_path(self, id):
        """
        Id to path
        Returns a list of directories extracted from id
        :param id: string, - object id
        :return: list
        """
        parts = id.lower().split('-')[0:5]
        tail = id[len('-'.join(parts)) + 1:]
        parts.append(tail)
        return parts

    def parse_url(self, url):
        """
        Parse url
        Processes url to return a tuple of id and filename. This is being used
        when we create dynamic image resizes to retrieve the original based on
        resize filename.
        :param url: string - resize url
        :return: tuple - id and filename
        """
        url = url.replace(self._url, '')
        url = url.strip('/').lower()
        url = url.split('/')
        id = '-'.join(url[:-1])
        filename = url[-1]
        return id, filename

    def put_original(self, src, id, force=False):
        """
        Put original file to storage
        Does not require a filename as it will be extracted from provided id.
        the resulting path will have following structure:
            3c72aedc/ba25/11e6/569/406c8f413974/original-filename.jpg

        :param src: string - path to source file
        :param id: string - generated id
        :param force: bool - whether to overwrite existing
        :return: string - generated id
        """
        filename = '-'.join(id.split('-')[5:])
        return self.put_variant(src, id, filename, force)

    def put_variant(self, src, id, filename, force=False):
        """
        Put file variant to storage
        Save local file in storage under given id and filename. Will raise an
        exception on an attempt to overwrite existing file which you can force
        to ignore.
        """
        if not os.path.exists(src):
            msg = 'Unable to find local file [{}]'
            raise x.LocalFileNotFound(msg.format(src))

        parts = self.id_to_path(id)
        dir = os.path.join(self.path, *parts)
        os.makedirs(dir, exist_ok=True)
        dst = os.path.join(self.path, *parts, filename.lower())
        if not force and os.path.exists(dst):
            msg = 'File [' + filename + '] exists under [' + id + ']. '
            msg += 'Use force option to overwrite.'
            raise x.FileExists(msg)
        shutil.copyfile(src, dst)
        return id

    def delete(self, id):
        """
        Delete
        Remove file from storage by id
        """
        id = str(id)
        path = os.path.join(self.path, *id.split('-')[0:5])
        shutil.rmtree(path)
        return True

    def retrieve_original(self, id, local_path):
        """
        Retrieve original
        Download file from storage and put to local temp path
        """
        path = self.id_to_path(id)
        filename = path[5]
        src = os.path.join(self.path, *path, filename)
        dst_dir = os.path.join(local_path, id)
        dst = os.path.join(dst_dir, filename)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        shutil.copyfile(src, dst)
        return dst


class BackendS3(Backend):
    """
    Amazon S3 backend
    Stores files in an amazon s3 bucket
    """

    def __init__(self, url='http://localhost'):
        """
        Backend constructor
        :param url: string - base storage url
        """
        super().__init__(url)

    @property
    def path(self):
        """
        Get path
        Returns path to local storage and creates one if necessary
        """
        pass

    def id_to_path(self, id):
        """
        Id to path
        Returns a list of directories extracted from id
        :param id: string, - object id
        :return: list
        """
        pass

    def parse_url(self, url):
        """
        Parse url
        Processes url to return a tuple of id and filename. This is being used
        when we create dynamic image resizes to retrieve the original based on
        resize filename.
        :param url: string - resize url
        :return: tuple - id and filename
        """
        pass

    def put_original(self, src, id, force=False):
        """
        Put original file to storage
        Does not require a filename as it will be extracted from provided id.
        the resulting path will have following structure:
            3c72aedc/ba25/11e6/569/406c8f413974/original-filename.jpg

        :param src: string - path to source file
        :param id: string - generated id
        :param force: bool - whether to overwrite existing
        :return: string - generated id
        """
        pass

    def put(self, src, id, filename, force=False):
        """
        Put file to storage
        Save local file in storage under given id and filename. Will raise an
        exception on an attempt to overwrite existing file which you can force
        to ignore.
        """
        pass

    def delete(self, id):
        """
        Delete
        Remove file from storage by id
        """
        pass

    def retrieve_original(self, id, local_path):
        """
        Retrieve original
        Download file from storage and put to local temp path
        """
        pass
