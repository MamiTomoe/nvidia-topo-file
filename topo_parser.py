from consts import LoggerFormats
from parsing.parser import Parser
from input_and_output.output import create_models_files, print_parsed_models
from input_and_output.input import read_parsed_files
import logging
import click

logging.basicConfig(level=logging.INFO,
                    format=LoggerFormats.LOGGER_FORMATER)
logger = logging.getLogger(__name__)


@click.command()
@click.option("-h", is_flag=True, help="Prints the usages and options")
@click.option("-p", is_flag=True, help="Print parsed topology")
@click.option("-f", is_flag=True, help="Parse topology. need topofile -f <topofile>")
@click.argument("topofile", type=click.Path(exists=True), required=False)
def cli(h, f, p, topofile=None):
    if h:
        help()
    elif f and topofile:
        parse_topology(topofile)
    elif p:
        print_topology()
    else:
        click.echo("No vaild option was chosen")


def help():
    logger.info("You can use -f to parse file.\nexample:topo_parser –f topofile.topo\n"
                "or you can use -p to print parsed topology.\n"
                "Example: topo_parser -p ")


def parse_topology(topofile):
    parser = Parser(topofile, logger)
    with click.progressbar(parser.get_models()) as bar:
        for models in bar:
            create_models_files(models)


def print_topology():
    for models in read_parsed_files():
        print_parsed_models(models)
    logger.info("Finished to print all the files!")



if __name__ == '__main__':
    # main()
    cli()

