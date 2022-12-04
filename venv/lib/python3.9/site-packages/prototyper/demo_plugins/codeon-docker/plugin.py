import os
from pathlib import Path
from prototyper.plugins import PluginBase
from prototyper.plugins.template import build_template


TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


EXTRA_SETTINGS = """STATIC_ROOT = os.path.join(BASE_DIR, '..', 'files', 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'files', 'media')
FILE_UPLOAD_PERMISSIONS = 0o644

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)
"""


class Plugin(PluginBase):
    def on_build_complete(self):
        root = os.path.basename(self.build.project.path)
        context = dict(root=root, proj_name=self.build.project.name)
        build_to = os.path.dirname(self.build.build_path)
        build_template(TEMPLATE, build_to, context)
        self._patch_settings_py()
    
    def _patch_settings_py(self):
        f = Path(self.build.settings_pckg_path) / 'settings.py'
        s = f.read_text()
        s += EXTRA_SETTINGS
        s.replace(
            "os.path.join(BASE_DIR, 'db.sqlite3')",
            "os.path.join(BASE_DIR, '..', 'files', 'run', 'database.sqlite')",
        )
        f.write_text(s)
