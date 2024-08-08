{
    'name': 'Mass Mailing Automation',
    'summary': 'Module for Automation mass mailing',
    'description': 'Module for Automation mass mailing',
    'version': '14.0.1.0.1',
    'author': 'SUNNIT',
    'category': 'Marketing/Email Marketing',
    'contributors': [
        'Hendrix Costa <hendrix@sunnit.com.br>',
        'Rafael Lima <lima@sunnit.com.br>',
    ],
    'depends': [
        'mass_mailing_base'
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/utm_stage.xml',
        'data/menu_security.xml',
        'data/ir_sequence.xml',


        'views/utm_stage.xml',
        'views/utm_campaign_views.xml',
        'views/mail_template_views.xml',
        'views/mailing_mailing_view.xml',
        'views/base_menu.xml',

        'wizard/utm_campaign_schedule_date_views.xml',
    ],
    'demo': [
    ],
    'application': True,
    "installable": True,
    'post_init_hook': 'post_init_hook',

}
