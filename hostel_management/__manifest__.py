{
    "name": "Hostel Management",
    'author': "mirve",
    'website': "https://www.mirve.in",
    'display_name': """Hostel Management by mirve""",
    "application":True,
    'installable': True,
    'sequence': -100,
    'depends': [
        'base',
        'mail',
    ],
    "data": [
        'data/sequence_data.xml',
        'security/ir.access.csv',
        'view/hostel_room_views.xml',
        'view/hostel_facility_views.xml',
        'view/hostel_student_views.xml',
        'view/hostel_menus.xml',
        'data/hostel_facility_demo.xml',

    ]
}