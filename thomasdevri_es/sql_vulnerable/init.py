"""
Perform migrations and insert hidden data into database.

Tests always run migrations, and the code is pretty straightforward,
so there is not test coverage.
"""
import os
import sys

if __name__ == '__main__':
    # configure django
    from django import setup as django_setup

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(BASE_DIR)
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'thomasdevri_es.settings'
    )
    django_setup()

# pylint: disable=wrong-import-position
from django.db import connection
from django.contrib.auth.models import User

def init_data(*a, **kw):
    """
    Create mock data in ssh_passwords table for thomas to discover. Accepts
    and ignores arguments passed in by django.
    """
    with connection.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS staff_site_passwords')
        cursor.execute("""
            CREATE TABLE staff_site_passwords (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                plaintextpass TEXT NOT NULL,
                isactive SMALLINT NOT NULL
            )
        """)

        silly_users = [
            ('mary_c_ristmus', 'ToMaS'),
            (
                'this_website_has_better_test_coverage_than_cyberpunk_2077',
                'itstrue'
            ),
            ('potayto', 'potatoee'),
            ('tomayto', 'tomatowe'),
            ('chris', 'iamchris1988'),
            ('jtddv', 'we_will_never_know'),
            (
                'cjdv101',
                'dad_please_make_your_password_longer_than_6_characters'
            ),
            (
                'keight',
                'what_the_fuck_did_you_just_say_about_me_you_Little_Bitch'
            ),
            ('BabyYoda', 'ThisIsTheWay'),
            ('santa','ho_ho_ho_69'),
            ('jayjay', 'okay_boomer'),
        ]
        for usr, passwd in silly_users:
            cursor.execute(
                "INSERT INTO staff_site_passwords (user, plaintextpass, isactive) "
                f"VALUES ('{usr}', '{passwd}', 0)"
            )
        cursor.execute(
            "INSERT INTO staff_site_passwords (user, plaintextpass, isactive) VALUES "
            "('thomasdev', 'i_am_an_insecure_chungus', 1)"
        )
        User.objects.create_user(
            username='thomasdev',
            password='i_am_an_insecure_chungus',
            is_staff=True
        )


def reverse_init_data(*a, **kw):
    """
    Exists as a django migration hook.
    """
    with connection.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS staff_site_passwords')


if __name__ == '__main__':
    init_data()
