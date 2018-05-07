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

    @classmethod
    def from_list(cls, l):
        ''' Constructs self._options and self.choices from a list.

        Args:
            l (list: str): list of strings to transform into a Menu.
        '''
        options = {str(k + 1): i for k, i in enumerate(l)}
        choices = '\n'.join('{}. {}'.format(k, i)
                            for k, i in sorted(options.items()))
        return cls(options, choices)
