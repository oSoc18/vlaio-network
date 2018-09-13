from .vat_normilze import normalize
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'vlaio_prototype.settings'
import django

# before importing any model
django.setup()
import pandas as pd
from main.models import Company

class Config:
    def __init__(self, xl_to_sql, model_class, xl_types=None, map_df_func=None):
        self.xl_to_sql = xl_to_sql
        self.xl_types = xl_types
        self.xl_cols = set(xl_to_sql.keys())
        self.model_class = model_class
        self.map_df_func=map_df_func

    def insert_models(self):
        dicts = self.df.to_dict('records')
        self.model_class.objects.bulk_create(
            [
                self.model_class(**{self.xl_to_sql[k]: d[k] for k in self.xl_cols})
                for d in dicts
            ]
        )

    def insert_from_excel(self, file_path):
        self.get_data_from_excel_file(file_path)
        self.insert_models()

    def get_data_from_excel_file(self, file_path):
        self.df = pd.read_excel(
            file_path,
            encoding='sys.getfilesystemencoding()',
            dtype=self.xl_types
        )
        present = set(self.df.columns)
        missing = self.xl_cols - present
        if missing:
            raise ValueError("Missing columns: " + ",".join(missing))
        additional = present - self.xl_cols
        for col in additional:
            del self.df[col]

        if self.map_df_func is not None:
            self.df = self.map_df_func(self.df)


def map_company_vat(df):
    VAT_COLUMN = "Ondernemingsnummer"
    df[VAT_COLUMN] = df[VAT_COLUMN].apply(normalize)
    return df


COMPANY_CONFIG = Config(
    xl_to_sql={
        # In file name: db column name
        "Naam": "name",
        "Ondernemingsnummer": "vat",
        "Gemiddeld aantal werknemers\n2016": "employees",
        "Winst (Verlies) van het boekjaar na belasting (+/-)\nEUR\n2016": "profit"
    },
    xl_types={
        "Naam": str,
        "Ondernemingsnummer": str,
        "Gemiddeld aantal werknemers\n2016": int,
        "Winst (Verlies) van het boekjaar na belasting (+/-)\nEUR\n2016": int
    },
    model_class=Company,
    map_df_func=map_company_vat
)
