{
    'name': "Account Account Flow",
    'description': """
        Se genera el flujo de contabilidad
    """,

    'author': "Tonny Velazquez Juarez",
    'website': "corner.store59@gmail.com",

    'category': 'account_payment_flow',
    "version": '15.0.1.0.0',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_flow_view.xml',
        'views/account_account_type_views.xml',
        # 'views/account_move.xml',
    ],
    "license": "Other proprietary",
}
