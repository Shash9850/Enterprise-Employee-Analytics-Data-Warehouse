import pandas as pd


file_path = "data/generated/employee_history.csv"

history = pd.read_csv(file_path)

print("Shape:", history.shape)

print("\nColumns:")
print(history.columns.tolist())

print("\nFirst 10 rows:")
print(history.head(10).to_string(index=False))

print("\nChange type distribution:")
print(history["change_type"].value_counts())

print("\nCurrent flag distribution:")
print(history["is_current"].value_counts())

print("\nEmployees with multiple history records:")
record_counts = history["employee_id"].value_counts()
print(record_counts[record_counts > 1].head(10))