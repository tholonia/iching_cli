#!/bin/env python
# Import the barcode package with explicit path to avoid name conflict
import sys
sys.path.insert(0, './packages')
import barcode
from barcode.writer import ImageWriter  # Updated import path

# Define the ISBN number
isbn_number = "9798313459127"

# Generate the barcode
isbn = barcode.get_barcode_class("isbn13")
isbn_barcode = isbn(isbn_number, writer=ImageWriter())

# Save the barcode image
barcode_path = "isbn_barcode.png"
isbn_barcode.save(barcode_path)

print(f"Barcode saved as {barcode_path}")
