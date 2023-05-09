import os.path

from recipes.constants import default_email
from recipes.data_collection_util import DataCollection
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f", 
            "--file",
            type=str,
            help="Required 1 argument - path to excel file")
        
        parser.add_argument(
            "--email",
            type=str,
            default=default_email,
            help="Enter email for desired receipient"
        )

    def handle(self, *args, **options):
        if not options.get("file"):
            raise CommandError("Require file argument. See help for details.")
        if os.path.isfile(options["file"]):
            recipient = options["email"]
            DataCollection.collect_from_excel(options["file"], recipient)
        else:
            raise ValueError("Invalid file or path.")