import click

from vladpy_telegram_ro_bot._application import Application


# TODO version option


@click.command()
def main() -> None:
	Application().run()


if __name__ == '__main__':
	main()
