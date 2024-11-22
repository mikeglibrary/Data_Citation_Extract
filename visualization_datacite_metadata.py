#Simple script to show how many of the scanned PDF articles cite the same identified DataCite data set doi


import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('output.csv')

# Count the number of citations that each dataset has in the output file
citation_counts = df.groupby('Title')['Title of Citing Local PDF'].count().sort_values(ascending=False)

# Create a bar plat
plt.figure(figsize=(12, 6))
citation_counts.plot(kind='bar')
plt.title('Number of Citations per Dataset')
plt.xlabel('Dataset Title')
plt.ylabel('Number of Citations')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Draw the plat
plt.show()

# Print the citation counts
print(citation_counts)