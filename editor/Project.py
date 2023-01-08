import os.path
from common import if_joined_does_not_exist_remake_it

class Project:
    # Info on data structure:
    # 0 - global 1 - yes 2 - no for global / project settings (gps)

    path: str = None
    name: str = ':new'
    title: str = 'Untitled'
    files_opened: list[int, ...] = []
    indexes: list[dict[int, str], ...] = []
    allow_multiple_commands: int = 0 # gps

    def __repr__(self):
        return self.name

    def load(self, config):
        if not self.path:
            if_joined_does_not_exist_remake_it(config.cache_folder, "project_temp")
            self.path = os.path.join(config.cache_folder, "project_temp")
            return
        #TODO: add loading of project file and information