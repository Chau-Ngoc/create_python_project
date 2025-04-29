from jinja2 import DictLoader, Environment, select_autoescape

from create_python_project.renderer import TemplateRenderer
from create_python_project.utils import render_to_file


def test_render_to_file(tmp_path):
    env = Environment(loader=DictLoader({"test.txt.jinja": "Hello {{ name }}"}), autoescape=select_autoescape())
    renderer = TemplateRenderer(env)

    fn = tmp_path / "test.txt"
    render_to_file(renderer, "test.txt.jinja", fn, name="Chau")

    assert fn.read_text() == "Hello Chau"
