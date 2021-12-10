import os
import click
import requests
from .moodle import MoodleClient


CONTEXT_MOODLE_CLIENT_KEY = "MOODLE_CLIENT"


@click.pass_context
def get_moodle_client(ctx):
    return ctx.obj[CONTEXT_MOODLE_CLIENT_KEY]


@click.group()
@click.pass_context
def cli(ctx):
    moodle_url = os.getenv("MOODLE_URL")
    moodle_token = os.getenv("MOODLE_TOKEN")
    if not moodle_url or not moodle_token:
        click.echo(
            "Please set MOODLE_URL and MOODLE_TOKEN in your environment "
            "before running the CLI"
        )
        ctx.exit(1)

    moodle = MoodleClient(
        requests.Session(),
        moodle_url,
        moodle_token
    )

    ctx.obj = {
        CONTEXT_MOODLE_CLIENT_KEY: moodle
    }


@cli.command()
@click.argument("source_id")
@click.argument("course_name")
@click.argument("course_shortname")
@click.argument("course_category_id")
def copy_course(
    source_id, course_name, course_shortname, course_category_id
):
    """Copy course with SOURCE_ID to new course"""

    moodle = get_moodle_client()
    res = moodle.copy_course(
        source_id,
        course_name,
        course_shortname,
        course_category_id
    )
    click.echo(res)
