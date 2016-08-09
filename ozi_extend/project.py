# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Campos (danielcampos@avanzosc.es) Date: 08/09/2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
import urllib2
import urllib
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp.exceptions import Warning
from openerp import tools
import openerp.addons.decimal_precision as dp

Digits=dp.get_precision('Account')



class project_project(osv.osv):
    _inherit = 'project.project'

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image(value, size=(550, 350), )}, context=context)

    _columns = {

        'image': fields.binary(u"项目图片",
                               help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
                                        string=u"项目图片", type="binary", multi="_get_image",
                                        store={
                                            'project.project': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                                        },
                                        help="600X450"),
        'x_suburb': fields.char(u'Suburb', size=50,),
        'x_region': fields.char(u'区域', size=50),
        'x_project_address': fields.char(u'项目地址', size=120),
        'x_show_address': fields.char(u'展厅地址', size=120),
        'x_show_date': fields.char(u'开放时间', size=50),
        'x_price_range': fields.char(u'价格区间', size=50),
        'x_deal_time': fields.char(u'项目成交时间', size=50),
        'x_weixin_url': fields.char(u'微信项目介绍', size=300),
        'x_appointment_url': fields.char(u'预约', size=300),
        'x_reservation_url': fields.char(u'订房', size=300),
        'x_seafile_url': fields.char(u'Seafile', size=300),

    }

    def open_x_seafile_url(self, cr, uid, ids, context=None):
        project = self.browse(cr, uid, ids[0])
        url = project.x_seafile_url
        if not url:
            return True
        if 'http' not in url:
            url = 'http://' + url
        return self.open_url(url)

    def open_url(self, url):
        return {
            'name': 'url',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }
