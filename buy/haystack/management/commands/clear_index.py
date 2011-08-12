from optparse import make_option
import sys
from django.core.management.base import BaseCommand
from haystack.management.commands.update_index import get_site


class Command(BaseCommand):
    help = "Clears out the search index completely."
    base_options = (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='If provided, no prompts will be issued to the user and the data will be wiped out.'
        ),
        make_option('-s', '--site', action='store', dest='site',
            type='string', help='The site object to use when reindexing (like `search_sites.mysite`).'
        ),
    )
    option_list = BaseCommand.option_list + base_options
    
    def handle(self, **options):
        """Clears out the search index completely."""
        # Cause the default site to load.
        site = get_site(options.get('site'))
        self.verbosity = int(options.get('verbosity', 1))
        
        if options.get('interactive', True):
            print
            print "WARNING: This will irreparably remove EVERYTHING from your search index."
            print "Your choices after this are to restore from backups or rebuild via the `rebuild_index` command."
            
            yes_or_no = raw_input("Are you sure you wish to continue? [y/N] ")
            print
            
            if not yes_or_no.lower().startswith('y'):
                print "No action taken."
                sys.exit()
        
        if self.verbosity >= 1:
            print "Removing all documents from your index because you said so."
        
        from haystack import backend
        sb = backend.SearchBackend(site=site)
        sb.clear()
        
        if self.verbosity >= 1:
            print "All documents removed."
