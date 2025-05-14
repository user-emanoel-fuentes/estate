{
    'name': 'Real Estate',
    'version': '17.0.0.0.0',
    'author':'Emanoel Fuentes',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data':[
        #SECURITY
        # 'security/res_groups.xml' ,
        'security/ir.model.access.csv',

        #VIEWS
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
    
        #MENU
        'views/estate_menu.xml',

    ],
    'demo':[
        # 'demo/demo.xml',
    ],
    'application': True,
}