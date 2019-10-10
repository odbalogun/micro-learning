from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'

    menu = [
        ParentItem(
            app='courses'
        ),
        ParentItem(
            app='discounts'
        ),
        ParentItem(
            app='payments'
        ),
        ParentItem(
            app='users'
        ),
        ParentItem(
            app='configurations'
        ),
        ParentItem(
            app='admin',
            label='Audit Trail'
        ),
    ]
