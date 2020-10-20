import click
from datapipes.run import DataSpigot
from actor import *

"""
1. CSV data is loaded by DataPipes via config
2. We can turn on the spigot at any time
3. Need to setup the monte carlo here?
"""

@click.command()
@click.option('--cfg', default='config.yml', help='The application YAML configuration file.')
# @click.option('--version', default=True, is_flag=True, help='Print the application version.')
def main(cfg):

    dataSpigot = DataSpigot(cfg,version=True)
    dataSpigot.on()
    # actors_neo.close()

    return 0


if __name__ == '__main__':
    main()
