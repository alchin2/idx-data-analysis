from utils import get_directories, process_listings

def main():
    key = "CRMLSListing"
    raw_path, processed_path = get_directories()
    print(f"Processing raw directory: {raw_path}")
    combined, data = process_listings(raw_path, key)

    print(f"Saving combined listings to: {processed_path / 'combined_listings.csv'}")
    combined.to_csv(processed_path / "combined_listings.csv", index=False)


    print(f"Total listings processed: {data[0]}\n Residential listings saved: {data[1]}\n Approximate {data[1]/data[0]*100:.2f}% of total listings are residential.")


if __name__ == "__main__":
    main()