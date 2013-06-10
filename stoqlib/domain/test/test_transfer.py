# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2007 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

from stoqlib.domain.product import Product, ProductHistory
from stoqlib.domain.test.domaintest import DomainTest


class TestTransferOrderItem(DomainTest):

    def testGetTotal(self):
        order = self.create_transfer_order()
        item = self.create_transfer_order_item(order)
        self.assertEquals(item.get_total(), 625)


class TestTransferOrder(DomainTest):

    def testTransferProcess(self):
        order = self.create_transfer_order()
        self.assertEqual(order.can_send(), False)
        self.assertEqual(order.can_receive(), False)

        self.create_transfer_order_item(order)
        self.assertEqual(order.can_send(), True)
        self.assertEqual(order.can_receive(), False)

        order.send()
        self.assertEqual(order.can_send(), False)
        self.assertEqual(order.can_receive(), True)

        order.receive(self.create_employee())
        self.assertEqual(order.can_send(), False)
        self.assertEqual(order.can_receive(), False)

    def testSend(self):
        qty = 2
        order = self.create_transfer_order()
        item = self.create_transfer_order_item(order, quantity=qty)

        product = self.store.find(Product, sellable=item.sellable).one()
        storable = product.storable
        before_qty = storable.get_balance_for_branch(order.source_branch)
        order.send()
        after_qty = storable.get_balance_for_branch(order.source_branch)
        self.assertEqual(after_qty, before_qty - qty)

        history = self.store.find(ProductHistory, sellable=item.sellable).one()
        self.failIf(history is None)
        self.assertEqual(history.quantity_transfered, qty)

    def testReceive(self):
        sent_qty = 2
        order = self.create_transfer_order()
        item = self.create_transfer_order_item(order, quantity=sent_qty)
        order.send()

        storable = item.sellable.product_storable
        before_qty = storable.get_balance_for_branch(order.destination_branch)
        order.receive(self.create_employee())
        after_qty = storable.get_balance_for_branch(order.destination_branch)
        self.assertEqual(after_qty, before_qty + sent_qty)

    def testAddItem(self):
        order = self.create_transfer_order()

        item = self.create_transfer_order_item()
        order.add_item(item)
        self.assertEquals(item.transfer_order, order)

    def testRemoveItem(self):
        order = self.create_transfer_order()
        item = self.create_transfer_order_item(order)
        order.remove_item(item)

        order = self.create_transfer_order()
        item = self.create_transfer_order_item()
        self.assertRaises(ValueError, order.remove_item, item)

    def testGetSourceBranchName(self):
        order = self.create_transfer_order()
        self.assertEquals(order.get_source_branch_name(), u'Source')

    def testGetDestinationBranchName(self):
        order = self.create_transfer_order()
        self.assertEquals(order.get_destination_branch_name(),
                          u'Dest')

    def testGetSourceResponsibleName(self):
        order = self.create_transfer_order()
        self.assertEquals(order.get_source_responsible_name(),
                          u'Ipswich')

    def testGetDestinationResponsibleName(self):
        order = self.create_transfer_order()
        self.assertEquals(order.get_destination_responsible_name(),
                          u'Bolton')

    def testGetTotalItemsTransfer(self):
        order = self.create_transfer_order()
        self.create_transfer_order_item(order)
        self.assertEquals(order.get_total_items_transfer(), 5)
        self.create_transfer_order_item(order)
        self.assertEquals(order.get_total_items_transfer(), 10)
