from pathlib import Path

def save_csv_data(data: str, output_path: Path):
    """Saves the raw text data to the output file."""
    # Create the output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"\n✅ Success! Data saved to {output_path}")
    except IOError as e:
        print(f"\n❌ Error: Could not write file to {output_path}. Reason: {e}")