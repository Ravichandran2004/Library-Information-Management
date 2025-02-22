import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from collections import defaultdict
from lims_app.models import BorrowRecord

def remove_duplicates():
    records = BorrowRecord.objects.values('user_id', 'book_id', 'is_returned', 'id')
    grouped_records = defaultdict(list)

    for record in records:
        key = (record['user_id'], record['book_id'], 'is_returned')
        grouped_records[key].append(record['id'])

    duplicate_ids = [ids[1:] for ids in grouped_records.values() if len(ids) > 1]
    flat_duplicate_ids = [item for sublist in duplicate_ids for item in sublist]

    if flat_duplicate_ids:
        BorrowRecord.objects.filter(id__in=flat_duplicate_ids).delete()
        print(f'Successfully deleted {len(flat_duplicate_ids)} duplicate BorrowRecord(s).')
    else:
        print('No duplicate BorrowRecord entries found.')

if __name__ == '__main__':
    remove_duplicates()


# from collections import defaultdict
# from django.core.management.base import BaseCommand
# from lims_app.models import BorrowRecord

# class Command(BaseCommand):
#     help = 'Remove duplicate BorrowRecord entries from the database.'

#     def handle(self, *args, **kwargs):
#         records = BorrowRecord.objects.values('user_id', 'book_id', 'is_returned', 'id')
#         grouped_records = defaultdict(list)

#         for record in records:
#             key = (record['user_id'], record['book_id'], record['is_returned'])
#             grouped_records[key].append(record['id'])

#         duplicate_ids = [ids[1:] for ids in grouped_records.values() if len(ids) > 1]
#         flat_duplicate_ids = [item for sublist in duplicate_ids for item in sublist]

#         if flat_duplicate_ids:
#             self.stdout.write(self.style.WARNING(f'Found {len(flat_duplicate_ids)} duplicate BorrowRecord(s).'))
#             for record_id in flat_duplicate_ids:
#                 self.stdout.write(f'Duplicate Record ID: {record_id}')
#             # Uncomment the line below to delete duplicates after verification
#             # BorrowRecord.objects.filter(id__in=flat_duplicate_ids).delete()
#             self.stdout.write(self.style.SUCCESS('Duplicate BorrowRecords identified.'))
#         else:
#             self.stdout.write('No duplicate BorrowRecord entries found.')
