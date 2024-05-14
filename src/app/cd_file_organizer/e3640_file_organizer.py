import os
import sys

from pathlib import Path

from cd_sem_file_organizer import CdSemFileCollector
from cd_sem_file_organizer import CdSemFileDeleter


if __name__ == '__main__':
    try:
        p = Path('e3640_file_copy.ini')
        t = CdSemFileCollector(p)
        t.handle()
    except FileNotFoundError:
        print('File Copy: File Not Found')

    try:
        p = Path('e3640_file_delete.ini')
        t = CdSemFileDeleter(p)
        t.handle()
    except FileNotFoundError:
        print('File Delete: File Not Found')

    # try:
    #     p = Path('e3640_desk_delete.ini')
    #     t = CdSemFileDeleter(p)
    #     t.handle()
    # except FileNotFoundError:
    #     print('Disk Delete: File Not Found')
    print('tetest')

