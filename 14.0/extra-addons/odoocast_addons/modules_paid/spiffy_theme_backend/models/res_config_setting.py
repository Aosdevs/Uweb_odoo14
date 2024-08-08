# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.

from odoo.modules.module import get_resource_path
from odoo import api, http, fields, models, tools, _
from odoo.http import request
import base64


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    spiffy_favicon = fields.Binary(related='company_id.favicon',
                            string="Backend Tab Favicon", readonly=False)
    tab_name = fields.Char(related='company_id.tab_name',
                           string="Backend Tab Name", readonly=False)
    backend_theme_level = fields.Selection(
        related='company_id.backend_theme_level', string="Backend Theme Level", required=True, readonly=False)

    login_page_style = fields.Selection(
        related='company_id.login_page_style', string="Login Styles", required=True, readonly=False)

    login_page_background_img = fields.Binary(
        related='company_id.login_page_background_img', string="Login Background Image", readonly=False)

    login_page_background_color = fields.Char(
        related='company_id.login_page_background_color', string='Login Background Color', readonly=False)

    login_page_text_color = fields.Char(
        related='company_id.login_page_text_color', string='Login Text Color', readonly=False)

    show_bg_image = fields.Boolean(
        related='company_id.show_bg_image', string='Add Login Background Image', readonly=False)

    backend_menubar_logo = fields.Binary(
        related='company_id.backend_menubar_logo', string="Menubar Logo", readonly=False)

    backend_menubar_logo_icon = fields.Binary(
        related='company_id.backend_menubar_logo_icon', string="Menubar Logo Icon", readonly=False)

    # Fields for PWA start
    enable_pwa_backend = fields.Boolean(
        string='Enable PWA', related='company_id.enable_pwa_backend', readonly=False,)
    app_name_pwa_backend = fields.Char(
        'App Name', related='company_id.app_name_pwa_backend', readonly=False)
    short_name_pwa_backend = fields.Char(
        'Short Name', related='company_id.short_name_pwa_backend', readonly=False)
    description_pwa_backend = fields.Char(
        'App Description', related='company_id.description_pwa_backend', readonly=False)
    image_192_pwa_backend = fields.Binary(
        'Image 192px', related='company_id.image_192_pwa_backend', readonly=False)
    image_512_pwa_backend = fields.Binary(
        'Image 512px', related='company_id.image_512_pwa_backend', readonly=False)
    start_url_pwa_backend = fields.Char(
        'App Start Url', related='company_id.start_url_pwa_backend', readonly=False)
    background_color_pwa_backend = fields.Char(
        'Background Color', related='company_id.background_color_pwa_backend', readonly=False)
    theme_color_pwa_backend = fields.Char(
        'Theme Color', related='company_id.theme_color_pwa_backend', readonly=False)
    pwa_backend_shortcuts_ids = fields.Many2many(
        related='company_id.pwa_backend_shortcuts_ids', readonly=False)
    # Fields for PWA end

    spiffy_toobar_color = fields.Char('Toolbar Color', related='company_id.spiffy_toobar_color', readonly=False)
