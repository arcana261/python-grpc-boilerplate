import os
import sys
import itertools
import json

_NONE = object()


class SettingManager:
    _sentry = object()

    def __init__(self):
        self.env = os.getenv('ENV', 'prd')

        try:
            self._default = __import__('settings.default', fromlist=['*'])
        except ModuleNotFoundError:
            self._default = object()

        try:
            self._env = __import__('settings.{}'.format(self.env), fromlist=['*'])
        except ModuleNotFoundError:
            self._env = object()

        self._loaded = []

    def load(self, filename, fmt='json'):
        filename = os.path.abspath(filename)
        if fmt == 'json':
            with open(filename) as f:
                self._loaded.append((filename, json.load(f)))

    def unload(self, filename):
        filename = os.path.abspath(filename)
        self._loaded = [(f, v) for f, v in self._loaded if f != filename]

    def __getattr__(self, item):
        result = SettingManager._sentry

        for _, values in self._loaded:
            if item in values:
                result = values[item]

        result = os.getenv(item, result)

        if result is SettingManager._sentry:
            result = getattr(self._env, item, getattr(self._default, item, SettingManager._sentry))
            if result is SettingManager._sentry:
                raise AttributeError

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
        return iter(filter(lambda x: not x.startswith('_'),
                    set(itertools.chain(getattr(self._default, '__dict__', dict()).keys(),
                                        getattr(self._env, '__dict__', dict()).keys()))))


sys.modules[__name__] = SettingManager()
