import pandas as pd
import argparse
from typing import Iterator
from constants.energy_constants import TIMESTAMP, INITIALMW, TARGETMW, RRP


class EnergyRevenueCalc:
    """
        A class to calculate energy revenue from battery dispatch data.

        This calculator processes large CSV files in chunks to manage memory usage
        efficiently while calculating the net energy revenue for a specified date.

        Attributes:
            file_path (str): Path to the CSV file containing battery dispatch data.
            date (datetime.date): The date for which to calculate revenue.
            total_revenue (float): The accumulated total revenue.
    """

    def __init__(self, file_path, date, chunk_size):
        self.file_path = file_path
        self.date = pd.to_datetime(date, format='%Y-%m-%d').date()
        self.chunk_size = chunk_size
        self.total_revenue = 0

    def process_chunks(self) -> Iterator[pd.DataFrame]:
        """
        Process the input CSV file in chunks. This method reads the CSV file in chunks, converts the timestamp column
        to datetime, and filters each chunk for the specified date.

        :returns: A chunk of the CSV file, filtered for the specified date.
        """
        previous_last_row = None
        for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size,
                                 usecols=[TIMESTAMP, INITIALMW, TARGETMW, RRP]):
            chunk[TIMESTAMP] = pd.to_datetime(chunk[TIMESTAMP], format='%d/%m/%Y %H:%M')
            filtered_chunk = chunk[chunk[TIMESTAMP].dt.date == self.date]
            if not filtered_chunk.empty:
                if previous_last_row is not None:
                    filtered_chunk = pd.concat([previous_last_row.to_frame().T, filtered_chunk])
                yield filtered_chunk
                previous_last_row = filtered_chunk.iloc[-1]

    @staticmethod
    def calculate_interval_revenue(initial_mw: float, target_mw: float, rrp: float) -> float:
        """
        Calculate the revenue for a given interval.

        :param initial_mw: power output of the battery unit measured at the beginning of the period
        :param target_mw: (the dispatch MW expected at the end of the interval
        :param rrp: energy price
        """
        energy_dispatched = (initial_mw + target_mw) / 2 * (5 / 60)
        return energy_dispatched * rrp

    def process_interval(self, current: pd.Series, next_: pd.Series) -> float:
        """
        Process a single interval and return its revenue.

        :returns: The calculated revenue for the interval.
        """
        end_mw = next_[INITIALMW] if next_ is not None else current[TARGETMW]
        return self.calculate_interval_revenue(current[INITIALMW], end_mw, current[RRP])

    def process_chunk(self, chunk: pd.DataFrame) -> None:
        """
        Process a single chunk of data.
        :param chunk: A chunk of data to process.
        """
        for i in range(len(chunk) - 1):  # Note the -1 here
            current_interval = chunk.iloc[i]
            next_interval = chunk.iloc[i + 1]
            interval_revenue = self.process_interval(current_interval, next_interval)
            self.total_revenue += interval_revenue

    def calculate_total_revenue(self) -> float:
        """
        This method processes all chunks of the input file, accumulates the revenue
        for each interval, and returns the total revenue for the specified date.
        :returns float: The total calculated revenue.
        """
        for chunk in self.process_chunks():
            self.process_chunk(chunk)
        return self.total_revenue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate energy revenue from battery dispatch data.")
    parser.add_argument("--file_path", help="Path to the CSV file containing battery dispatch data",
                        default="./coding_practice_python_battery_dispatch_dataset.csv")
    parser.add_argument("--date", default="2024-04-01",
                        help="Date of interest in YYYY-MM-DD format (default: 2024-04-01)")
    parser.add_argument("--chunk", default=100, help="Number of records to process in batches.")

    args = parser.parse_args()

    calculator = EnergyRevenueCalc(args.file_path, args.date, int(args.chunk))
    total_revenue = calculator.calculate_total_revenue()
    print(f"Net energy revenue for {args.date}: ${total_revenue:.2f}")
