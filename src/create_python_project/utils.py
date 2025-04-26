import os


def render_to_file(renderer, template: str, fn: str | os.PathLike, **kwargs) -> None:
    res = renderer.render(template, **kwargs)
    with open(fn, "w") as f:
        f.write(res)
