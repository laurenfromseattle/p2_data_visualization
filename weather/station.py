from datetime import datetime
import csv
import helper_functions as hf


class WeatherStation:
    def __init__(self, filename):
        self.id = None
        self.name = None
        self.location = {"longitude": None, "latitude": None, "elevation": None}
        self.dates = []
        self.temps = {"highs": [], "lows": []}
        self.prcp = []
        self.__processdata(filename)

    def __str__(self):
        return (
            f"Station id: {self.id}\n"
            f"Station name: {self.name}\n"
            f"Station location: \n"
            f" - Latitude: {self.location['latitude']}\n"
            f" - Longitude: {self.location['longitude']}\n"
            f" - Elevation: {self.location['elevation']}\n"
            f"Dates: \n"
            f" - Start Date: {self.dates[0]}\n"
            f" - End Date: {self.dates[-1]}\n"
            f" - Number of days: {len(self.dates)}\n"
            f"Precipitation ({len(self.prcp)} values): {self.prcp}\n"
            f"Temperatures: \n"
            f" - Highs ({len(self.temps['highs'])} values): {self.temps['highs']}\n"
            f" - Lows ({len(self.temps['lows'])} values): {self.temps['lows']}\n"
        )

    def __processdata(self, filename):

        try:
            with open(filename) as fhand:
                reader = csv.reader(fhand)
                headers = next(reader)

                # The types of data we would like processed.
                data_headers = ["DATE", "PRCP", "TMAX", "TMIN"]
                meta_headers = ["STATION", "NAME", "LATITUDE", "LONGITUDE", "ELEVATION"]

                # Locate the data in the file.
                data_headers_indexed = hf.get_column_indices(headers, data_headers)
                meta_headers_indexed = hf.get_column_indices(headers, meta_headers)

                # Loop through every row in the file and collect desired data.
                for row in reader:
                    # Data for row: list of tuples (data_header, value)
                    row_data = []
                    for (data_header, column_index) in data_headers_indexed:
                        # Populate row_data with data headers found in file.
                        if column_index != None:
                            if data_header == "DATE":
                                date_str = row[column_index]
                                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                                row_data.append((data_header, date))
                            if data_header == "PRCP":
                                prcp_str = row[column_index]
                                prcp = float(prcp_str) if prcp_str != "" else None
                                row_data.append((data_header, prcp))
                            if data_header in ["TMAX", "TMIN"]:
                                temp_str = row[column_index]
                                temp = int(temp_str) if temp_str != "" else None
                                row_data.append((data_header, temp))
                    # Populate class object with row_data if no data is missing.
                    # In order to sync dates across data, a date and all of its
                    # associated data is skipped if any data is missing. This way,
                    # a specific index across all data lists holds a data value
                    # collected on the same date.
                    if all(value is not None for (data_header, value) in row_data):
                        for (data_header, value) in row_data:
                            if data_header == "DATE":
                                self.dates.append(value)
                            if data_header == "PRCP":
                                self.prcp.append(value)
                            if data_header == "TMAX":
                                self.temps["highs"].append(value)
                            if data_header == "TMIN":
                                self.temps["lows"].append(value)
                    # Print what data is missing on specific dates, if any.
                    else:
                        missing_data = [
                            data_header
                            for (data_header, value) in row_data
                            if value is None
                        ]
                        for data_header in missing_data:
                            print(f"Missing {data_header} value for {date}.")

                        print(f"{date:%b %d, %Y} will be excluded from data set.\n")

                # When the loop has completed, collect desired meta data.
                meta_headers = ["STATION", "NAME", "LATITUDE", "LONGITUDE", "ELEVATION"]
                for (meta_header, column_index) in meta_headers_indexed:
                    if column_index != None:
                        if meta_header == "STATION":
                            self.id = row[column_index]
                        if meta_header == "NAME":
                            self.name = hf.format_station_name(row[column_index])
                        if meta_header == "LATITUDE":
                            self.location["latitude"] = float(row[column_index])
                        if meta_header == "LONGITUDE":
                            self.location["longitude"] = float(row[column_index])
                        if meta_header == "ELEVATION":
                            self.location["elevation"] = float(row[column_index])

        except FileNotFoundError:
            print("File cannot be found:", filename)
