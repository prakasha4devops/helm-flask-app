from datetime import datetime, timedelta

# Get the current date and time
current_datetime = datetime.now()

# Define the amount to add
one_year = timedelta(days=365)  # Adding 365 days for a year
four_hours = timedelta(hours=4)

# Calculate the new date and time
new_datetime = current_datetime + one_year + four_hours

# Print the result
print("Current Date and Time:", current_datetime)
print("New Date and Time:", new_datetime)
