# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2015 WT-IO-IT GmbH (https://www.wt-io-it.at)
#                    Mag. Wolfgang Taferner <wolfgang.taferner@wt-io-it.at>

{
    "name": "Belgium - First addon",
    "version": "1.0",
    "author": "NS-IO-IT GmbH, Wolfgang Taferner",
    "website": "https://www.nicolas-sciortino.com",
    "license": 'OEEL-1',
    "category": "Accounting/Accounting",
    'summary': "Belgian first addon",
    'description': """

Accounting reports for Austria.
================================

    * Defines the following reports:
        * Profit/Loss (§ 231 UGB Gesamtkostenverfahren)
        * Balance Sheet (§ 224 UGB)

    """,
    "depends": [],
    "data": ["views/myviews.xml", "views/partner.xml"
    ],
    'installable': True,
    'auto_install': True,

}