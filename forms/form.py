"""
This module provides the glossary query form
"""

import forms.form_filler as ff

from forms.form_filler import FLD_NM  # for tests

USERNAME = 'username'
PASSWORD = 'password'
GENDER = 'gender'
EMAIL = 'email'
AGE = 'age'
INTERESTS = 'interests'

REGISTRATION_FORM_FLDS = [
    {
        FLD_NM: 'Instructions',
        ff.QSTN: 'Enter your username and password.',
        ff.INSTRUCTIONS: True,
    },
   {
        ff.FLD_NM: USERNAME,
        ff.QSTN: 'User name:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        ff.FLD_NM: EMAIL,
        ff.QSTN: 'Email:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        ff.FLD_NM: PASSWORD,
        ff.QSTN: 'Password:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        ff.FLD_NM: AGE,
        ff.QSTN: 'Age:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        ff.FLD_NM: GENDER,
        ff.QSTN: 'Gender (optional):',
        ff.PARAM_TYPE: ff.QUERY_STR,  # Replace with your actual dropdown constant or logic
        ff.OPT: False,
        ff.CHOICES: ['Male', 'Female', 'Other', 'Prefer not to say'],
    },
    {
        ff.FLD_NM: INTERESTS,
        ff.QSTN: 'Interests:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
]


def get_form() -> list:
    return REGISTRATION_FORM_FLDS

def get_gender_options() -> list:
    """Retrieve the gender options for the gender field."""
    # This could also be fetched from a database or another source if needed
    return ['Male', 'Female', 'Other', 'Prefer not to say']

def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(REGISTRATION_FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(REGISTRATION_FORM_FLDS)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()