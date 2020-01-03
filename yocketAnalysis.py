# Part 1

import json
from pandas.io.json import json_normalize
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Read json containing data
with open("details7.json", "r", encoding="utf-8") as read_file:
    fileData = json.load(read_file)

# Normalized the data to show in a proper tabular view
dataNorm = json_normalize(fileData)
# print(dataNorm)

# Converting to a dataframe
finalData = pd.DataFrame(dataNorm)

# Analysing the shape of the dataframe
print(finalData.head())

# Information of the Dataframe,
# Checking if any null values
# print(data.info())

# Part 2

# Change Dataframe Column Name

data = finalData.rename(columns={'greOrGmatScore.gregmat': 'greGmat', 'greOrGmatScore.score': 'greGmatScore',
                                 'toeflIeltsScore.toelfIelts': 'toelfIelts', 'toeflIeltsScore.score': 'toeflIeltsScore',
                                 'workExperience.workExperience': 'workExperience',
                                 'workExperience.score': 'workExperienceNumber'})

# See the changes
print(data.head())
