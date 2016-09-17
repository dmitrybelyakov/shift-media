from unittest import mock, TestCase
from nose.plugins.attrib import attr

import os, shutil, uuid
from config.local import LocalConfig
from shiftmedia import BackendLocal
from shiftmedia.testing.localstorage_testhelpers import LocalStorageTestHelpers


@attr('backend', 'local')
class BackendLocalTests(TestCase, LocalStorageTestHelpers):
    """ Local storage backend tests """

    def setUp(self, app=None):
        super().setUp()

    def tearDown(self):
        """ Clean up after yourself """
        self.clean()
        super().tearDown()


    # ------------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------------

    def test_can_instantiate_backend(self):
        """ Can instantiate backend  """
        backend = BackendLocal(self.path)
        self.assertIsInstance(backend, BackendLocal)

    def test_getting_path_creates_directory(self):
        """ Can create local path upon getting """
        self.assertFalse(os.path.exists(self.path))
        backend = BackendLocal(self.path)
        path = backend.path
        self.assertTrue(os.path.exists(path))

    def test_put_file(self):
        """ Put uploaded file to storage """
        self.prepare_uploads()
        backend = BackendLocal(self.path)
        uploads = self.upload_path
        src = os.path.join(uploads, 'test.tar.gz')
        id = str(uuid.uuid1())
        backend.put(src, id)

        # assert directories created
        current = self.path
        for dir in id.split('-'):
            current = os.path.join(current, dir)
            self.assertTrue(os.path.exists(current))

        # assert file put
        full_file_path = os.path.join(current, 'original.tar.gz')
        self.assertTrue(os.path.exists(full_file_path))



