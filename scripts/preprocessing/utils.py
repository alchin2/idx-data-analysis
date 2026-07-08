import pandas as pd
import pathlib
from time import sleep
from tqdm import tqdm, trange
import warnings
warnings.filterwarnings('ignore')


def get_directories(): 
    """
    Retrieving the raw and processed data directories.
    """
    base_dir = pathlib.Path(__file__).parent.parent.parent
    raw_path = base_dir / "data" / "raw" 
    processed_path = base_dir / "data" / "processed" 


    return raw_path, processed_path

def process_listings(dir, key):
    """
    Filtering for residential properties and combining them into a single DataFrame.

    Input: directory path and key to filter file names.
    Output: Combined DF and tuple of (total listings, residential listings).

    """

    amt = 0
    combined = pd.DataFrame()
    
    # validate file
    files = list(dir.glob("*.csv"))
    matching_files = [f for f in files if key in f.name]
    
    for file in tqdm(matching_files, desc=f"Processing {key} files", unit="file", ncols=80, ascii=False):
    
        df = pd.read_csv(file, low_memory=False)
        amt += df.shape[0]

        # Filter for residential properties
        df = df[df["PropertyType"].isin(["Residential"])]

        # Sort by closed date
        df = df.sort_values(by="ListingContractDate", ascending=True)


        combined = pd.concat([combined, df[df["PropertyType"] == "Residential"]], ignore_index=True)

    return combined, (amt, combined.shape[0])







