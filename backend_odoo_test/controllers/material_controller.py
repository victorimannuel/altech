# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import werkzeug
import json

from sympy import false

from odoo import http
from odoo.http import request, Response


class MaterialController(http.Controller):

    # Endpoint to get all materials (GET)
    @http.route('/api/materials', auth='public', methods=['GET'])
    def get_materials(self, **kwargs):
        materials = request.env['material.material'].search([])
        result = []
        for material in materials:
            result.append({
                'id': material.id,
                'name': material.name,
                'code': material.code,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id,
            })

        try:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json, charset=utf-8',
                response=json.dumps(result),
            )
        except:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json, charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_desc': 'Error Description',
                })
            )

    # Endpoint to get material with id (GET)
    @http.route('/api/materials/<int:material_id>', auth='public', methods=['GET'])
    def get_material(self, material_id, **kwargs):
        material = request.env['material.material'].sudo().browse(material_id)
        result = {}
        if not material.exists():
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json, charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_desc': 'Material not found',
                })
            )

        result.update({
            'id': material.id,
            'name': material.name,
            'code': material.code,
            'type': material.type,
            'buy_price': material.buy_price,
            'supplier_id': material.supplier_id.id,
        })

        try:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json, charset=utf-8',
                response=json.dumps(result),
            )
        except:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json, charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_desc': 'Error Description',
                })
            )

    # Endpoint to update material (PUT)
    # @http.route('/api/materials/<int:material_id>', auth='public', methods=['PUT'])
    @http.route('/api/materials/<int:material_id>', auth='public', methods=['PUT'], csrf=False) # csrf=False
    def update_material(self, material_id, **kwargs):
        material = request.env['material.material'].sudo().browse(material_id)
        if not material.exists():
            # return {'error': 'Material not found'}
            return Response('Material not found', status=400)

        result = {}
        material_data = {}
        # Update fields based on provided data
        if 'name' in kwargs:
            material_data.update({'name': kwargs['name']})
            result.update({'name': kwargs['name']})
        if 'code' in kwargs:
            material_data.update({'code': kwargs['code']})
            result.update({'code': kwargs['code']})
        if 'type' in kwargs:
            material_data.update({'type': kwargs['type']})
            result.update({'type': kwargs['type']})
        if 'buy_price' in kwargs:
            material_data.update({'buy_price': kwargs['buy_price']})
            result.update({'buy_price': int(kwargs['buy_price'])})
        if 'supplier_id' in kwargs:
            material_data.update({'supplier_id': kwargs['supplier_id']})
            result.update({'supplier_id': kwargs['supplier_id']})

        # Update data using write function
        material.write(material_data)
        try:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json, charset=utf-8',
                response=json.dumps(result),
            )
        except:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json, charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_desc': 'Error Description',
                })
            )
        # return Response('Material updated successfully', status=200)

    # Endpoint to delete material (DELETE)
    # @http.route('/api/materials/<int:material_id>', auth='public', methods=['DELETE'])
    @http.route('/api/materials/<int:material_id>', auth='public', methods=['DELETE'], csrf=False) # csrf=False
    def delete_material(self, material_id, **kwargs):
        material = request.env['material.material'].sudo().browse(material_id)
        if not material.exists():
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json, charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_desc': 'Material not found',
                })
            )

        # Delete material
        material.unlink()
        try:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json, charset=utf-8',
                response=json.dumps({
                    'success': 'Material deleted successfully'
                }),
            )
        except:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json, charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_desc': 'Error Description',
                })
            )
