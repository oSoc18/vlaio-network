from .vat_normilze import normalize

import pandas as pd

file_path = "D:\\Downloads\\wetransfer-470901\\belfirst2.xlsx"


XL_TO_SQL = {
    # In file name: db column name
    "Naam": "name",
    "Ondernemingsnummer": "vat",
    "Gemiddeld aantal werknemers\n2016": "employees",
    "Winst (Verlies) van het boekjaar na belasting (+/-)\nEUR\n2016": "profit"
}

XL_TYPES = {
    "Naam": str,
    "Ondernemingsnummer": str,
    "Gemiddeld aantal werknemers\n2016": int,
    "Winst (Verlies) van het boekjaar na belasting (+/-)\nEUR\n2016": int
}

XL = set(XL_TO_SQL.keys())
VAT_COLUMN = "Ondernemingsnummer"


def get_companies_dataframe(file_path):
    df = get_dataframe(file_path, XL, dtypes=XL_TYPES)
    df[VAT_COLUMN] = df[VAT_COLUMN].apply(normalize)
    return df


def get_dataframe(file_path, xls_cols, dtypes):
    """
    :param file_path: set of columns names
    :param xls_cols:
    :return:
    """
    df = pd.read_excel(file_path, encoding='sys.getfilesystemencoding()', dtype=dtypes)
    present = set(df.columns)
    missing = xls_cols - present
    if missing:
        raise ValueError("Missing columns: " + ",".join(missing))
    additional = present - xls_cols
    for col in additional:
        del df[col]

    return df


def get_companies(df):
    from main.models import Company
    dicts = df.to_dict('records')
    return [
        Company(**{XL_TO_SQL[k]: d[k] for k in XL})
        for d in dicts
    ]


def insert_companies_from_file(file_path):
    from main.models import Company
    df = get_companies_dataframe(file_path)
    Company.objects.bulk_create(get_companies(df))
