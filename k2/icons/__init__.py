icons={}

def icon_html(name):
    cls=icons.get(name.lower(), icons.get('UNKNOWN'))
    return '<span aria-hidden="true" class="{cls}"></span>'.format(cls=cls)

class Icons(object):
    def __init__(self, app=None, **kw):
        self.app = app
        if app:
            self.init_app(app)
        self._init_kw(**kw)
            
    def _init_kw(self, **kw):
        if kw.get('icons'):
            icons = kw.get('icons')

            
    def init_app(self, app, **kw):
        self.app = app
        self._init_kw(**kw)
        app.jinja_env.globals.update(icon_html=icon_html)
        
    def html_function(self, func):
        icon_html = func
        if self.app:
            self.app.jinja_env.globals.update(icon_html=func)
            
    def icons(self, i):
        icons.update(i)