import pandas as pd
from tabulate import tabulate

def print_dataframe(df: pd.DataFrame, title: str = None, headers: str = 'keys', tablefmt: str = 'psql') -> None:
    """
    Prints a DataFrame in a formatted table style.
    
    Args:
        df (pd.DataFrame): The DataFrame to print.
        title (str, optional): A title to print before the table.
        headers (str, optional): Header format for tabulate. Defaults to 'keys'.
        tablefmt (str, optional): Table format for tabulate. Defaults to 'psql'.
    """
    if title:
        print(f"\n{title}")
        print("-" * len(title))

    if df.empty:
        print("Empty DataFrame")
        return

    print(tabulate(df, headers=headers, tablefmt=tablefmt, showindex=False))
    print("\n")
