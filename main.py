from agents.charleston_agent import run_charleston_agent
from agents.berkeley_agent import run_berkeley_agent
import pandas as pd
import os

def load_tms_table():
    return pd.read_csv("data/tms_table.csv")

def process_all():
    tms_data = load_tms_table()

    print("Starting Charleston County processing...")
    for tms in tms_data['Charleston County'].dropna():
        try:
            print(f"Processing TMS: {tms}")
            run_charleston_agent(str(tms).strip())
        except Exception as e:
            print(f"Charleston error with TMS {tms}: {e}")

    print("\nStarting Berkeley County processing...")
    for tms in tms_data['Berkeley County'].dropna():
        try:
            print(f"Processing TMS: {tms}")
            run_berkeley_agent(str(tms).strip())
        except Exception as e:
            print(f"Berkeley error with TMS {tms}: {e}")

if __name__ == "__main__":
    process_all()
