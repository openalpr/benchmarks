'''
A setting is something that changes the behavior of ALPR.  It could be a config entry tweak
or a modification of the source code.

Each setting has a value, min/max, and a name/id.  It knows how to update its value with ALPR.
'''

import massedit
import os

class SettingType:
    INTEGER = 1
    FLOAT = 2

class AlprSetting:

    def __init__(self, name, minimum, maximum, initial_val, setting_type = SettingType.FLOAT):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum

        self.setting_type = setting_type

        self.initial_val = initial_val
        self.set_value(initial_val)

    def _update_alpr(self):
        # Managed in the child classes
        pass


    def update_value(self, value):
        self.value = value

    def get_minimum(self):
        return self.minimum

    def get_maximum(self):
        return self.maximum

    def get_value(self):
        return self.value

    def set_value(self, value):

        if self.setting_type == SettingType.INTEGER:
            self.value = int(value)
        else:
            self.value = value

        self.update_alpr()

    def finish(self):
        # Set the config setting back to where we started
        self.set_value(self.initial_val)

    def __str__(self):
         return self.name + " = " + str(self.value)

class AlprConfigSetting(AlprSetting):

    def update_alpr(self):
        filenames = ['/storage/projects/alpr/config/openalpr.conf']

        search_regex = self.name + '\s*=.*'
        replacement = self.name + ' = ' + str(self.value)

        devnull = open(os.devnull, 'w')
        massedit_command = "re.sub('%s', '%s', line)" % (search_regex, replacement)
        massedit.edit_files(filenames, [ massedit_command ], dry_run=False, output=devnull)
        devnull.close()

        print "  -- Setting - OpenALPR Config is being updated: " + replacement