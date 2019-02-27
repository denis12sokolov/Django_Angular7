from django.core.management.base import BaseCommand

from core.parser.run import parse_all


class Command(BaseCommand):
    help = 'Run parser for all sites in DB'

    def add_arguments(self, parser):
        parser.add_argument('shops', nargs='*', type=str, default=None)

    def handle(self, *args, **options):
        shops = options.get("shops")
        if shops:
            parse_all(shops)
        else:
            parse_all()
