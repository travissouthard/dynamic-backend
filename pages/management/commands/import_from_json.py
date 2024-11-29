from django.core.management.base import BaseCommand
from pages.helpers.data_helper import import_site_data

class Command(BaseCommand):
    help = """
        Imports data from a specified json file.
        File must be a dict of lists named 'art', 'blog', 'project', 'webring', 'resume'
        Each of those lists should have a dict matching helpers.data_helper.py
    """

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)
    
    def handle(self, **options):
        try:
            file_path = options["json_file"]
            with open(file_path, "r") as f:
                import_site_data(f, file_path)
        except Exception as e:
            self.stdout.write(e)