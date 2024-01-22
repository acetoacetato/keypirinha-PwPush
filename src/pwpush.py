# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import requests
import json 
import os


class pwpush(kp.Plugin):
    """
    One-line description of your plugin.

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html
    """

    



    
    ITEMCAT_INIT_COMMAND = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_SELECT_SHARING = kp.ItemCategory.USER_BASE + 2
    ITEMCAT_CREATE_LINK = kp.ItemCategory.USER_BASE + 3

    DEFAULT_SECTION = 'defaults'
    ALIAS_SECTION = 'aliases'

    DEFAULT_ITEM_ENABLED = True
    DEFAULT_ALWAYS_EVALUATE = True
    DEFAULT_ITEM_LABEL = 'Create Sharing Link (pwpush)'
    DEFAULT_ITEM_DESCRIPTION = 'Create Password/File Sharing Link using PwPush.com API'

    default_item_enabled = DEFAULT_ITEM_ENABLED
    always_evaluate = DEFAULT_ALWAYS_EVALUATE
    default_item_label = DEFAULT_ITEM_LABEL

    DEFAULT_VIEWS_NUMBER = 1
    DEFAULT_DAYS_NUMBER = 1
    DEFAULT_STEP_RETRIEVAL= 'true'
    
    ACTION_COPY_RESULT = 'copy_result'
    ACTION_COPY_URL = 'copy_url'
    ACTION_OPEN_URL = 'open_url'

    DEFAULT_API_EMAIL = None
    DEFAULT_API_KEY = None
    
    API_URL = 'https://pwpush.com'
    API_EMAIL = None
    API_KEY = None

    enabled = DEFAULT_ITEM_ENABLED



    def __init__(self):
        super().__init__()
        
    def pwpush(self):
        print('Tese')

    def on_start(self):
        self._read_config()

        actions = [
            self.create_action(
                name=self.ACTION_COPY_RESULT,
                label='Copy JSON result',
                short_desc='Copy API response (as JSON) to the clipboard.')
            ]
        self.set_actions(self.ITEMCAT_INIT_COMMAND, actions)
        pass

    def on_catalog(self):
        catalog = []

        if self.default_item_enabled:
            catalog.append(self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label=self.DEFAULT_ITEM_LABEL,
                short_desc=self.DEFAULT_ITEM_DESCRIPTION,
                target="pwpush",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS)
            )
            self.set_catalog(catalog)
        pass


    def on_suggest(self, user_input, items_chain):
        suggestions = []

        if not items_chain or items_chain[-1].category() != kp.ItemCategory.KEYWORD:
            return
        

        suggestions.append(self.create_item(
            category=self.ITEMCAT_SELECT_SHARING,
            label='Share Password',
            short_desc='Create a link using PwPush.com to share securely a password.',
            target='password',
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.IGNORE,
            data_bag=user_input
        ))
        if not(self.API_KEY == None or self.API_EMAIL == None) and os.path.isfile(user_input):
            suggestions.append(self.create_item(
                category=self.ITEMCAT_SELECT_SHARING,
                label='Share File',
                target='file',
                short_desc='Create a link using PwPush.com to share securely a file (Requires configuring api key).',
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
                data_bag=user_input
            ))

        if not user_input or user_input == '':
           return

        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)
        

    def on_execute(self, item, action):
        if item and item.category() == self.ITEMCAT_SELECT_SHARING:
            if item.target() == 'password':
                #url = self.API_URL + '/p.json'
                #head = {'Content-Type' : 'multipart/form-data'}
                #data = { 'password[payload]': item.data_bag() }
                #r = requests.post(url, data, head)
                #response = json.loads(r.text)
                response = json.loads(self._request_pwpush(item.data_bag(), False))
                kpu.set_clipboard(self.API_URL + '/en/p/' + response['url_token'])

            if item.target() == 'file' and os.path.isfile(item.data_bag()):
                #file = open(item.data_bag())
                #files = {'file_push[files][]' : (os.path.basename(file), file) }
                #head = {'X-User-Email' : self.API_EMAIL, 'X-User-Token': self.API_KEY}
                #url = self.API_URL + '/f.json'
                #print(head)
                #r = requests.post(url, files=files, headers=head)
                #print(r.text)
                response = json.loads(self._request_pwpush(item.data_bag(), True))
                kpu.set_clipboard(self.API_URL + '/en/f/' + response['url_token'])
    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        self._read_config()
        pass


    def _request_pwpush(self, input, is_file):
        url = f'{self.API_URL}/{("f" if is_file else "p")}.json'
        head = None if (not self.API_EMAIL or not self.API_KEY) else  {'X-User-Email' : self.API_EMAIL, 'X-User-Token': self.API_KEY}
        input = {'file_push[files][]' : (os.path.basename(input), input) } if is_file else { 'password[payload]': input }
        if is_file:
            return requests.post(url, files=input, headers=head).text
        else:
            return requests.post(url, input, headers=head).text

    def _read_config(self):
        def _warn_cur_code(name, fallback):
            fmt = (
                "Invalid {} value in config. " +
                "Falling back to default: {}")
            self.warn(fmt.format(name, fallback))

        settings = self.load_settings()

        self.API_KEY = settings.get(
            "api_key",
            section=self.DEFAULT_SECTION,
            fallback=self.DEFAULT_API_KEY)

        # [default_item]
        self.API_EMAIL = settings.get(
            "api_email",
            section=self.DEFAULT_SECTION,
            fallback=self.DEFAULT_API_EMAIL)




