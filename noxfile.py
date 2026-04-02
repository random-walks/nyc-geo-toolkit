#!/usr/bin/env -S uv run --script

# /// script
# dependencies = ["nox>=2025.2.9"]
# ///

from __future__ import annotations

import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()
PROJECT = nox.project.load_toml()

nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def lint(session: nox.Session) -> None:
    session.install("prek")
    session.run(
        "prek", "run", "--all-files", "--show-diff-on-failure", *session.posargs
    )


@nox.session
def pylint(session: nox.Session) -> None:
    session.install("-e.", "pylint>=3.2")
    session.run("pylint", "nyc_geo_toolkit", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    test_deps = nox.project.dependency_groups(PROJECT, "test")
    session.install("-e.[all]", *test_deps)
    session.run("pytest", "-m", "not integration", *session.posargs)


@nox.session(default=False)
def docs(session: nox.Session) -> None:
    doc_deps = nox.project.dependency_groups(PROJECT, "docs")
    session.install("-e.", *doc_deps)
    if session.interactive:
        session.run("mkdocs", "serve", "--clean", *session.posargs)
    else:
        session.run("mkdocs", "build", "--clean", *session.posargs)


@nox.session(default=False)
def build(session: nox.Session) -> None:
    build_path = DIR.joinpath("build")
    if build_path.exists():
        shutil.rmtree(build_path)
    session.install("build")
    session.run("python", "-m", "build")


if __name__ == "__main__":
    nox.main()
