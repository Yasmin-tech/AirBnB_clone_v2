#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from models.state import State
import unittest
import os
from sqlalchemy import Column
import MySQLdb
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
from models import storage

class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    # @unittest.skipIf(os.environ.get("HBNB_TYPE_STORAGE") != "db", "This is only for db storage")
    """
    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), Column)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
    """
"""
my_sql_user = os.environ.get("HBNB_MYSQL_USER")
my_sql_pwd = os.environ.get("HBNB_MYSQL_PWD")
my_sql_db = os.environ.get("HBNB_MYSQL_DB")
my_sql_host = os.environ.get("HBNB_MYSQL_HOST")
db = MySQLdb.connect(host=my_sql_host, port=3306, user=my_sql_user, passwd=my_sql_pwd, db=my_sql_db)
cur = db.cursor()
"""
"""
class Test_City_sql(unittest.TestCase):
    \"\"\"This test is for the City class which is mapped to
        the sql table with <cities>
    \"\"\"
    # db = ""
    # cur = ""

    def __init__(self, *args, **kwargs):
        """ """
        self.my_sql_user = os.environ.get("HBNB_MYSQL_USER")
        self.my_sql_pwd = os.environ.get("HBNB_MYSQL_PWD")
        self.my_sql_db = os.environ.get("HBNB_MYSQL_DB")
        self.my_sql_host = os.environ.get("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=self.my_sql_host, port=3306, user=self.my_sql_user, passwd=self.my_sql_pwd, db=self.my_sql_db)
        self.cur = self.db.cursor()

    @staticmethod
    def command_console(command):
        \"\"\"pass argument to the console\"\"\"
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(command)
            file = f.getvalue()
        return file.strip('\n')

    \"\"\"
    @classmethod
    def setUpClass(self):
        my_sql_user = os.environ.get("HBNB_MYSQL_USER")
        my_sql_pwd = os.environ.get("HBNB_MYSQL_PWD")
        my_sql_db = os.environ.get("HBNB_MYSQL_DB")
        my_sql_host = os.environ.get("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=my_sql_host, port=3306, user=my_sql_user, passwd=my_sql_pwd, db=my_sql_db)
        self.cur = self.db.cursor()
    \"\"\"

    @classmethod
    def tearDownClass(self):
        self.cur.close()
        self.db.close()

    def test_city(self):
        \"\"\"test if City object is created\"\"\"
        value = Test_City_sql.command_console('create State name="salau"')
        self.cur.execute("SELECT COUNT(*) FROM {}".format("cities"))
        count = self.cur.fetchone()[0]
        print(count)
        self.assertEqual(0, count)

        Test_City_sql.command_console('create City name="isiaq", state_id="{}"'.format(value))
        self.cur.execute("SELECT COUNT(*) FROM {}".format("cities"))
        count = self.cur.fetchone()[0]
        print(count)
        self.assertEqual(1, count)
 """
class TestCitySql(unittest.TestCase):
    """This test is for the City class which is mapped to
        the sql table with <cities>
    """
    #db = None
    #cur = None

    def setUp(self):
        """Setup method - run before each test method"""
        self.my_sql_user = os.environ.get("HBNB_MYSQL_USER")
        self.my_sql_pwd = os.environ.get("HBNB_MYSQL_PWD")
        self.my_sql_db = os.environ.get("HBNB_MYSQL_DB")
        self.my_sql_host = os.environ.get("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=self.my_sql_host, user=self.my_sql_user, passwd=self.my_sql_pwd, db=self.my_sql_db)
        self.cur = self.db.cursor()
        print(self.cur)

    def command_console(self, command):
        """pass argument to the console"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(command)
            file = f.getvalue()
        return file.strip('\n')

    def tearDown(self):
        """Teardown method - run after each test method"""
        self.cur.close()
        self.db.close()

    def test_city(self):
        """test if City object is created"""
        print(self.cur)
        value = self.command_console('create State name="yasmin"')
        value2 = self.command_console('create State name="salau"')
        self.cur.execute("SELECT COUNT(*) FROM {}".format("states"))
        for count in self.cur.fetchall():
            print(count)
        self.cur.execute("SELECT COUNT(*) FROM {}".format("cities"))
        # count = self.cur.fetchone()[0]
        count = self.cur.fetchall()
        print(count)
        # self.assertEqual(0, count)

        self.command_console('create City name="kunle", state_id="{}"'.format(value2))
        value1 = self.command_console('create City name="mahmud", state_id="{}"'.format(value))
        # self.cur.execute("SELECT COUNT(*) FROM states JOIN cities ON states.id = cities.state_id WHERE cities.id = %s", (value,))
        self.cur.execute("SELECT COUNT(*) FROM cities")
        #for row in self.cur.fetchall():
        #    print(row)
        # count = self.cur.fetchone()[0]
        for count in self.cur.fetchall():
            print(count)
        # self.assertEqual(1, count)

