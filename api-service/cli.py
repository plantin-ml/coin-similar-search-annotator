from api.services.tasks_creator import TasksCreator
from api.scripts.fill_data import fill_coin_data
from api.scripts.export_dataset import export_data
import click


@click.group()
def cli():
    pass


@click.command()
def create_tasks():
    TasksCreator().process()


@click.command()
def cli_fill_data():
    fill_coin_data()


@click.command()
def cli_export_dataset():
    export_data()


cli.add_command(create_tasks)
cli.add_command(cli_fill_data, 'fill-data')
cli.add_command(cli_export_dataset, 'export-dataset')

if __name__ == "__main__":
    cli()
