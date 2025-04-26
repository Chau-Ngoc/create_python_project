from os import PathLike

from jinja2 import Environment


class TemplateRenderer:
    def __init__(self, environment: Environment):
        self.environment = environment

    def render(self, template_name: str | PathLike, **kwargs) -> str:
        template = self.environment.get_template(template_name)
        return template.render(kwargs)
