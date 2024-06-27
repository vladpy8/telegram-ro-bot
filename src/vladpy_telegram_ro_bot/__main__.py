import click

from vladpy_telegram_ro_bot._application._application import Application


# TODO feature: version option
# TODO fix: config path parameters


@click.command()
def main() -> None:
	Application().run()


if __name__ == '__main__':
	main()
