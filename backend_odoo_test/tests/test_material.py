# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.tests.common import SavepointCase, TransactionCase
from odoo.tests import tagged


# The tests code in this file is based on odoo documentation
# Reference: https://www.odoo.com/documentation/14.0/developer/tutorials/unit_tests.html
# Note: SavepointCase is used in Odoo 14 but deprecated in Odoo 15 and above


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class TestMaterialSavepointCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        """ Setup class to define all required fields in this class """
        # add env on self and many other things
        super(TestMaterialSavepointCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.

        # Create a new supplier with the test
        cls.test_supplier = cls.env['res.partner'].create({
            'name': 'Supplier A',
        })

        # Create a new material with the test
        cls.properties = cls.env['material.material'].create({
            'name': 'Pants',
            'code': 'A004',
            'type': 'jeans',
            'buy_price': 100,
            'supplier_id': cls.test_supplier.id,
        })

    def test_1_create_material(self):
        """ Function to create test material using"""
        # Check if the material record value match
        self.assertRecordValues(self.properties, [{
            'name': 'Pants',
            'code': 'A004',
            'type': 'jeans',
            'buy_price': 100,
            'supplier_id': self.test_supplier.id,
        },])

        print(
            '''\n
            ===============================================================
            = Function test: Create (using SavepointCase) was succesfull! =
            ===============================================================
            \n'''
        )

    def test_2_update_material(self):
        """ Function to test update material """
        self.properties.buy_price = 500

        # Check if the material record value match
        self.assertRecordValues(self.properties, [{
            'name': 'Pants',
            'code': 'A004',
            'type': 'jeans',
            'buy_price': 500,
            'supplier_id': self.test_supplier.id,
        },])

        print(
            '''\n
            ===============================================================
            = Function test: Update (using SavepointCase) was succesfull! =
            ===============================================================
            \n'''
        )

    def test_3_delete_material(self):
        """ Function to test delete material """
        # Delete material object
        self.properties.unlink()

        # Check that the material record no longer exists
        material_exists = self.env['material.material'].search_count([
            ('id', '=', self.properties.id)
        ])

        # Check value
        self.assertFalse(material_exists, "The material record was not deleted successfully.")

        print(
            '''\n
            ===============================================================
            = Function test: Delete (using SavepointCase) was succesfull! =
            ===============================================================
            \n'''
        )


# For Odoo 15 and above use TransactionCase because SavepointCase was merged into TransactionCase
class TestMaterialTransactionCase(TransactionCase):

    def test_create_data(self):
        # Create a new supplier with the test
        test_supplier = self.env['res.partner'].create({
            'name': 'Supplier B',
        })

        # Create a new material with the test
        test_material = self.env['material.material'].create({
            'name': 'Shirt',
            'code': 'A005',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': test_supplier.id,
        })

        # Check if the material record value match
        self.assertEqual(test_material.name, 'Shirt')
        self.assertEqual(test_material.code, 'A005')
        self.assertEqual(test_material.type, 'fabric')
        self.assertEqual(test_material.buy_price, 150)
        # Check if the supplier id in the material record is in fact the correct id
        self.assertEqual(test_material.supplier_id.id, test_supplier.id)

        print(
            '''\n
            =================================================================
            = Function test: Create (using TransactionCase) was succesfull! =
            =================================================================
            \n'''
        )

