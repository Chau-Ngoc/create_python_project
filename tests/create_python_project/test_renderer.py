from jinja2 import DictLoader, Environment, select_autoescape

from create_python_project.renderer import TemplateRenderer


def test_init():
    env = Environment(loader=DictLoader({"test.txt.jinja": "Hello {{ name }}"}), autoescape=select_autoescape())
    renderer = TemplateRenderer(env)
    assert renderer.environment == env


def test_render():
    env = Environment(loader=DictLoader({"test.txt.jinja": "Hello {{ name }}"}), autoescape=select_autoescape())
    renderer = TemplateRenderer(env)
    assert renderer.render("test.txt.jinja", name="Chau") == "Hello Chau"
