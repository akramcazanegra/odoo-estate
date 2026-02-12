{ 
    "name": "Real Estate",
    "summary":"Test Module",
    "version": "19.0.0.0.0",
    "author": "Akram elmamoun",
    "website": "https://www.odoo.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "crm",
        "mail", 
    ],
    "data": [
        # Security Files
       "security/res_groups.xml",
       "security/ir.model.access.csv",
       "data/mail_template_data.xml",
       "security/ir_rule.xml",
        #Views
        
        "views/estate_property_view.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",

    ]
}