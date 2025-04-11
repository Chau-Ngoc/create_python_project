from os import PathLike
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

project_root_dir = Path(__file__).parents[1]
templates_dir = (project_root_dir / "templates").resolve()
examples_dir = (project_root_dir / "examples").resolve()
env = Environment(loader=FileSystemLoader(templates_dir), autoescape=select_autoescape())


class TemplateRenderer:
    def __init__(self, environment: Environment):
        self.environment = environment

    def render(self, template_name: str | PathLike, **kwargs) -> str:
        template = self.environment.get_template(template_name)
        return template.render(kwargs)


tpl_renderer = TemplateRenderer(env)
res = tpl_renderer.render("main.py.jinja", author="Chau")
test_res = tpl_renderer.render("test_main.py.jinja", author="Chau")
pprj_res = tpl_renderer.render(
    "pyproject.toml.jinja",
    author_name="Chau",
    author_email="playerzawesome@gmail.com",
    project_name="test",
    project_version="0.0.0_beta",
)

with open(examples_dir / "main.py", "w") as f:
    f.write(res)

with open(examples_dir / "test_main.py", "w") as f:
    f.write(test_res)

with open(examples_dir / "pyproject.toml", "w") as f:
    f.write(pprj_res)
