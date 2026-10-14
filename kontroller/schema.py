import pandas as pd
import pandera.pandas as pa 
import sys
import argparse

schema = pa.DataFrameSchema(
    {
        "kund_id":pa.Column(
            int,
            unique=True,
            nullable=False,
        ),
        "alder":pa.Column(
            int,
            checks=pa.Check.in_range(18,120),
            nullable=False,
        ),
        "region": pa.Column(
            str,
            checks=pa.Check.isin(
                ["Stockholm", "Väst", "Mitt", "Syd", "Norr"]
                # the controll don't handel vast and väst 
            ),
            nullable=False
        ),
        "abonnemang":pa.Column(
            str,
            checks=pa.Check.isin([
                "Bas", "Standard", "Premium"
            ]),
            nullable=False,
        ),
        "manader_som_kund":pa.Column(
            int,
            checks=pa.Check.greater_than_or_equal_to(0),
            nullable=False,
        ),
        "manadskostnad": pa.Column(
            float,
            checks=pa.Check.greater_than_or_equal_to(0),
            nullable=False,
        ),
        "data_gb_per_manad":pa.Column(
            float,
            checks=pa.Check.greater_than_or_equal_to(0),
            # zero is accepted
            nullable=False,
        ),
        "supportarenden_12m": pa.Column(
            int,
            checks=pa.Check.greater_than_or_equal_to(0),
            nullable=False,
        ),
        "avslutat": pa.Column(
            int,
            checks=pa.Check.isin([0,1]),
            nullable=False,
        ),
    }
)
parser = argparse.ArgumentParser(
    description="Validate customer data with Pandera"
)
parser.add_argument(
    "data_file",
    help="Path to the cvs file that has to be validate",
)
args = parser.parse_args()
df = pd.read_csv(args.data_file)


try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as error:
    print("Data validation failed:")
    print(error.failure_cases.to_string(index=False))
    sys.exit(1)

print("Data validation passed.")

# for check the exit code in the terminal 
# python kontroller/schema.py data/kundbas_ny_leverans.csv
# then 
# echo $? 
# should give 1 because the program has terminate with a faild 
# is the except in the try/exept block.

