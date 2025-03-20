# Defensive-Model

## 1. NFL Big Data Bowl 2025 Data Processing

This part is designed to process the NFL Big Data Bowl 2025 dataset. The related directory structure and file path conventions are as follows:

```sql
root/
├── data/ Contains raw CSV files (Raw Data)
│   └── games.csv    <-- game data
│   └── player_plays.csv   <-- player data for each play
│   └── plays.csv <-- play data
├── src/                  <-- Contains src files
└── README.md                      <-- Project README file
```

### Data Storage

All raw data files (CSV format) should be placed in the data/nfl-big-data-bowl-2025 folder.
The code uses relative paths to access files from this folder.

### Data processing

Data processing scripts are located in the process_data folder.
These scripts will read the raw data from data/nfl-big-data-bowl-2025, perform cleaning, transformation, and analysis.
Processed data outputs are saved in the data folder for subsequent use.

### Usage Instructions

Ensure that Python 3 is installed along with the required libraries (e.g., pandas).
In the scripts within the process_data folder, you can load the data using relative paths. For example:

```python
import pandas as pd
# Load a raw data CSV file from the data/nfl-big-data-bowl-2025 folder
df = pd.read_csv('../data/nfl-big-data-bowl-2025/games.csv')
```

After processing, the scripts save the output files to the data folder.
