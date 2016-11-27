from unittest import mock, TestCase
from nose.plugins.attrib import attr

import os, shutil
from config.local import LocalConfig
from shiftmedia import BackendLocal
from shiftmedia import Storage
from shiftmedia.resizer import Resizer
from shiftmedia.testing.localstorage_testhelpers import LocalStorageTestHelpers


@attr('resizer', 'unit')
class StorageTests(TestCase, LocalStorageTestHelpers):
    """
    Image resizer unit tests
    These mostly quickly test the maths
    """

    # ------------------------------------------------------------------------
    # Resize to fit math
    # ------------------------------------------------------------------------

    def test_fit_no_upscale_smaller_original(self):
        """ Fit, no upscale, src smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FIT
        src = (100, 300)
        dst = (200, 400)
        upscale = False
        result = resizer.get_ratio(src, dst,mode=mode, upscale=upscale)
        self.assertEquals(src, result['size'])
        self.assertEquals((0,0), result['position'])

    def test_fit_no_upscale_one_side_smaller(self):
        """ Fit, no upscale, one side smaller"""
        resizer = Resizer
        mode = resizer.RESIZE_TO_FIT
        src = (100, 300)
        dst = (50, 400)
        upscale = False
        result = resizer.get_ratio(src, dst,mode=mode, upscale=upscale)
        self.assertEquals((50, 150), result['size'])
        self.assertEquals((0, 0), result['position'])

    def test_fit_no_upscale_bigger_original(self):
        """ Fit, no upscale, original bigger"""
        resizer = Resizer
        mode = resizer.RESIZE_TO_FIT
        src = (2000, 4000)
        dst = (1000, 1500)
        upscale = False
        result = resizer.get_ratio(src, dst,mode=mode, upscale=upscale)
        self.assertEquals((750, 1500), result['size'])
        self.assertEquals((0, 0), result['position'])

    def test_fit_upscale_smaller_original(self):
        """ Fit, upscale, original smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FIT
        src = (2000, 1000)
        dst = (3500, 3000)
        upscale = True
        result = resizer.get_ratio(src, dst, mode=mode, upscale=upscale)
        self.assertEquals((3500, 1750), result['size'])
        self.assertEquals((0, 0), result['position'])

    def test_fit_upscale_one_side_smaller(self):
        """ Fit, upscale, one side smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FIT
        src = (5000, 2200)
        dst = (3500, 3000)
        upscale = True
        result = resizer.get_ratio(src, dst, mode=mode, upscale=upscale)
        self.assertEquals((3500, 1540), result['size'])
        self.assertEquals((0, 0), result['position'])

    def test_fit_upscale_bigger_original(self):
        """ Fit, upscale, original bigger """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FIT
        src = (5000, 3000)
        dst = (1000, 1500)
        upscale = True
        result = resizer.get_ratio(src, dst, mode=mode, upscale=upscale)
        self.assertEquals((1000, 600), result['size'])
        self.assertEquals((0, 0), result['position'])

    # ------------------------------------------------------------------------
    # Resize to fill math
    # ------------------------------------------------------------------------

    def test_fill_no_upscale_smaller_original(self):
        """ Fill, no upscale, src smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FILL
        src = (1000, 3000)
        dst = (2000, 4000)
        upscale = False
        result = resizer.get_ratio(src, dst, mode, upscale)
        self.assertEquals(src, result['size'])
        self.assertEquals((0, 0), result['position'])

    def test_fill_no_upscale_one_side_smaller(self):
        """ Fill, no upscale, one side smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FILL
        src = (2000, 3000)
        dst = (3000, 2000)
        upscale = False
        result = resizer.get_ratio(src, dst, mode, upscale)
        self.assertEquals((2000, 2000), result['size'])
        self.assertEquals((0, 500), result['position'])

    def test_fill_no_upscale_bigger_original(self):
        """ Fill, no upscale, original bigger """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FILL
        src = (2000, 3000)
        dst = (1000, 2000)
        upscale = False
        result = resizer.get_ratio(src, dst, mode, upscale)
        self.assertEquals((1500, 3000), result['size'])
        self.assertEquals((250, 0), result['position'])

    def test_fill_upscale_original_smaller(self):
        """ Fill, upscale, original smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FILL
        src = (2000, 1000)
        dst = (4000, 3000)
        upscale = True
        result = resizer.get_ratio(src, dst, mode, upscale)
        self.assertEquals((1333, 1000), result['size'])
        self.assertEquals((334, 0), result['position'])

    @attr('xxx')
    def test_fill_upscale_one_side_smaller(self):
        """ Fill, upscale, one side smaller """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FILL
        src = (5000, 2000)
        dst = (4000, 3000)
        upscale = True
        result = resizer.get_ratio(src, dst, mode, upscale)
        self.assertEquals((2666, 2000), result['size'])
        self.assertEquals((1167, 0), result['position'])

    def test_fill_upscale_original_bigger(self):
        """ Fill, upscale, original bigger """
        resizer = Resizer
        mode = resizer.RESIZE_TO_FILL
        src = (4000, 3000)
        dst = (2000, 1000)
        upscale = True
        result = resizer.get_ratio(src, dst, mode, upscale)
        self.assertEquals((4000, 2000), result['size'])
        self.assertEquals((0, 500), result['position'])



