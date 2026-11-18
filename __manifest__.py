# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name' : 'Bufete de Abogados' ,
    'version' : '18.0.1.0.0',
    'sequence': 16,
    'category' : 'Legal',
    'summary' : 'Sistema integral para la gestión de bufetes de abogados, Asoría Legal y Casos',
    'description': """
Sistema de Gestión de Bufete de Abogados
========================
Un módulo integral diseñado para gestionar bufetes de abogados, incluyendo la gestión de casos,
asignación de abogados, horarios de tribunales, interacciones con clientes y gestión documental.
""",
    'author' : 'Abuelgasem',
    'depends' : ['base','base_setup',
                 'hr','mail', 'contacts','sale',
                 'product',] ,
    'data' : [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/case_stage_data.xml',
        'views/dashboard_views.xml',
        'views/legal_advice_view.xml',
        'views/configuration_views.xml',
        'views/lawyer_view.xml',
        'views/inherit_hr_employee_view.xml',
        'views/inherit_res_partner_view.xml',
        'views/case_view.xml',
        'views/inherit_prudoct_template_view.xml',
        'views/inhert_sale_orde_view.xml',
        'views/menu.xml',
        'wizard/case_report_wizard_menu.xml',
        'wizard/case_report_wizard_view.xml',
        'wizard/lawyer_case_report_wizard_menu.xml',
        'wizard/lawyer_case_report_wizard_views.xml',
        'report/report_case_template.xml',
        'report/report_lawyer_case_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'bufete_de_abogados/static/src/css/dashboard.css',
            'bufete_de_abogados/static/src/js/dashboard.js',
            'bufete_de_abogados/static/src/xml/dashboard.xml',
        ],
    },
    'license': 'LGPL-3',

}