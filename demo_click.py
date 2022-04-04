import click


@click.command
@click.argument('message')
@click.option('--count', default=1, help='Number of messages')
def test(message, count):
    for _ in range(count):
        print(message)


if __name__ == "__main__":
    test()
