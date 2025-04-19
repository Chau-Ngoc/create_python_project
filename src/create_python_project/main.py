import re
from os import PathLike
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader, TemplateNotFound, select_autoescape

templates_dir = "templates"
env = Environment(loader=PackageLoader("create_python_project", templates_dir), autoescape=select_autoescape())


class TemplateRenderer:
    def __init__(self, environment: Environment):
        self.environment = environment

    def render(self, template_name: str | PathLike, **kwargs) -> str:
        template = self.environment.get_template(template_name)
        return template.render(kwargs)


tpl_renderer = TemplateRenderer(env)


@click.command()
@click.argument("dest", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--author_name", help="The name of the author", prompt="Name of the project's author")
@click.option("--author_email", help="The email of the author", prompt="Email of the project's author")
@click.option(
    "--project_name",
    help="The name of the project. This will also be used to name your project root directory. Spaces will be replaced by underscores.",
    prompt="Project name",
)
def cli(author_name, author_email, project_name, dest):
    project_name = re.sub(r"\s+", "_", project_name)

    if dest == ".":
        dest = (Path.cwd() / project_name).resolve()
        dest.mkdir(exist_ok=False)
    else:
        dest = Path(dest).resolve()

    try:
        paths = ["src", "tests"]
        templates = ["main.py.jinja", "test_main.py.jinja"]
        file_names = ["main.py", "test_main.py"]

        for i, path in enumerate(paths):
            main_path = dest / path / project_name
            main_path.mkdir(parents=True)

            res = tpl_renderer.render(templates[i], author_name=author_name, package_dir=project_name)
            with open(main_path / file_names[i], "w") as f:
                f.write(res)

    except (TemplateNotFound, FileExistsError) as e:
        click.secho(e, err=True, fg="red")

    click.secho(f'New project is created in "{dest}"', fg="green")
