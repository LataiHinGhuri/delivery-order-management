{
    'name': 'Delivery Order Management',
    'summary': """This module will create a project task after order confirmation for delevery management""",
    'version': '10.0.1.0',
    'description': """When we confirm a sale order it creates a task in a specific project.To do that you need to create a project first and create stages for that project. Then, Project id and the stage id for creating task needs to added to the code.""",
    'author': 'Metamorphosis',
    'company': 'Metamorphosis ltd.',
    'website': 'http://metamorphosis.com.bd/',
    'category': 'Tools',
    'images': [
        'static/description/delivery-banner.png',
        ],
    'license': 'OPL-1',
    'depends': ['sale','project'],
    'data': [
        'views/delivery_order.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 16,
    'currency': 'EUR',
}