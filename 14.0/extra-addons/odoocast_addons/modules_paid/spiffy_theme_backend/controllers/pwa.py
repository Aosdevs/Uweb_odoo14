# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.

import json
from odoo import http
from odoo.http import request


class PwaMainBackend(http.Controller):

    def get_asset_urls(self, asset_xml_id):
        qweb = request.env['ir.qweb'].sudo()
        assets = qweb._get_asset_nodes(asset_xml_id, {}, True, True)
        urls = []
        for asset in assets:
            if asset[0] == 'link':
                urls.append(asset[1]['href'])
            if asset[0] == 'script':
                urls.append(asset[1]['src'])
        return urls

    @http.route('/backend/service_worker.js', type='http', auth="public", sitemap=False)
    def service_worker_backend(self):
        qweb = request.env['ir.qweb'].sudo()
        company_id = request.env.company.id
        lang_code = request.env.lang
        current_lang = request.env['res.lang']._lang_get(lang_code)
        mimetype = 'text/javascript;charset=utf-8'
        content = qweb._render('spiffy_theme_backend.service_worker_backend', {
            'company_id': company_id,
        })
        return request.make_response(content, [('Content-Type', mimetype)])

    @http.route('/pwa/backend/enabled', type='json', auth="public")
    def enabled_pwa_backend(self):
        company_id = request.env.company
        if company_id.enable_pwa_backend:
            return company_id.enable_pwa_backend
        else:
            return False

    @http.route('/pwa/offline', type='http', auth="public")
    def pwa_offline(self, **kw):
        return request.render('spiffy_theme_backend.pwa_offline_page',)

    @http.route('/spiffy_theme_backend/<int:company_id>/manifest.json', type='http', auth="public")
    def manifest(self, company_id=None):
        company = request.env['res.company'].search(
            [('id', '=', company_id)]) if company_id else request.env.company
        pwashortlist = []
        app_name_pwa_backend = company.app_name_pwa_backend
        short_name_pwa_backend = company.short_name_pwa_backend
        description_pwa_backend = company.description_pwa_backend
        background_color_pwa_backend = company.background_color_pwa_backend
        theme_color_pwa_backend = company.theme_color_pwa_backend
        start_url_pwa_backend = company.start_url_pwa_backend
        pwashortlistas = company.pwa_backend_shortcuts_ids
        image_192_pwa_backend = "/web/image/res.company/%s/image_192_pwa_backend/192x192" % (
            company.id)
        image_512_pwa_backend = "/web/image/res.company/%s/image_512_pwa_backend/512x512" % (
            company.id)
        qweb = request.env['ir.qweb'].sudo()
        mimetype = 'application/json;charset=utf-8'
        pwa_content = {
            "name": app_name_pwa_backend,
            "short_name": short_name_pwa_backend,
            "icons": [{
                "sizes": "192x192",
                "src": image_192_pwa_backend,
                "type": "image/png"
            }, {
                "sizes": "512x512",
                "src": image_512_pwa_backend,
                "type": "image/png"
            }],
            "start_url": start_url_pwa_backend,
            "display": "standalone",
            "scope": "/",
            "background_color": background_color_pwa_backend,
            "theme_color": theme_color_pwa_backend,
        }
        if pwashortlistas:
            for pwashorts in company.pwa_backend_shortcuts_ids:
                dict = {
                    "name": pwashorts.name,
                    "short_name": pwashorts.short_name,
                    "description": pwashorts.description,
                    "url": pwashorts.url,
                    "icons": [{"src": "/web/image/res.company/%s/image_192_shortcut" % (
                        company.id), "sizes": "192x192"}],
                }
                pwashortlist.append(dict)
                pwa_content.update({
                    'pwashortlistas': pwashortlist,
                })
        return request.make_response(
            data=json.dumps(pwa_content),
            headers=[('Content-Type', 'application/json')]
        )
