import os
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


def render(renderer, template: str, fn: str | os.PathLike, **kwargs) -> None:
    res = renderer.render(template, **kwargs)
    with open(fn, "w") as f:
        f.write(res)


def create_default_project_path(ctx, param, value):
    if value is None:
        return Path.cwd()
    else:
        return value


@click.command()
@click.argument(
    "dest", required=False, type=click.Path(exists=True, file_okay=False), callback=create_default_project_path
)
@click.option("--author_name", help="The name of the author", prompt="Name of the project's author")
@click.option("--author_email", help="The email of the author", prompt="Email of the project's author")
@click.option(
    "--project_name",
    help="The name of the project. This will also be used to name your project root directory. Spaces will be replaced by underscores.",
    prompt="Project name",
)
@click.option(
    "--project_version",
    help="The version of the project",
    default="0.1.0",
    show_default=True,
    prompt="Project version",
)
def cli(author_name, author_email, project_name, project_version, dest):
    click.echo(f"{dest = }")
    project_name = re.sub(r"\s+", "_", project_name)

    if dest == Path.cwd():
        dest = (dest / project_name).resolve()
        dest.mkdir(exist_ok=False)
    else:
        dest = Path(dest).resolve()

    try:
        main_path = dest / "src" / project_name
        main_path.mkdir(parents=True)
        render(
            tpl_renderer,
            "main.py.jinja",
            main_path / "main.py",
            author_name=author_name,
            package_dir=project_name,
        )

        render(
            tpl_renderer,
            "pyproject.toml.jinja",
            dest / "pyproject.toml",
            project_name=project_name,
            project_version=project_version,
            author_name=author_name,
            author_email=author_email,
        )
        render(tpl_renderer, ".gitignore.jinja", dest / ".gitignore")
        render(tpl_renderer, ".pre-commit-config.yaml.jinja", dest / ".pre-commit-config.yaml")
        render(tpl_renderer, "README.md.jinja", dest / "README.md")

    except (TemplateNotFound, FileExistsError) as e:
        click.secho(e, err=True, fg="red")

    click.secho(f'New project is created in "{dest}"', fg="green")
