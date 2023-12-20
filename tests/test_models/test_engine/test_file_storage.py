#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.review import Review
from models.state import State
from models.place import Place
from models import storage
import os


@unittest.skipIf(os.environ.get("HBNB_TYPE_STORAGE") == "db", "skip if it's for DBStorage")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        storage.new(new)
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        new.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        storage.new(new)
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_all_with_class(self):
        """test if all instance of one type is returned"""
        self.assertEqual(0, len(storage.all(Review)))
        r1 = Review()
        r1.comment = "I love it"
        storage.new(r1)
        storage.save()
        self.assertEqual(1, len(storage.all(Review)))
        r2 = Review()
        r2.save()
        self.assertEqual(2, len(storage.all(Review)))

    def test_all_with_none(self):
        """test the all method with a none argument"""
        self.assertEqual(0, len(storage.all(Review)))
        r1 = Review()
        r1.save()
        self.assertEqual(1, len(storage.all(Review)))
        r2 = Review()
        r2.save()
        self.assertEqual(2, len(storage.all(Review)))

    def test_delete_obj(self):
        """confirm if an object is delete from the __objects dict"""
        self.assertEqual(0, len(storage.all()))
        s1 = State()
        storage.save()
        storage.delete(s1)
        self.assertEqual(0, len(storage.all()))
        r2 = Review()
        r2.save()
        storage.delete(r2)
        self.assertEqual(0, len(storage.all()))

    def test_delete_obj_with_none(self):
        """test the delete method with a none object"""
        self.assertEqual(0, len(storage.all()))
        p1 = Place()
        p1.save()
        storage.delete()
        self.assertEqual(1, len(storage.all()))
        b1 = BaseModel()
        b1.save()
        storage.delete()
        self.assertEqual(2, len(storage.all()))
