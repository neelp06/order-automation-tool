# Order Automation Tool

A Python desktop application that automates order management for a warehouse.

## What it does
- Validates order data from CSV files
- Flags duplicates and missing information
- Auto-generates PDF job cards for valid orders
- Stores order history in a SQLite database
- Produces a color coded Excel summary report
- Simple GUI — no coding knowledge required to use

## Tech Stack
Python, pandas, SQLite, ReportLab, openpyxl, tkinter

## How to Run
pip install pandas reportlab openpyxl
python src/gui.py