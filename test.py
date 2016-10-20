#! /usr/bin/env python
"""Test suite"""

from tempfile import mkdtemp
from shutil import rmtree
import unittest
from os import path

class BptbxTestSuite(unittest.TestCase):

    def test_cmdline (self):
        print ('--- testing b_cmdline')
        from bptbx import b_cmdline
        if 'windows' in b_cmdline.get_platform():
            command = 'cmd.exe'
            command_exe = command +  ' /C dir'
        else:
            command = 'ls'
            command_exe = command + ' ~/'

        assert b_cmdline.check_for_command(command)
        code, _, _ = b_cmdline.execute_command(command_exe, True, True)
        assert code == 0
        assert b_cmdline.get_command_process(command)

    def test_daemon(self):
        print ('--- testing b_daemon')
        from bptbx import b_daemon
        from threading import Thread
        from time import sleep

        class TestDaemon(b_daemon.Daemon):
            runs = 0
            def _run_daemon_process(self):
                #print ('daemon running. iteration #{}'.format(self.runs+1))
                self.runs += 1

        def start_daemon(daemon):
            daemon.start()

        daemon = TestDaemon(1)
        thread = Thread(target=start_daemon, args = (daemon,))
        thread.start()
        sleep(2)
        assert daemon.runs > 0
        daemon.stop()

    def test_enum(self):
        print ('--- testing b_enum')
        from bptbx import b_enum
        my_enum = b_enum.enum ('START', 'STOP')
        assert my_enum.START == 0
        assert my_enum.STOP == 1

    def test_iotools(self):
        print ('--- testing b_iotools')
        from bptbx import b_iotools

        assert (b_iotools.basename('/somewhere/on/the/disc/filetype.css', '.css')
         == 'filetype')
        assert (b_iotools.basename('/somewhere/on/the/disc/filetype.css')
        == 'filetype.css')
        assert b_iotools.countlines('LICENSE') == 202
        assert b_iotools.file_exists('LICENSE')
        assert len(b_iotools.filedatetime()) == 2
        assert len(b_iotools.finddirs('.')) > 0
        assert len(b_iotools.findfiles('.')) > 0
        assert len(b_iotools.findfiles('.', '120410hd1212re')) == 0
        assert len(b_iotools.get_immediate_subdirectories('.')) > 0
        assert len(b_iotools.get_immediate_subfiles('.')) > 0
        assert b_iotools.getuidfromfilepath('LICENSE') == 'LICENSE'
        b_iotools.import_module_with_check('numpy')
        b_iotools.import_modules_with_check( [ 'numpy', 'math' ])
        assert b_iotools.insertintofilename('test.txt', 'foo') == 'testfoo.txt'
        assert b_iotools.md5sum('LICENSE') == '175792518e4ac015ab6696d16c4f607e'
        kv = b_iotools.read_config_section_to_keyval_list(
                    'test-data/config.txt', 'AlbumInfo')
        assert kv == [('key', 'Value')], kv
        kv = b_iotools.read_config_section_to_keyval_list(
                    'test-data/config.txt', 'TextInfo')
        assert kv == [('foo', 'Bar')], kv
        assert len(b_iotools.read_file_to_list('LICENSE')) == 202
        b_iotools.zip_dir_recursively('test-data', 'test-data/zip.zip')
        assert b_iotools.file_exists('test-data/zip.zip')
        b_iotools.remove_silent('test-data/zip.zip')
        assert not b_iotools.file_exists('test-data/zip.zip')
        self.assertRaises(TypeError, b_iotools.mkdirs)
        self.assertRaises(TypeError, b_iotools.mkdirs, None)
        self.assertRaises(TypeError, b_iotools.mkdirs, '')
        temp_dir = mkdtemp()
        self.addCleanup(rmtree, temp_dir, True)
        b_iotools.mkdirs(temp_dir)
        temp_subdir = path.join(temp_dir, 'test')
        self.assertFalse(path.exists(temp_subdir))
        b_iotools.mkdirs(temp_subdir)
        self.assertTrue(path.exists(temp_subdir))
        temp_subsubsubdir = path.join(temp_dir, 'test2', 'test3', 'test4')
        self.assertFalse(path.exists(temp_subsubsubdir))
        b_iotools.mkdirs(temp_subsubsubdir)
        self.assertTrue(path.exists(temp_subsubsubdir))
        self.assertRaises(TypeError, b_iotools.get_immediate_subdirectories)
        self.assertRaises(TypeError, b_iotools.get_immediate_subdirectories, None)
        self.assertRaises(TypeError, b_iotools.get_immediate_subdirectories, '')
        self.assertRaises(OSError, b_iotools.get_immediate_subdirectories, 'asdasf:321kds')
        temp_dir = mkdtemp()
        self.addCleanup(rmtree, temp_dir, True)
        self.assertEqual(0, len(b_iotools.get_immediate_subdirectories(temp_dir)))
        b_iotools.mkdirs(path.join(temp_dir, 'sub1'))
        b_iotools.mkdirs(path.join(temp_dir, 'sub2'))
        b_iotools.mkdirs(path.join(temp_dir, 'sub3'))
        self.assertEqual(3, len(b_iotools.get_immediate_subdirectories(temp_dir)))
        self.assertEqual('sub1', b_iotools.get_immediate_subdirectories(temp_dir)[0])
        self.assertEqual('sub2', b_iotools.get_immediate_subdirectories(temp_dir)[1])
        self.assertEqual('sub3', b_iotools.get_immediate_subdirectories(temp_dir)[2])

    def test_legacy(self):
        print ('--- testing b_legacy')
        from bptbx import b_legacy
        assert b_legacy.b_configparser()
        assert b_legacy.b_queue()
        assert b_legacy.b_urllib2()
        assert b_legacy.b_tk()

    def test_logging(self):
        print ('--- testing b_logging')
        from bptbx import b_logging
        b_logging.setup_logging(True)

    def test_math (self):
        print ('--- testing b_math')
        from bptbx import b_math
        result = b_math.split_list_to_equal_buckets([1, 2, 3, 4, 5, 6, 7, 8], 3)
        assert result == [[1.0, 2.0, 3.0], [4.0, 5.0], [6.0, 7.0, 8.0]]
        result = b_math.reduce_list([1, 3, 4, 3], 2)
        assert result == [ 2.0, 3.5 ]

    def test_pil(self):
        print ('--- testing b_pil')
        from bptbx import b_pil
        from bptbx import b_iotools
        b_pil.resize_image_with_factor('test-data/image.jpg',
                                       './image-resized.jpg', 0.5)
        length = b_pil.get_length_of_long_side('test-data/image.jpg')
        assert length == 460
        length = b_pil.get_length_of_long_side('./image-resized.jpg')
        assert length == 230, length
        b_iotools.remove_silent('./image-resized.jpg')

    def test_strings (self):
        print ('--- testing b_strings')
        from bptbx import b_strings
        assert b_strings.id_generator()
        assert b_strings.concat_list_to_string([ 'a', 'b', 'c' ]) == 'abc'
        assert b_strings.fillzeros('12', 4) == '0012'

    def _random_calculation (self):
        from random import randint
        val1 = randint(1, 100)
        val2 = randint(1, 100)
        result = val1 + val2

    def test_threading (self):
        print ('--- testing b_threading')
        from bptbx import b_threading
        cpus = b_threading.get_cpus()
        pool = b_threading.ThreadPool(cpus)
        for _ in range(0, 10):
            pool.add_task(self._random_calculation)
        pool.wait_completion()
        assert pool.is_empty()

    def test_visual (self):
        print ('--- testing b_visual')
        from bptbx import b_visual
        from random import randint
        x_axis_dataset = []
        y1 = []
        y2 = []
        for x in range(1, 11):
            x_axis_dataset.append(x)
            y1.append(randint(1, 100))
            y2.append(randint(1, 100))
        y_axis_datasets = [y1, y2]
        y_axis_datalabels = ['Some data', 'Some other data']
        x_axis_isdatetime = False
        title = 'Test plot'
        x_label = 'Data points'
        y_label = 'Random values'
        fontsize = 9
        fontweight = 'bold'

        try:
            b_visual.print_dataset(x_axis_dataset, y_axis_datasets,
                    y_axis_datalabels, x_axis_isdatetime, title, x_label,
                    y_label, fontsize, fontweight, '%d.%m.%Y\n%H:%M', False)
        except Exception:
            pass

    def test_web (self):
        print ('--- testing b_web')
        from bptbx import b_web
        content = b_web.download_webpage_to_list('http://www.google.de')
        assert len(content) > 0

if __name__ == "__main__":
    unittest.main()
#
# if __name__ == "__main__":
#
#     test_cmdline()
#     test_daemon()
#     test_enum()
#     test_iotools()
#     test_legacy()
#     test_logging()
#     test_math()
#     test_pil()
#     test_strings()
#     test_threading()
#     try:
#         test_visual()
#     except Exception:
#         print( 'Catched TclError. Most probably there is no display available.')
#     test_web()
#
#     print ('--- all tests have passed.')
