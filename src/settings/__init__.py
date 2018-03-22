import os
import sys
import itertools
import json

_NONE = object()


class SettingManager:

    def __init__(self):
        # what is current environment?
        # assume default environment to be production
        self.env = os.getenv('ENV', 'prd')

        try:
            # try to read default settings
            self._default = __import__('settings.default', fromlist=['*'])
        except ModuleNotFoundError:
            # if default settings is not found, just assume empty object
            self._default = object()

        try:
            # try to read environment specific setting overrides
            self._env = __import__('settings.{}'.format(self.env), fromlist=['*'])
        except ModuleNotFoundError:
            # if environment specific settings is not found, just assume empty object
            self._env = object()

        # maintain list of other loaded settings
        self._loaded = []

    def load(self, filename, fmt='json'):
        """
        load settings from specified file
        :param filename:
        :param fmt: format of data to read
        :return:
        """
        filename = os.path.abspath(filename)
        if fmt == 'json':
            with open(filename) as f:
                self._loaded.append((filename, json.load(f)))

    def unload(self, filename):
        """
        unload settings that were read from file
        previously by calling load
        :param filename:
        :return:
        """
        filename = os.path.abspath(filename)
        self._loaded = [(f, v) for f, v in self._loaded if f != filename]

    def __getattr__(self, item):
        # empty object that can denote empty
        # or None result. It's better than using
        # None because None can be intended
        # value of a setting
        sentry = object()

        # assume result to be empty
        result = sentry

        # first try to read setting from loaded
        # files.
        # the files are traversed in order
        # so that newly added files
        # may override settings from older ones
        for _, values in self._loaded:
            if item in values:
                # don't break, continue because
                # some newer file may have setting
                # which overrides this file
                result = values[item]

        # try to read setting from environment
        # variable of same name
        # if environment variable is present
        # it can override setting defined
        # in manually loaded files
        result = os.getenv(item, result)

        if result is sentry:
            # if result is still sentry, then specified
            # setting is not in loaded config files
            # nor it is in environment variables
            # try to read setting using default data
            # and environment specific data
            result = getattr(self._env, item, getattr(self._default, item, sentry))
            if result is sentry:
                # if still not found
                # throw error
                raise AttributeError

        # return result
        return result

    def __contains__(self, item):
        try:
            self.__getattr__(item)
            return True
        except AttributeError:
            return False

    def get(self, item, default=_NONE):
        try:
            return self.__getattr__(item)
        except AttributeError:
            if default is not _NONE:
                return default
            raise AttributeError

    def __iter__(self):
        chained = itertools.chain(getattr(self._default, '__dict__', dict()).keys(),
                                  getattr(self._env, '__dict__', dict()).keys())

        for _, values in self._loaded:
            chained = itertools.chain(chained, values.keys())

        return iter(filter(lambda x: not x.startswith('_'), set(chained)))


sys.modules[__name__] = SettingManager()
