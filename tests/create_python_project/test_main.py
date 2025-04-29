from pathlib import Path

import pytest
from click.testing import CliRunner
from jinja2 import TemplateNotFound

import create_python_project.main
from create_python_project.main import cli, create_default_project_path


@pytest.mark.parametrize("value, expected", [(None, Path.cwd()), ("/tmp", "/tmp"), (".", ".")])
def test_create_default_project_path(value, expected):
    res = create_default_project_path(None, None, value)
    assert res == expected


@pytest.mark.parametrize(
    "args, project_root_dir",
    [
        (
            [
                "--author_name",
                "Chau",
                "--author_email",
                "mail.com",
                "--project_name",
                "test_project",
                "--project_version",
                "0.1.0",
            ],
            "test_project",
        ),
        (
            [
                "--author_name",
                "Chau",
                "--author_email",
                "mail.com",
                "--project_name",
                "test_project",
                "--project_version",
                "0.1.0",
                ".",
            ],
            ".",
        ),
    ],
)
def test_cli(tmp_path_factory, args, project_root_dir):
    tmp_project_root = tmp_path_factory.mktemp("project_root")
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_project_root):
        result = runner.invoke(cli, args)
        assert result.exit_code == 0
        assert (
            f'New project is created in "{sorted(tmp_project_root.glob("**/src"))[0].parent.resolve()}"'
            in result.output
        )


@pytest.mark.parametrize(
    "exc, exc_message", [(TemplateNotFound, "Template Not Found!"), (FileExistsError, "Directory Exists!")]
)
def test_cli_raise_template_not_found(monkeypatch, tmp_path, exc, exc_message):
    def mock_render_to_file(*args, **kwargs):
        raise exc(exc_message)

    monkeypatch.setattr(create_python_project.main, "render_to_file", mock_render_to_file)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(
            cli,
            [
                "--author_name",
                "Chau",
                "--author_email",
                "mail.com",
                "--project_name",
                "test_project",
                "--project_version",
                "0.1.0",
                ".",
            ],
        )
        assert result.exit_code == 111
        assert exc_message in result.output
