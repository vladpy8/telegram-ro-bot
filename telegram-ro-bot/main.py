import click

from _application import Application


@click.command()
def main() -> None:
	Application().run()


if __name__ == '__main__':
	main()
