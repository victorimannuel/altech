# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import requests
import random
import string
from odoo.tests.common import HttpCase
from odoo.tests import tagged

# The tests code in this file is referencing from code on another module

MATERIAL_ENDPOINT = '/api/materials/'

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class TestMaterialAPI(HttpCase):

    def get_base_url(self):
        """ Function to get base url from system parameter """
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return base_url

    def generate_material_data(self, num_records, test_supplier):
        """ Function to generate material data based on parameter """
        materials_data = []
        for i in range(num_records):
            material = {
                'name': f'Material_{i + 1}',  # Material_1, Material_2, etc.
                'code': generate_random_string(4),  # Random code of length 4
                'type': random.choice(['fabric', 'jeans', 'cotton']),  # Random type
                'buy_price': random.randint(100, 1000),  # Random buy price between 100 and 1000
                'supplier_id': test_supplier.id  # Supplier id from parameter
            }
            materials_data.append(material)
        return materials_data

    def create_materials(self, materials_data):
        """ Function to create material using Odoo ORM """
        for material_data in materials_data:
            self.env['material.material'].create(material_data)

    def setUp(self):
        """ Function to define all required fields in this class """
        super(TestMaterialAPI, self).setUp()

        # Prepare data to be compared later with api response
        # Create supplier test data
        self.test_supplier = self.env['res.partner'].create({
            'name': 'Supplier A',
        })

        # Create material test data
        num_records = 5
        dynamic_materials_data = self.generate_material_data(num_records, self.test_supplier)
        self.create_materials(dynamic_materials_data)

        # Get BASE URL that will be use combined later with API endpoint
        self.BASE_URL = self.get_base_url()

        # Get all material
        materials_all_obj = self.env['material.material'].search([])
        self.material_all = []
        for material in materials_all_obj:
            self.material_all.append({
                'id': material.id,
                'name': material.name,
                'code': material.code,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id,
            })

        # Get single material
        material_single_obj = self.env['material.material'].search([], limit=1)
        self.material_single = {
            'id': material_single_obj.id,
            'name': material_single_obj.name,
            'code': material_single_obj.code,
            'type': material_single_obj.type,
            'buy_price': material_single_obj.buy_price,
            'supplier_id': material_single_obj.supplier_id.id,
        }

    def test_1_get_all_material(self):
        """ Function to get all materials """
        # Call API
        endpoint = MATERIAL_ENDPOINT
        response = self.url_open(endpoint)
        parsed_response_content = json.loads(response.content)

        # Compare response status code, ensure 200 (means OK)
        self.assertEqual(response.status_code, 200)
        # Compare records and api response
        self.assertEqual(self.material_all, parsed_response_content)

        print(
            '''\n
            =================================================================
            = API test: GET /api/materials (using HttpCase) was succesfull! =
            =================================================================
            \n'''
        )

    def test_2_get_spesific_material(self):
        """ Function to get specific material using id """
        # Call API
        endpoint = MATERIAL_ENDPOINT + str(self.material_single.get('id'))
        response = self.url_open(endpoint)
        parsed_response_content = json.loads(response.content)

        # Compare response status code, ensure 200 (means OK)
        self.assertEqual(response.status_code, 200)
        # Compare records and api response
        self.assertEqual(self.material_single, parsed_response_content)

        print(
            '''\n
            ===================================================================================
            = API test: GET /api/materials/<int:material_id> (using HttpCase) was succesfull! =
            ===================================================================================
            \n'''
        )

    def test_3_update_material(self):
        """ Function to test update material """
        # Call API
        url = self.BASE_URL + MATERIAL_ENDPOINT + str(self.material_single.get('id'))
        payload = {'name': 'Updated Material Name', 'buy_price': 200}
        response = requests.put(url, payload)
        parsed_response_content = json.loads(response.content)

        # Compare response status code, ensure 200 (means OK)
        self.assertEqual(response.status_code, 200)
        # Compare records and api response
        self.assertEqual(payload, parsed_response_content)

        print(
            '''\n
            ===================================================================================
            = API test: PUT /api/materials/<int:material_id> (using HttpCase) was succesfull! =
            ===================================================================================
            \n'''
        )

    def test_4_delete_material(self):
        """ Function to test delete material """
        # Call API
        url = self.BASE_URL + MATERIAL_ENDPOINT + str(self.material_single.get('id'))
        response = requests.delete(url)

        # Check that the material record no longer exists
        material_exists = self.env['material.material'].search_count([
            ('id', '=', self.material_single.get('id'))
        ])

        # Compare response status code, ensure 200 (means OK)
        self.assertEqual(response.status_code, 200)
        # Check value
        self.assertFalse(material_exists, "The material record was not deleted successfully.")

        print(
            '''\n
            ======================================================================================
            = API test: DELETE /api/materials/<int:material_id> (using HttpCase) was succesfull! =
            ======================================================================================
            \n'''
        )
