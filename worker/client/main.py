import click
from worker import Worker


@click.group(context_settings={"help_option_names": ['-h', '--help']})
@click.option('--server', default='http://localhost:18000', help='Server address.')
@click.pass_context
def cli(ctx, server):
    ctx.ensure_object(dict)
    ctx.obj['WORKER'] = Worker(server_address=server)


@cli.command('register')
@click.pass_context
def register(ctx):
    worker = ctx.obj['WORKER']
    response = worker.register()
    if 'worker_id' in response:
        click.echo(f"Registered with ID: {response['worker_id']}")
    else:
        click.echo("Registration failed.")


@cli.command('add_transaction')
@click.option('--key', required=True, help='Transaction key.')
@click.option('--value', required=True, help='Transaction value.')
@click.pass_context
def add_transaction(ctx, key, value):
    worker = ctx.obj['WORKER']
    transaction_data = {key: value}
    worker.add_transaction(transaction_data)
    click.echo(f"Transaction added: {transaction_data}")


@cli.command('get_id')
@click.pass_context
def get_id(ctx):
    worker = ctx.obj['WORKER']
    worker_id = worker.get_id()
    if worker_id:
        click.echo(f"Worker ID: {worker_id}")
    else:
        click.echo("Worker is not registered.")


@cli.command('get_leader')
@click.pass_context
def get_leader(ctx):
    worker = ctx.obj['WORKER']
    leader_id = worker.get_leader()
    if leader_id:
        click.echo(f"Leader ID: {leader_id}")
    else:
        click.echo("No leader information available.")


@cli.command('check_consistency')
@click.pass_context
def check_consistency(ctx):
    worker = ctx.obj['WORKER']
    if worker.check_consistency():
        click.echo("Blockchain data is consistent across all nodes.")
    else:
        click.echo("Blockchain data is not consistent.")


@cli.command('mine_block')
@click.pass_context
def mine_block(ctx):
    worker = ctx.obj['WORKER']
    new_block = worker.mine_block()
    if new_block:
        click.echo(f"New block mined: {new_block}")
    else:
        click.echo("Mining failed.")


@cli.command('get_chain')
@click.pass_context
def get_chain(ctx):
    worker = ctx.obj['WORKER']
    chain = worker.get_chain()
    click.echo(f"Current blockchain: {chain}")


@cli.command('dump_data')
@click.option('--db-url', help='Database URL')
@click.pass_context
def dump_data(ctx, db_url):
    worker = ctx.obj['WORKER']
    """Dump blockchain data into PostgreSQL database."""
    worker.connect_db(db_url)
    worker.dump_data()


@cli.command('stop_dump_data')
@click.pass_context
def stop_dump_data(ctx):
    worker = ctx.obj['WORKER']
    worker.stop_dump_data()


@cli.command('disconnect')
@click.pass_context
def disconnect(ctx):
    worker = ctx.obj['WORKER']
    worker.disconnect()


if __name__ == '__main__':
    cli(obj={})
