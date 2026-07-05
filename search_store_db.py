import pandas as pd

store_location_file = pd.read_csv("ignored files/home_depot_us_locations_sorted.csv")

def getStoreAddress(store_number):
    
    store_number = int(store_number)
    row = store_location_file.loc[store_location_file["store_number"] == store_number].iloc[0]
    
    if row["address_present"] == "yes":
        full_address = row["full_address"]    
    else:
        full_address = "Address unavailable in database"
    
    
    return full_address

    
    

if __name__ == "__main__":
    print("Enter store number\n")
    user_store_number = input()
    print(getStoreAddress(user_store_number))