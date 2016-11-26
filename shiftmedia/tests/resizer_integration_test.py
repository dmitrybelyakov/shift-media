from unittest import mock, TestCase
from nose.plugins.attrib import attr

import os, shutil
from config.local import LocalConfig
from shiftmedia import BackendLocal
from shiftmedia import Storage
from shiftmedia.resizer import Resizer
from shiftmedia.testing.localstorage_testhelpers import LocalStorageTestHelpers


@attr('resizer', 'integration')
class StorageTests(TestCase, LocalStorageTestHelpers):
    """
    Image resizer integration tests
    These will resize actual images
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        """ Clean up after yourself """
        # self.clean()
        super().tearDown()

    # test assets
    files = dict(
        vertical=dict(file='original_vertical.jpg', size=(248, 768)),
        horizontal=dict(file='original_horizontal.jpg', size=(768, 248)),
        square=dict(file='original_square.jpg', size=(700, 700))
    )

    # ------------------------------------------------------------------------
    # Image manipulation tests: to fit
    # ------------------------------------------------------------------------

    def test_integration_fit_no_upscale_smaller_original(self):
        """ INTEGRATION: Fit, no upscale, src smaller """
        img = self.files['vertical'] #248x768
        filename = img['file']
        target_size = '3000x1000'
        mode = Resizer.RESIZE_TO_FIT
        algo = None
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(img['size'][0], result.size[0])
        self.assertEquals(img['size'][1], result.size[1])
        result.show()

    def test_integration_fit_no_upscale_one_side_smaller(self):
        """ INTEGRATION: Fit, no upscale, one side smaller"""
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '300x500'
        mode = Resizer.RESIZE_TO_FIT
        algo = None
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(161, result.size[0])
        self.assertEquals(500, result.size[1])
        # result.show()

    def test_integration_fit_no_upscale_bigger_original(self):
        """ INTEGRATION: Fit, no upscale, original bigger"""
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '200x300'
        mode = Resizer.RESIZE_TO_FIT
        algo = None
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(96, result.size[0])
        self.assertEquals(300, result.size[1])
        # result.show()

    def test_integration_fit_upscale_smaller_original(self):
        """ INTEGRATION: Fit, upscale, original smaller """
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '300x500'
        mode = Resizer.RESIZE_TO_FIT
        algo = None
        upscale = True
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(290, result.size[0])
        self.assertEquals(900, result.size[1])
        # result.show()

    def test_integration_fit_upscale_one_side_smaller(self):
        """ INTEGRATION: Fit, upscale, one side smaller """
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '300x500'
        mode = Resizer.RESIZE_TO_FIT
        algo = None
        upscale = True
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(161, result.size[0])
        self.assertEquals(500, result.size[1])
        # result.show()

    def test_integration_fit_upscale_bigger_original(self):
        """ INTEGRATION: Fit, upscale, original bigger """
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '200x300'
        mode = Resizer.RESIZE_TO_FIT
        algo = None
        upscale = True
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(96, result.size[0])
        self.assertEquals(300, result.size[1])
        # result.show()

    # ------------------------------------------------------------------------
    # Image manipulation tests: to fill
    # ------------------------------------------------------------------------

    def test_integration_fill_no_upscale_smaller_original(self):
        """ Fill, no upscale, src smaller """
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '2000x3000'
        mode = Resizer.RESIZE_TO_FILL
        algo = None
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(248, result.size[0])
        self.assertEquals(768, result.size[1])
        # result.show()

    def test_integration_fill_no_upscale_one_side_smaller(self):
        """ Fill, no upscale, one side smaller """
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '150x900'
        mode = Resizer.RESIZE_TO_FILL
        algo = None
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(150, result.size[0])
        self.assertEquals(768, result.size[1])
        # result.show()

    def test_integration_fill_no_upscale_bigger_original_risize_original(self):
        """ Fill, no upscale, original bigger - resize original algo """
        img = self.files['vertical']  # 248x768
        filename = img['file']
        target_size = '200x100'
        mode = Resizer.RESIZE_TO_FILL
        algo = Resizer.RESIZE_ORIGINAL
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        self.assertEquals(200, result.size[0])
        self.assertEquals(100, result.size[1])
        # result.show()

    def test_integration_fill_no_upscale_bigger_original_risize_sample(self):
        """ Fill, no upscale, original bigger - resize sample algo """
        img = self.files['horizontal']  # 248x768
        filename = img['file']
        target_size = '200x100'
        mode = Resizer.RESIZE_TO_FILL
        algo = Resizer.RESIZE_SAMPLE
        upscale = False
        self.prepare_uploads()
        src = os.path.join(self.upload_path, filename)
        result = Resizer.resize(src, target_size, mode, algo, upscale)
        # self.assertEquals(200, result.size[0])
        # self.assertEquals(100, result.size[1])
        result.show()


    @attr('xxx')
    def test_algorithm_performance(self):
        """ Testing algorithm performance """
        root = os.path.realpath(os.path.dirname(__file__) + '/../../')
        src = os.path.join(root, 'var', 'earthview')
        tmp = self.tmp_path
        ignores = ['.DS_Store', 'earthview.txt']
        files = [item for item in os.scandir(src) if item.is_file() and item.name not in ignores]
        import time

        start1 = time.perf_counter()
        for file in files:
            target_size = '500x500'
            mode = Resizer.RESIZE_TO_FILL
            algo = Resizer.RESIZE_SAMPLE # TIME TAKEN: 139.14194644900272
            # algo = Resizer.RESIZE_ORIGINAL # TIME TAKEN: 153.24238268200133
            dst = os.path.join(tmp, file.name)
            img = Resizer.resize(file.path, target_size, mode, algo)
            img.save(dst)

        end1 = time.perf_counter()
        dif1 = (start1 - end1) * -1

        start2 = time.perf_counter()
        for file in files:
            target_size = '500x500'
            mode = Resizer.RESIZE_TO_FILL
            # algo = Resizer.RESIZE_SAMPLE # TIME TAKEN: 139.14194644900272
            algo = Resizer.RESIZE_ORIGINAL # TIME TAKEN: 153.24238268200133
            dst = os.path.join(tmp, file.name)
            img = Resizer.resize(file.path, target_size, mode, algo)
            img.save(dst)

        end2 = time.perf_counter()
        dif2 = (start2 - end2) * -1

        print('RESIZE SAMPLE:', dif1)
        print('RESIZE ORIGINAL:', dif2)





    def test_integration_fill_upscale_original_smaller_risize_original(self):
        """ Fill, upscale, original smaller - resize original algo """
        pass


    def test_integration_fill_upscale_original_smaller_risize_sample(self):
        """ Fill, upscale, original smaller - resize sample algo """
        pass


    def test_integration_fill_upscale_one_side_smaller_risize_sample(self):
        """ Fill, upscale, one side smaller - resize sample algo """
        pass


    def test_integration_fill_upscale_one_side_smaller_risize_original(self):
        """ Fill, upscale, one side smaller - resize original algo """
        pass


    def test_integration_fill_upscale_original_bigger_risize_original(self):
        """ Fill, upscale, original bigger - resize original algo """
        pass


    def test_integration_fill_upscale_original_bigger_risize_sample(self):
        """ Fill, upscale, original bigger - resize sample algo """
        pass










