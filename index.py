import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console

console = Console()

plt.close("all")

def getLatencyCol(dataframe):
    """
    Returns the name of the column that has "latency" in it.

    :param dataframe: data where the latency column resides
    :return: returns column title that contains "latency"
    """
    for col in df.columns.values.tolist():
        if "latency" in col.lower():
            latency_col_title = col

    if not latency_col_title:
        console.print("""
    [yellow]WARNING:[/yellow] Latency not found in any column.
        """)
        return ""
    else:
        return latency_col_title

raw_df = pd.read_csv('base_case_multicast/run_1/vm1_output/pub_output.csv')
row_count = len(raw_df)

# Skip first 4 rows
df = pd.read_csv('base_case_multicast/run_1/vm1_output/pub_output.csv', skiprows=4)

# Choose which rows and columns to include:
# [row_start:row_end, col_start: col_end]
df = df.iloc[0:(row_count - 6), 0:6]

latency_col_title = getLatencyCol(df)

latencies = df[latency_col_title]
latencies = latencies.astype(float)

latencies.plot(y="Latencies")
plt.savefig('file.pdf')

# console.print(latencies[0:10].to_string())

# data = [6.1,5.8,5.7,5.7,5.8,5.6,5.5,5.3,5.2,5.2]
  
# df = pd.DataFrame(data)
# df.plot()
# plt.show()