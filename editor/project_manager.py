from config_manager import get_projects
from Config import Config
from Project import Project

def load_project(config: Config):
    projects: list[Project, ...] = get_projects(config)
    if config.current_project_name == ':new':
        config.current_project = Project()
    elif config.current_project_name in projects:
        config.current_project = projects[config.current_project_name]

    config.current_project.load(config)

def save_project(config: Config):
    #TODO: project saving and management
    pass