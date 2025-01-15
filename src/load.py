import csv

def load_data(products_list: list):
    """
    Saves the given list of product dictionaries to a csv file.
    The file is opened in append mode, and the header is written if the file is empty.
    This allows the same function to be used for both initial and subsequent writes.
    """
    
    with open("../data.csv", "a+", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=products_list[0].keys())
        file.seek(0,0)
        if not file.read(1):
            writer.writeheader()

        writer.writerows(products_list)