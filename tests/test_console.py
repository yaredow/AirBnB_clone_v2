#!/usr/bin/python3
"""test for console"""
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
from models.engine.db_storage import DBStorage
import models


class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        cls.consol = HBNBCommand()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.consol

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
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """test quit command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_EOF(self):
        with patch("sys.stdout", new=StringIO()):
            self.assertTrue(self.consol.onecmd("EOF"))

    def test_create(self):
        """Test create command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertEqual(
                "[[User]", f.getvalue()[:7])

    def test_show(self):
        """Test show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            object1 = f.getvalue()
        my_id = object1[object1.find('(')+1:object1.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_z_all(self):
        """Test alternate all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())

    def test_z_count(self):
        """Test count command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    def test_z_show(self):
        """Test alternate show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy_1(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_update_1(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("sldkfjsl.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            object1 = f.getvalue()
        my_id = object1[object1.find('(')+1:object1.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test_DB")
    def test_create_1(self):
        """Test create command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
            user = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertIn(user, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State")
            ste = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertIn(ste, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City")
            city1 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertIn(city1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place")
            plc = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Place")
            self.assertIn(plc, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review")
            rew = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Review")
            self.assertIn(rew, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity")
            amn = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Amenity")
            self.assertIn(amn, f.getvalue())

    @unittest.skipIf(type(models.storage) == FileStorage, "Test_FileStorage")
    def test_create_1(self):
        """Test create command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
            user = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertIn(user, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State")
            ste = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertIn(ste, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City")
            city1 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertIn(city1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place")
            plc = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Place")
            self.assertIn(plc, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review")
            rew = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Review")
            self.assertIn(rew, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity")
            amn = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Amenity")
            self.assertIn(amn, f.getvalue())

    @unittest.skipIf(type(models.storage) == FileStorage, "Test_FileStorage")
    def test_kwargs_dict_1(self):
        """Test kwargs"""
        with patch("sys.stdout", new=StringIO()) as f:
            get = ("create City name='Bogota'")
            self.consol.onecmd(get)
        with patch("sys.stdout", new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertIn("'name': 'Bogota'", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test_DB")
    def test_kwargs_dict(self):
        """Test kwargs"""
        with patch("sys.stdout", new=StringIO()) as f:
            get = ("create City name='Bogota'")
            self.consol.onecmd(get)
        with patch("sys.stdout", new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertIn("'name': 'Bogota'", f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "Test_DB")
    def test_update_2(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("mrrobot.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(whateveruser)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            object1 = f.getvalue()
        id_obj = object1[object1.find('(')+1:object1.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + id_obj + ")")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + id_obj + ", name)")
            self.assertEqual(
                "** value missing **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
