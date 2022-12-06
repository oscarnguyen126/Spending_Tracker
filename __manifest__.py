{
    'name': 'Control Spending App',
    'author': 'Oscar Nguyen',
    'version': '15.0.1.0',
    'application': True,
    'installable': True,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'view/income_view.xml',
        'view/outcome_view.xml',
        'view/budget.xml',
        'view/category.xml',

        
        'view/main_menu.xml',
             ],
    'license': 'GPL-3',
}
