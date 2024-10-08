==============================
Coupons multi product criteria
==============================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Production%2FStable-green.png
    :target: https://odoo-community.org/page/development-status
    :alt: Production/Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fsale--promotion-lightgray.png?logo=github
    :target: https://github.com/OCA/sale-promotion/tree/14.0/sale_coupon_criteria_multi_product
    :alt: OCA/sale-promotion
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/sale-promotion-14-0/sale-promotion-14-0-sale_coupon_criteria_multi_product
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/296/14.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This module allows to define complex rules on products to fulfill the conditions
of a coupon program, so for a given set of products we could define a minimum quantity
and another for others, being all those criterias mandatory for the coupon to be
applied.

**Table of contents**

.. contents::
   :local:

Configuration
=============

To configure multiple product criterias:

#. Go to *Sales > Catalog > Coupon Programs* and select or create a new one.
#. On the *Coupon Criteria* field choose *Multi Product*.
#. The standard domain will be hidden and a criteria list will be shown.
#. Add as many criterias as needed for the desired promotion behavior.

In the list of criterias we can configure:

- Qty: The minimum quantity of products in the sale order to fulfill the condition.
- Products: The products that should be present to fulfill the condition.
- Repeat: The sum of quantities of any product in the criteria must be at least the one
  defined in the minimum quantities. If not set, the minimum quantity will be the number
  of products defined in the criteria, as all of them must be in the order to fulfill
  the condition.

Some examples:

 ===== ================ ========
  Qty      Products      Repeat
 ===== ================ ========
    1   Prod A
 ===== ================ ========

A unit of Product A must be in the sale order.

 ===== ================ ========
  Qty      Products      Repeat
 ===== ================ ========
    2   Prod B, Prod C
 ===== ================ ========

A unit of Product B and Product C must be in the sale order.

 ===== ================ ========
  Qty      Products      Repeat
 ===== ================ ========
    3   Prod D, Prod E   X
 ===== ================ ========

Either Product D or Product E or both must be in the sale order and the sum of their
quantities must be three.

Also note that all the defined criterias must be fulfilled or the program won't be
applied.

Usage
=====

Once configured, apply the programs as usual.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/sale-promotion/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/sale-promotion/issues/new?body=module:%20sale_coupon_criteria_multi_product%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Tecnativa

Contributors
~~~~~~~~~~~~

* `Tecnativa <https://www.tecnativa.com>`_:

  * Pedro M. Baeza
  * David Vidal

* `Domatix <https://www.domatix.com>`_:

  * Álvaro López Oró

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-chienandalu| image:: https://github.com/chienandalu.png?size=40px
    :target: https://github.com/chienandalu
    :alt: chienandalu

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-chienandalu| 

This module is part of the `OCA/sale-promotion <https://github.com/OCA/sale-promotion/tree/14.0/sale_coupon_criteria_multi_product>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
