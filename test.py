#!/usr/bin/env python3
"""Test suite"""

from argparse import _StoreAction, _StoreTrueAction, ArgumentError
from bptbx import b_cmdprs
from bptbx import b_daemon
from bptbx import b_date
from bptbx import b_enum
from bptbx import b_iotools
from bptbx import b_legacy
from bptbx import b_logging
from bptbx import b_pil
from bptbx import b_shell
from bptbx import b_strings
from bptbx import b_threading
from bptbx import b_visual
from bptbx import b_web
from os import path, devnull
from random import randint
from re import sub
from shutil import rmtree
from tempfile import mkdtemp
from threading import Thread
from time import sleep
import sys
import unittest


class BptbxTestSuite(unittest.TestCase):

    def test_cmdprs(self):
        print('--- testing b_cmdprs')
        dnull = open(devnull, 'w')
        sys.stdout = dnull  # disable print

        # init ----------------------------------------------------------------
        prs = b_cmdprs.init('test')
        self.assertIsNotNone(prs)
        self.assertEqual(prs.description, 'test')
        self.assertRaises(TypeError, b_cmdprs.show_help)
        self.assertRaises(ValueError, b_cmdprs.show_help, {})

        # file_in -------------------------------------------------------------
        prs = b_cmdprs.init()
        self.assertRaises(TypeError, b_cmdprs.add_file_in)
        self.assertRaises(ValueError, b_cmdprs.add_file_in, {})
        b_cmdprs.add_file_in(prs)
        self.assertRaises(
            ArgumentError, b_cmdprs.add_file_in, prs)  # Not allowed twice
        self._check_action(prs, 'i', 'Input file', 'INPUT')
        self._check_action(b_cmdprs.add_file_in(
            b_cmdprs.init(), '-i'), 'i', 'Input file', 'INPUT')
        self._check_action(b_cmdprs.add_file_in(
            b_cmdprs.init(), 'i'), 'i', 'Input file', 'INPUT')
        self._check_action(b_cmdprs.add_file_in(
            b_cmdprs.init(), 'o'), 'o', 'Input file', 'INPUT')
        self._check_action(b_cmdprs.add_file_in(
            b_cmdprs.init(), 'o', 'My input'), 'o', 'My input', 'INPUT')
        self.assertRaises(TypeError, b_cmdprs.check_file_in)
        self.assertRaises(TypeError, b_cmdprs.check_file_in, {})
        self.assertRaises(ValueError, b_cmdprs.check_file_in, {}, {})
        self.assertRaises(ValueError, b_cmdprs.check_file_in, prs, {})
        args = prs.parse_args(['-i', 'test-data/config.txt'])
        try:
            b_cmdprs.check_file_in(prs, args)
            b_cmdprs.check_file_in(prs, args, 'i')
            b_cmdprs.check_file_in(prs, args, '-i')
        except SystemExit:
            self.fail('Unexpected system exit')
        self.assertRaises(SystemExit, b_cmdprs.check_file_in, prs,
                          prs.parse_args(['-i', 'test-data/']))
        self.assertRaises(SystemExit, b_cmdprs.check_file_in, prs, args, 'o')
        args = prs.parse_args(['-i', 'doesnotexist'])
        self.assertRaises(SystemExit, b_cmdprs.check_file_in, prs, args, 'i')

        # dir_in --------------------------------------------------------------
        prs = b_cmdprs.init()
        self.assertRaises(TypeError, b_cmdprs.add_dir_in)
        self.assertRaises(ValueError, b_cmdprs.add_dir_in, {})
        b_cmdprs.add_dir_in(prs)
        self.assertRaises(
            ArgumentError, b_cmdprs.add_dir_in, prs)  # Not allowed twice
        self._check_action(prs, 'i', 'Input directory', 'INPUT')
        self._check_action(b_cmdprs.add_dir_in(
            b_cmdprs.init(), '-i'), 'i', 'Input directory', 'INPUT')
        self._check_action(b_cmdprs.add_dir_in(
            b_cmdprs.init(), 'i'), 'i', 'Input directory', 'INPUT')
        self._check_action(b_cmdprs.add_dir_in(
            b_cmdprs.init(), 'o'), 'o', 'Input directory', 'INPUT')
        self._check_action(b_cmdprs.add_dir_in(
            b_cmdprs.init(), 'o', 'My input'), 'o', 'My input', 'INPUT')
        self.assertRaises(TypeError, b_cmdprs.check_dir_in)
        self.assertRaises(TypeError, b_cmdprs.check_dir_in, {})
        self.assertRaises(ValueError, b_cmdprs.check_dir_in, {}, {})
        self.assertRaises(ValueError, b_cmdprs.check_dir_in, prs, {})
        args = prs.parse_args(['-i', 'test-data/'])
        try:
            b_cmdprs.check_dir_in(prs, args)
            b_cmdprs.check_dir_in(prs, args, 'i')
            b_cmdprs.check_dir_in(prs, args, '-i')
        except SystemExit:
            self.fail('Unexpected system exit')
        self.assertRaises(SystemExit, b_cmdprs.check_dir_in, prs,
                          prs.parse_args(['-i', 'test-data/config.txt']))
        self.assertRaises(SystemExit, b_cmdprs.check_dir_in, prs, args, 'o')
        args = prs.parse_args(['-i', 'doesnotexist/'])
        self.assertRaises(SystemExit, b_cmdprs.check_dir_in, prs, args, 'i')

        # file_out ------------------------------------------------------------
        prs = b_cmdprs.init()
        self.assertRaises(TypeError, b_cmdprs.add_file_out)
        self.assertRaises(ValueError, b_cmdprs.add_file_out, {})
        b_cmdprs.add_file_out(prs)
        self.assertRaises(
            ArgumentError, b_cmdprs.add_file_out, prs)  # Not allowed twice
        self._check_action(prs, 'o', 'Output file', 'OUTPUT')
        self._check_action(b_cmdprs.add_file_out(
            b_cmdprs.init(), '-o'), 'o', 'Output file', 'OUTPUT')
        self._check_action(b_cmdprs.add_file_out(
            b_cmdprs.init(), 'o'), 'o', 'Output file', 'OUTPUT')
        self._check_action(b_cmdprs.add_file_out(
            b_cmdprs.init(), 'a'), 'a', 'Output file', 'OUTPUT')
        self._check_action(b_cmdprs.add_file_out(
            b_cmdprs.init(), 'a', 'My OUTPUT'), 'a', 'My OUTPUT', 'OUTPUT')
        self.assertRaises(TypeError, b_cmdprs.check_file_out)
        self.assertRaises(TypeError, b_cmdprs.check_file_out, {})
        self.assertRaises(ValueError, b_cmdprs.check_file_out, {}, {})
        self.assertRaises(ValueError, b_cmdprs.check_file_out, prs, {})
        args = prs.parse_args(['-o', 'test-data/new.txt'])
        try:
            b_cmdprs.check_file_out(prs, args)
            b_cmdprs.check_file_out(prs, args, 'o')
            b_cmdprs.check_file_out(prs, args, '-o')
        except SystemExit:
            self.fail('Unexpected system exit')
        self.assertRaises(SystemExit, b_cmdprs.check_file_out, prs,
                          prs.parse_args(['-o', 'test-data/']))
        self.assertRaises(SystemExit, b_cmdprs.check_file_out, prs,
                          prs.parse_args(['-o', 'test-data/config.txt']))
        b_cmdprs.check_file_out(prs,
                                prs.parse_args(['-o', 'test-data/config.txt']),
                                can_exist=True)

        # dir_out ------------------------------------------------------------
        prs = b_cmdprs.init()
        self.assertRaises(TypeError, b_cmdprs.add_dir_out)
        self.assertRaises(ValueError, b_cmdprs.add_dir_out, {})
        b_cmdprs.add_dir_out(prs)
        self.assertRaises(
            ArgumentError, b_cmdprs.add_dir_out, prs)  # Not allowed twice
        self._check_action(prs, 'o', 'Output directory', 'OUTPUT')
        self._check_action(b_cmdprs.add_dir_out(
            b_cmdprs.init(), '-o'), 'o', 'Output directory', 'OUTPUT')
        self._check_action(b_cmdprs.add_dir_out(
            b_cmdprs.init(), 'o'), 'o', 'Output directory', 'OUTPUT')
        self._check_action(b_cmdprs.add_dir_out(
            b_cmdprs.init(), 'a'), 'a', 'Output directory', 'OUTPUT')
        self._check_action(b_cmdprs.add_dir_out(
            b_cmdprs.init(), 'a', 'My OUTPUT'), 'a', 'My OUTPUT', 'OUTPUT')
        self.assertRaises(TypeError, b_cmdprs.check_dir_out)
        self.assertRaises(TypeError, b_cmdprs.check_dir_out, {})
        self.assertRaises(ValueError, b_cmdprs.check_dir_out, {}, {})
        self.assertRaises(ValueError, b_cmdprs.check_dir_out, prs, {})
        b_iotools.mkdirs('test-data/new_folder')
        args = prs.parse_args(['-o', 'test-data/new_folder'])
        try:
            b_cmdprs.check_dir_out(prs, args)
            b_cmdprs.check_dir_out(prs, args, 'o')
            b_cmdprs.check_dir_out(prs, args, '-o')
        except SystemExit:
            self.fail('Unexpected system exit')
        rmtree('test-data/new_folder')
        self.assertRaises(SystemExit, b_cmdprs.check_dir_out, prs,
                          prs.parse_args(['-o', 'test-data/config.txt']))
        self.assertRaises(SystemExit, b_cmdprs.check_dir_out, prs,
                          prs.parse_args(['-o', 'test-data/']),
                          can_exist=False)
        b_cmdprs.check_dir_out(prs, prs.parse_args(['-o', 'test-data/']),
                               can_exist=True)
        ap = path.abspath('test-data/test')
        b_cmdprs.check_dir_out(prs, prs.parse_args(['-o', 'test-data/test']),
                               can_exist=False, mk_dir=True, ch_dir=False)
        rmtree(ap)

        # bool ----------------------------------------------------------------
        prs = b_cmdprs.init()
        self.assertRaises(TypeError, b_cmdprs.add_bool)
        self.assertRaises(ValueError, b_cmdprs.add_bool, {})
        b_cmdprs.add_bool(prs)
        self.assertRaises(
            ArgumentError, b_cmdprs.add_bool, prs)  # Not allowed twice
        self._check_action(prs, 'b', 'Option', None, _StoreTrueAction)
        self._check_action(b_cmdprs.add_bool(
            b_cmdprs.init(), '-b'), 'b', 'Option', None,
            _StoreTrueAction)
        self._check_action(b_cmdprs.add_bool(
            b_cmdprs.init(), 'b', 'verbose'), 'b', 'verbose', None,
            _StoreTrueAction)

        # opt -----------------------------------------------------------------
        prs = b_cmdprs.init()
        self.assertRaises(TypeError, b_cmdprs.add_option)
        self.assertRaises(ValueError, b_cmdprs.add_option, {})
        b_cmdprs.add_option(prs)
        self.assertRaises(
            ArgumentError, b_cmdprs.add_option, prs)  # Not allowed twice
        self._check_action(prs, 's', 'Value', None, _StoreAction)
        self._check_action(b_cmdprs.add_option(
            b_cmdprs.init(), '-s'), 's', 'Value', 'VALUE')
        self._check_action(b_cmdprs.add_option(
            b_cmdprs.init(), 's', 'testlabel'), 's', 'testlabel', 'VALUE')
        self.assertRaises(TypeError, b_cmdprs.check_option)
        self.assertRaises(TypeError, b_cmdprs.check_option, {})
        self.assertRaises(ValueError, b_cmdprs.check_option, {}, {})
        self.assertRaises(ValueError, b_cmdprs.check_option, prs, {})
        args = prs.parse_args(['-s', 'Yo'])
        try:
            b_cmdprs.check_option(prs, args)
            b_cmdprs.check_option(prs, args, 's')
            b_cmdprs.check_option(prs, args, '-s')
            b_cmdprs.check_option(prs, prs.parse_args([]), optional=True)
            b_cmdprs.check_option(prs, prs.parse_args(['-s', '20']),
                                  is_int=True)
        except SystemExit:
            self.fail('Unexpected system exit')
        self.assertRaises(SystemExit, b_cmdprs.check_option, prs,
                          prs.parse_args([]))
        self.assertRaises(SystemExit, b_cmdprs.check_option, prs,
                          prs.parse_args(['-s', 'noint']), is_int=True)

        # fin -----------------------------------------------------------------
        sys.stdout = sys.__stdout__
        dnull.close()

    def _check_action(self, prs, letter, help, meta=None, ac=_StoreAction):
        a = self._get_action(prs, letter, ac)
        self.assertIsNotNone(a)
        self.assertEqual(a.help, help)
        if meta:
            self.assertEqual(a.metavar, meta)

    def _get_action(self, prs, arg, atype):
        for action in prs._get_optional_actions():
            print(action)
            if isinstance(action, atype) and action.dest == arg:
                return action

    # -------------------------------------------------------------------------

    def test_date(self):
        print('--- testing b_date')
        epoch = 946681200  # 01.01.2000 00:00.000
        ts = b_date.epoch_to_timestamp(epoch)
        dto = b_date.epoch_to_dto(epoch)
        dto_from_ts = b_date.timestamp_to_dto(ts)
        epoch_from_ts = b_date.timestamp_to_epoch(ts)
        ts_from_dto = b_date.dto_to_timestamp(dto)
        epoch_from_dto = b_date.dto_to_epoch(dto)

        self.assertEqual(epoch, epoch_from_ts)
        self.assertEqual(epoch, epoch_from_dto)
        self.assertEqual(dto, dto_from_ts)
        self.assertEqual(ts, ts_from_dto)
        self.assertRaises(ValueError, b_date.epoch_to_timestamp, None)
        self.assertRaises(ValueError, b_date.epoch_to_timestamp, 'string')
        self.assertRaises(ValueError, b_date.epoch_to_dto, None)
        self.assertRaises(ValueError, b_date.epoch_to_dto, 'string')
        self.assertRaises(ValueError, b_date.timestamp_to_dto, None)
        self.assertRaises(ValueError, b_date.timestamp_to_epoch, None)
        self.assertRaises(ValueError, b_date.dto_to_timestamp, None)
        self.assertRaises(ValueError, b_date.dto_to_epoch, None)

    def test_cmdline(self):
        print('--- testing b_shell')
        if 'windows' in b_shell.get_platform():
            command = 'cmd.exe'
        else:
            command = 'ls'
        assert b_shell.check_for_command(command)

    def test_daemon(self):
        print('--- testing b_daemon')

        class TestDaemon(b_daemon.Daemon):
            runs = 0

            def _run_daemon_process(self):
                # print ('daemon running. iteration #{}'.format(self.runs+1))
                self.runs += 1

        def start_daemon(daemon):
            daemon.start()

        daemon = TestDaemon(1)
        thread = Thread(target=start_daemon, args=(daemon,))
        thread.start()
        sleep(2)
        assert daemon.runs > 0
        daemon.stop()

    def test_enum(self):
        print('--- testing b_enum')
        my_enum = b_enum.enum('START', 'STOP')
        assert my_enum.START == 0
        assert my_enum.STOP == 1

    def test_iotools(self):
        print('--- testing b_iotools')

        assert (b_iotools.basename(
            '/somewhere/on/the/disc/filetype.css', '.css')
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
        b_iotools.import_modules_with_check(['numpy', 'math'])
        assert b_iotools.insertintofilename('test.txt', 'foo') == 'testfoo.txt'
        assert b_iotools.md5sum(
            'LICENSE') == '175792518e4ac015ab6696d16c4f607e'
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
        self.assertRaises(
            TypeError, b_iotools.get_immediate_subdirectories, None)
        self.assertRaises(
            TypeError, b_iotools.get_immediate_subdirectories, '')
        self.assertRaises(
            OSError, b_iotools.get_immediate_subdirectories, 'asdasf:321kds')
        temp_dir = mkdtemp()
        self.addCleanup(rmtree, temp_dir, True)
        self.assertEqual(
            0, len(b_iotools.get_immediate_subdirectories(temp_dir)))
        b_iotools.mkdirs(path.join(temp_dir, 'sub1'))
        b_iotools.mkdirs(path.join(temp_dir, 'sub2'))
        b_iotools.mkdirs(path.join(temp_dir, 'sub3'))
        self.assertEqual(
            3, len(b_iotools.get_immediate_subdirectories(temp_dir)))
        self.assertEqual(
            'sub1', b_iotools.get_immediate_subdirectories(temp_dir)[0])
        self.assertEqual(
            'sub2', b_iotools.get_immediate_subdirectories(temp_dir)[1])
        self.assertEqual(
            'sub3', b_iotools.get_immediate_subdirectories(temp_dir)[2])

        self.assertRaises(TypeError, b_iotools.read_csv_to_array)
        self.assertRaises(TypeError, b_iotools.read_csv_to_array, None)
        self.assertRaises(IOError, b_iotools.read_csv_to_array, 'doesnotexist')
        csv_data = b_iotools.read_csv_to_array(
            path.join('test-data', 'input.csv'))
        self.assertEqual(csv_data,
                         [
                             ['test line', '47', '12'], ['test', '47', '12']
                         ])

    def test_legacy(self):
        print('--- testing b_legacy')
        assert b_legacy.b_configparser()
        assert b_legacy.b_queue()
        assert b_legacy.b_urllib2()
        assert b_legacy.b_tk()

    def test_logging(self):
        print('--- testing b_logging')
        b_logging.setup_logging(True)

    def test_pil(self):
        print('--- testing b_pil')
        b_pil.resize_image_with_factor('test-data/image.jpg',
                                       './image-resized.jpg', 0.5)
        length = b_pil.get_length_of_long_side('test-data/image.jpg')
        assert length == 460
        length = b_pil.get_length_of_long_side('./image-resized.jpg')
        assert length == 230, length
        b_iotools.remove_silent('./image-resized.jpg')

    def test_strings(self):
        print('--- testing b_strings')
        assert b_strings.id_generator()
        assert b_strings.fillzeros('12', 4) == '0012'

    def test_threading(self):
        print('--- testing b_threading')
        cpus = b_threading.get_cpus()
        pool = b_threading.ThreadPool(cpus)
        for _ in range(0, 10):
            pool.add_task(self._random_calculation)
        pool.wait_completion()
        assert pool.is_empty()

    def test_visual(self):
        print('--- testing b_visual')
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
                                   y_axis_datalabels, x_axis_isdatetime, title,
                                   x_label, y_label, fontsize, fontweight,
                                   '%d.%m.%Y\n%H:%M', False)
        except Exception:
            pass

    def test_web(self):
        print('--- testing b_web')
        content = b_web.download_webpage_to_list('http://www.google.de')
        assert len(content) > 0

    def _random_calculation(self):
        randint(1, 100) + randint(1, 100)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        unittest.main()
    else:
        suite = BptbxTestSuite()
        method_name = 'test_{}'.format(sub('^b_', '', sys.argv[1]))
        method = None
        try:
            method = getattr(suite, method_name)
        except AttributeError:
            raise NotImplementedError(
                'Class `{}` does not implement `{}`'.format(
                    suite.__class__.__name__, method_name))
        method()
