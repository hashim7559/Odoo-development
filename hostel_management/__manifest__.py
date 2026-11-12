# -*- coding: utf-8 -*-
{
    "name": "Hostel Management",
    'author': "mirve",
    'website': "https://www.mirve.in",
    'display_name': """Hostel Management by mirve""",
    "application":True,
    'installable': True,
    'auto_install': False,
    'sequence': -100,
    'depends': [
        'base',
        'mail',
        'contacts',
        'product',
        'account',
    ],
    "data": [
        'data/sequence_data.xml',
        'data/email_template_data.xml',
        'security/ir.access.csv',
        'view/hostel_room_views.xml',
        'view/hostel_facility_views.xml',
        'view/hostel_student_views.xml',
        'view/leave_request_views.xml',
        'wizard/available_room_views.xml',
        'view/hostel_menus.xml',

    ],
    "demo": [
        'demo/hostel_facility_demo.xml',
        'demo/rental_product_demo.xml',
    ]
}
