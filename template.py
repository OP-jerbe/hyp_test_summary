import sys
from datetime import datetime
from tkinter.filedialog import askopenfilenames

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DatetimeIndex

# Define the starting directory for finding csv files
INITIAL_DIR: str = r'\\opdata2\Company\PRODUCTION FOLDER\Production History'

# Define the source serial number and RMA number (if applicable)
SOURCE_SN: str = 'XXXLRFC'
RMA_NUMBER: str | None = None

# Define time stamps for each pass/rework of source.
# Must be of the format: 'YYYY-MM-DD hh:mm:ss'
TEST_CYCLES: list[str] = []

assert len(TEST_CYCLES) % 2 == 0

# Define the y-axis scales for certain columns to plot
ANG_INT_HIGH: int | float = 7
ANG_INT_LOW: int | float = -7
PRESSURE_HIGH: float = 1e-5
PRESSURE_LOW: float = 1e-7
TOTAL_CURRENT_HIGH: float = -5e-6
TOTAL_CURRENT_LOW: float = 0


# Function to read a CSV file and parse dates
def read_csv_with_dates(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, parse_dates=['Time'], date_format=datetime_format)


def plot_test_data(
    df: pd.DataFrame, vertical_lines: list, fig_title: str | None = None
) -> None:
    """
    Plots specific columns in separate subplots, except for 'Solenoid Current (A)' and 'Beam Voltage (kV)'
    which share the last subplot with dual y-axes.

    Parameters:
    - df: pandas DataFrame containing the data to plot.
    - vertical_lines: list of datetime objects for vertical lines.
    - fig_title: title for the figure.

    Returns:
    - None
    """

    columns_to_plot: list[str] = [
        'Angular Intensity (mA/sr)',
        'Source Pressure (mBar)',
        'Beam Supply Current (uA)',
        'Total Current (A)',
        'Solenoid Current (A)',
        'Beam Voltage (kV)',
    ]

    colors: list[str] = [
        'red',
        'blue',
        'green',
        'purple',
        'orange',
        'dodgerblue',
    ]  # Adjust as necessary

    fig, axes = plt.subplots(nrows=5, ncols=1, sharex=True, figsize=(11, 8.5))

    if fig_title:
        fig.suptitle(fig_title, fontsize=12)

    # Plot the first four columns normally
    for i, (column, color) in enumerate(
        zip(columns_to_plot[:-2], colors[:-2], strict=True)
    ):  # Skip the last two columns
        df[column].plot(ax=axes[i], color=color)
        axes[i].set_ylabel(column, fontsize=8)
        axes[i].set_xlabel('')
        axes[i].tick_params(axis='x', labelsize=8)

        # Shade alternating sections between vertical lines
        for j in range(1, len(vertical_lines), 2):
            try:
                axes[i].axvspan(
                    vertical_lines[j - 1],
                    vertical_lines[j],
                    color='lightgray',
                    alpha=0.3,
                )
            except Exception as e:
                print(
                    f'Error shading region between {vertical_lines[j - 1]} and {vertical_lines[j]}: {e}'
                )

        # Shade a section black
        # axes[i].axvspan(datetime.strptime('2024-08-05 08:13:00', '%Y-%m-%d %H:%M:%S'),
        #                 datetime.strptime('2024-08-13 13:30:00', '%Y-%m-%d %H:%M:%S'),
        #                 color='black',
        #                 alpha=1)

        # Custom behaviors
        if column == 'Angular Intensity (mA/sr)':
            axes[i].axhline(
                y=0, color='lightgray', linestyle='-', label='y = 0', linewidth=0.75
            )
            axes[i].axhline(
                y=-4, color='lightgray', linestyle='--', label='y = -4', linewidth=0.75
            )
            axes[i].set_ylim([ANG_INT_LOW, ANG_INT_HIGH])
        elif column == 'Source Pressure (mBar)':
            axes[i].set_yscale('log')
            axes[i].set_ylim([PRESSURE_LOW, PRESSURE_HIGH])
        elif column == 'Total Current (A)':
            axes[i].axhline(
                y=-1.2e-6,
                color='lightgray',
                linestyle='--',
                label='y = -1.2',
                linewidth=0.75,
            )
            axes[i].set_ylim([TOTAL_CURRENT_LOW, TOTAL_CURRENT_HIGH])

    # Combine 'Solenoid Current (A)' and 'Beam Voltage (kV)' in the last subplot
    ax1 = axes[-1]  # Primary axis for Solenoid Current
    ax2 = ax1.twinx()  # Secondary axis for Beam Voltage

    df['Solenoid Current (A)'].plot(ax=ax1, color=colors[-2])
    df['Beam Voltage (kV)'].plot(ax=ax2, color=colors[-1], linestyle='-')

    ax1.set_ylabel('Solenoid Current (A)', fontsize=8, color=colors[-2])
    ax2.set_ylabel('Beam Voltage (kV)', fontsize=8, color=colors[-1])

    ax1.tick_params(axis='x', labelsize=8)
    ax2.tick_params(axis='x', labelsize=8)

    ax1.axhline(
        y=2.5, color='moccasin', linestyle='--', label='y = 2.5', linewidth=0.75
    )
    ax1.axhline(
        y=1.2, color='moccasin', linestyle='--', label='y = 2.5', linewidth=0.75
    )
    ax2.axhline(
        y=-13, color='paleturquoise', linestyle='--', label='y = 2.5', linewidth=0.75
    )

    # Shade alternating sections between vertical lines on both axes
    for j in range(1, len(vertical_lines), 2):
        try:
            ax1.axvspan(
                vertical_lines[j - 1], vertical_lines[j], color='lightgray', alpha=0.3
            )
        except Exception as e:
            print(
                f'Error shading region between {vertical_lines[j - 1]} and {vertical_lines[j]}: {e}'
            )

    # # Shade a section black
    # ax1.axvspan(datetime.strptime('2024-08-05 08:13:00', '%Y-%m-%d %H:%M:%S'),
    #             datetime.strptime('2024-08-13 13:30:00', '%Y-%m-%d %H:%M:%S'),
    #             color='black',
    #             alpha=1)

    plt.tight_layout()
    plt.show()


# Define the datetime format
datetime_format: str = '%m/%d/%Y %I:%M:%S %p'

# Filepath to data
filepaths: tuple[str, ...] | str = askopenfilenames(
    title='Choose CSV file',
    initialdir=INITIAL_DIR,
    filetypes=(('CSV Files', '*.csv'), ('All Files', '*.*')),
)

# Read in the csv data and put them all together into one dataframe
try:
    df: pd.DataFrame = pd.concat(map(read_csv_with_dates, filepaths), ignore_index=True)
except Exception as e:
    print(f'\nError: {e}')
    print('\nCould not create dataframe.\n')
    sys.exit()

# Clean up csv data
df.set_index('Time', inplace=True)
index: DatetimeIndex = pd.to_datetime(df.index, format=datetime_format)
df.index = index
df['Beam Voltage (kV)'] = df['Beam Voltage (kV)'] * 1e-3
df['Extractor Voltage (kV)'] = df['Extractor Voltage (kV)'] * 1e-3
df.rename(
    columns={'Angular Intensity (mA/str)': 'Angular Intensity (mA/sr)'}, inplace=True
)

# Filter only for minute data
df_minutes: pd.DataFrame = df[index.second == 0]
df_minute: pd.DataFrame = df_minutes.copy()

# Convert date strings to datetime objects
vertical_lines: list[datetime] = [
    datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in TEST_CYCLES
]

# Create a mask based on the conditions (do not plot where solenoid current is less than 1 A or where angular intensity is greater than 0 i.e. plot NEG data only)
# mask = (df_minute['Solenoid Current (A)'] <= 1) | (df_minute['Angular Intensity (mA/sr)'] >= 0) | (df_minute['Beam Voltage (kV)'] > -7.8) # uncomment if you wish to only plot NEG test data

# Set all values in the filtered columns to NaN where the mask is True, keeping the indexes
# (Uncomment out one of the two following df_minute.loc lines to apply the mask)
# df_minute.loc[mask, COLUMNS_TO_PLOT] = np.nan             # apply mask to every column
# df_minute.loc[mask, [#'Angular Intensity (mA/sr)',
#                      #'Source Pressure (mBar)',
#                      ]
#                      ] = np.nan                           # apply mask to specific columns

if RMA_NUMBER:
    plot_test_data(
        df_minute, vertical_lines, fig_title=f'{SOURCE_SN} (RMA-{RMA_NUMBER})'
    )
else:
    plot_test_data(df_minute, vertical_lines, fig_title=f'{SOURCE_SN}')
