import sys

VALID_ITEM_DATA = [{'name': 'minimal', 'order': 0, 'done': False},
                   {'name': 'has_start_date', 'order': 1, 'done': False,
                       'start_date': 'Sun, 06 Nov 1994 08:49:37 -0000'},
                   {'name': 'has_description', 'order': 4, 'done': False,
                       'description': 'Lorem ipsum dolor sit amet.'},
                   {'name': 'already_done', 'order': 8, 'done': True}]

ADDITIONAL_VALID_ITEM_DATA = [{'name': 'a',
                               'order': 57,
                               'done': True},
                              {'name': 'a',
                               'order': 1,
                               'done': False,
                               'description': 'Lorem ipsum dolor sit amet',
                               'start_date': 'Sun, 05 Apr 2020 19:22:13 -0000',
                               'due_date': 'Mon, 09 Nov 1981 19:22:13 -0000',
                               'end_date': 'Sun, 08 Jun 1956 19:22:13 -0000'}]

INVALID_ITEM_DATA = [{'name': 'name too long '*100,
                      'order': 57,
                      'done': True},
                     {'name': 'no order number',
                      'done': False},
                     {'name': 'unstandardized date format',
                      'order': 12,
                      'done': False,
                      'start_date': 'January 21, 2012'},
                     {'name': 'extraneous fields',
                      'order': 12,
                      'done': False,
                      'spatula': 'albuquerque'},
                     {}  # Empty JSON
                     ]

VALID_OVERWRITE_DATA = [{'name': 'name change only'},
                        {'name': 'name and doneness', 'done': True},
                        {'name': 'update that could overwrite a field',
                         'description': None},
                        {'name': 'name and date',
                         'start_date': 'Tue, 08 Nov 1994 08:49:37 -0000'},
                        {'order': 12}]

INVALID_OVERWRITE_DATA = [{'name': None},  # Remove a required field
                          {'name': 'name too long '*100},
                          {'id': None},
                          {'start_date': 'January 21, 2012'},
                          {'id': 37},  # Primary key should be immutable,
                                       # since we use it as a foreign key
                          {},
                          {'done': 'asdf'}]  # Wrong type: string in a boolean field

VALID_USER_DATA = [
        {'username': 'leahvelleman',
         'email': 'leahvelleman@gmail.com',
         'password': 'zooblefart'},
        {'username': 'accéntedchãraçtérs',
         'email': 'fancyletters@foo.com',
         'password': '2r039fjaio'},
        {'username': 'someoneelse',
         'email': 'someone.else@gmail.com',
         'password': 'squeedleblorf'},
        {'username': 'FredNull',
         'email': 'fnull@example.com',
         'password': 'wo239u3hofwasf'},
        {'username': '도윤김',
         'email': 'doyeonkim@gmail.com',
         'password': '2398rhfeoriaselfjwe'},
        {'username': 'ExtendedUnicodePassword',
         'email': 'somuchunicode@gmail.com',
         'password': '表ポあA鷗ŒéＢ逍Üßªąñ丂㐀𠀀'},
        {'username': 'OkayEmail',
         'email': 'name@domain.thisisnotactuallyaTLD',
         'password': 'squeedleblorf'},
        {'username': 'OkayEmail2',
         'email': '도윤@whatever.net',
         'password': 'squeedleblorf'},
         ]

INVALID_USER_DATA = [
        {'username': '',
         'email': 'no.username@gmail.com',
         'password': 'zooblefart'},
        {'username': '💕 💞 💓 💗 💖',
         'email': 'shmoopybutt@gmail.com',
         'password': '28hfiaslawe'},
        {'username': 'No Email',
         'email': None,
         'password': 'squeedleblorf'},
        {'username': 123,
         'email': 'username.is.the.wrong.type@hotmail.com',
         'password': '2aeaica'},
        {'username': 'Bademail1',
         'email': 'foo',
         'password': 'squeedleblorf'},
        {'username': 'Bademail2',
         'email': 'too..many..periods@gmail.com',
         'password': 'squeedleblorf'},
        {'username': 'Bademail3',
         'email': '(really)badspecialcharacters@gmail.com',
         'password': 'squeedleblorf'},
        {'username': 'Extrafields',
         'email': 'foo@foo.com',
         'useless': 'this is bad',
         'password': 'squeedleblorf'},
         ]

INVALID_ID_NUMBERS = [sys.maxsize, "0.5", "-1", "1&garbage", "", "spork"]
