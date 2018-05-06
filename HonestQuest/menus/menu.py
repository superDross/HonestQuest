from HonestQuest.utils.print_text import print_centre
from HonestQuest.utils.common import sleep


class Menu(object):
    ''' Base class for all menus.

    Attributes:
        options (dict): {option (str): method (func)}
        choices (str): string representation of _options.
        parent (Menu): menu object above this menu,
    '''

    def __init__(self,  options, choices, parent=None):
        self.parent = parent
        self.options = self._add_parent_to_options(options)
        self.choices = self._add_back_to_choices(choices)

    def handle_options(self):
        ''' Extract and execute a method from self.options.'''
        try:
            print_centre(self.choices)
            choice = input('>> ')
            item = self.options[choice]
            return item
        except KeyError:
            msg = '{} is not a valid choice. Try again.\n'
            print_centre(msg.format(choice))
            sleep()
            return self.handle_options()

    def _add_parent_to_options(self, options):
        ''' Modify options to include parent menu.'''
        if self.parent:
            number_options = len(options)
            new_option_key = str(number_options + 1)
            options[new_option_key] = self.parent
        return options

    def _add_back_to_choices(self, choices):
        ''' Modify choices to include back option to parent menu.'''
        if not self.parent:
            return choices
        num = len(self.options)
        if choices:
            return '{}\n{}. Back'.format(choices, num)
        else:
            return '{}. Back'.format(num)


# class SubMenu(Menu):
#     ''' Base class for a Menu underneath a parent Menu.
# 
#     Attributes:
#         parent (Menu): menu object above this sub menu
#         _options (dict): {option (str): method (func)}
#         choices (str): string representation of _options
#     '''
# 
#     def __init__(self, options, choices, parent):
#         self.parent = parent
#         self.options = self.add_parent_to_options(options)
#         self.choices = self.add_back_to_choices(choices)
#         Menu.__init__(self, self.options, self.choices)
# 
#     def add_parent_to_options(self, options):
#         ''' Modify options to include parent menu.'''
#         if not isinstance(self.parent, Menu):
#             raise ValueError('{} is not Menu type'.format(self.parent))
#         number_options = len(options)
#         new_option_key = str(number_options + 1)
#         options[new_option_key] = self.parent
#         return options
# 
#     def add_back_to_choices(self, choices):
#         ''' Modify choices to include back option to parent menu.'''
#         num = len(self.options)
#         if choices:
#             return '{}\n{}. Back'.format(choices, num)
#         else:
#             return '{}. Back'.format(num)
