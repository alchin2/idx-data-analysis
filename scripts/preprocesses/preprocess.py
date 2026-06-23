from utils import get_directories, process_listings

def process_listings_data():
    """Process listing data from raw directory."""
    key = "CRMLSListing"
    raw_path, processed_path = get_directories()


    print(f"Processing listings from raw directory: {raw_path}")
    combined, data = process_listings(raw_path, key)
    combined.to_csv(processed_path / "combined_listings.csv", index=False)
    print("=" * 60)
    print(f"Total listings processed: {data[0]}\nResidential listings saved: {data[1]}\nApproximate {data[1]/data[0]*100:.2f}% of total listings are residential.")
    print("=" * 60)

def process_sold_data():
    """Process sold data from raw directory."""
    key = "CRMLSSold"
    raw_path, processed_path = get_directories()


    print(f"Processing sold data from raw directory: {raw_path}")
    combined, data = process_listings(raw_path, key)
    combined.to_csv(processed_path / "combined_sold.csv", index=False)
    print("\n")
    print("=" * 60)
    print(f"Total sold properties processed: {data[0]}\nResidential properties saved: {data[1]}\nApproximate {data[1]/data[0]*100:.2f}% of total sold properties are residential.")
    print("=" * 60)

def main():
    print("=" * 60)
    print("Preprocessing CRML Data")
    print("=" * 60)
    
    print("\n--- Processing Listings ---\n")
    process_listings_data()
    
    print("\n--- Processing Sold Data ---\n")
    process_sold_data()
    


if __name__ == "__main__":
    main()

# Listing: 838693 -> 533052
# Sold: 681599 -> 458336
# Total: 1,520,292 -> 991,388 (residential properties only)