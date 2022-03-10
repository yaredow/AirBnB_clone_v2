#!/usr/bin/python3
"""test for console module"""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
import console
import tests
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from os import getenv


class TestConsole(unittest.TestCase):
    """test the console"""
    console = HBNBCommand()

    def setUp(self):
        """setup for the test"""
        pass

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.preloop.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.help_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.help_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.help_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.help_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.help_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.help_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.help_count.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.help_update.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual('', f.getvalue())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using db")
    def test_create(self):
        print(getenv("HBNB_TYPE_STORAGE") != "db")
        """Test create command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            self.assertTrue(f.getvalue() is not None)

    def test_create_db(self):
        """Test create command inpout DB"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California!"')
            s = f.getvalue()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all State")
            self.assertEqual(
                "[\"[State]", f.getvalue()[:9])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using db")
    def test_show(self):
        """Test show command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    # TODO: test_show_db
    # what works with show..

    def test_destroy(self):
        """Test destroy command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Everything")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 123456")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    # Wait should any of this work, what's the id we're working on
    def test_update(self):
        """Test update command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User " + my_id)
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_dot_all(self):
        """Test all command """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Butts.all()")
            self.assertEqual(
                '*** Unknown syntax: Butts.all()\n', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.all()")
            self.assertEqual("*** Unknown syntax: State.all()\n", f.getvalue())

    def test_dot_count(self):
        """Test count command """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Butts.count()")
            self.assertEqual(
                "*** Unknown syntax: Butts.count()\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.count()")
            self.assertEqual(
                "*** Unknown syntax: State.count()\n", f.getvalue())

    def test_dot_show(self):
        """Test show command """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Butts.show()")
            self.assertEqual(
                "*** Unknown syntax: Butts.show()\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "*** Unknown syntax: BaseModel.show(abcd-123)\n", f.getvalue())

    def test_dot_destroy(self):
        """Test destroy command """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Everything.destroy()")
            self.assertEqual(
                "*** Unknown syntax: Everything.destroy()\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.destroy(123456)")
            self.assertEqual(
                "*** Unknown syntax: User.destroy(123456)\n", f.getvalue())

    def test_dot_update(self):
        """Test destroy command """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Butts.update()")
            self.assertEqual(
                "*** Unknown syntax: Butts.update()\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update(123456)")
            self.assertEqual(
                "*** Unknown syntax: User.update(123456)\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update()")
            self.assertEqual(
                "*** Unknown syntax: User.update()\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
