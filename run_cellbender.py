#!/usr/bin/python
# run this in cellbender environment
import os
import shutil
import subprocess
import argparse

# Loop through each version and perform the copying, renaming, and running CellBender
def run_cellbender(base_path, samples, output_path):
    for sample in samples:
        raw_path = os.path.join(base_path, sample, 'Solo.out', 'Velocyto', 'raw')
        
        # Define the paths for the new spliced and unspliced directories
        spliced_path = os.path.join(raw_path, 'spliced')
        
        # Create the spliced and unspliced directories if they don't exist
        os.makedirs(spliced_path, exist_ok=True)
        
        # Define the source files
        spliced_src = os.path.join(raw_path, 'spliced.mtx')
        barcodes_src = os.path.join(raw_path, 'barcodes.tsv')
        features_src = os.path.join(raw_path, 'features.tsv')
        
        # Define the destination files
        spliced_dst = os.path.join(spliced_path, 'matrix.mtx')
        barcodes_dst_spliced = os.path.join(spliced_path, 'barcodes.tsv')
        features_dst_spliced = os.path.join(spliced_path, 'genes.tsv')
        
        # Copy and rename the files
        shutil.copyfile(spliced_src, spliced_dst)
        shutil.copyfile(barcodes_src, barcodes_dst_spliced)
        shutil.copyfile(features_src, features_dst_spliced)

        # Define the output paths for CellBender
        spliced_output = os.path.join(output_path, sample, 'spliced_filt', 'output.lh5')
        
        # Create output directories if they don't exist
        os.makedirs(os.path.dirname(spliced_output), exist_ok=True)

        # Run CellBender on spliced matrix
        subprocess.run([
            'cellbender', 'remove-background',
            '--input', spliced_path,
            '--output', spliced_output,
            '--debug',
            '--cuda'  # Use GPU if available
        ])

    print("All versions processed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CellBender")
    parser.add_argument("base_path", help="Path to the input .mtx file")
    parser.add_argument("--samples", nargs='+', help="List of sample names")
    parser.add_argument("--samples_file", help="Path to a file containing sample names, one per line")
    parser.add_argument("output_path", help="Path to output .h5 file")
    args = parser.parse_args()
    
    if args.samples_file:
        with open(args.samples_file, 'r') as f:
            samples = [line.strip() for line in f]
    elif args.samples:
        samples = args.samples
    else:
        parser.error("Either --samples or --samples_file must be provided")
    
    run_cellbender(args.base_path, samples, args.output_path)