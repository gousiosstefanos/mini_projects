import collections
import json
import locale
import reports
import sys
import emails


def load_data(filename):
  # Loads the contents of filename as a JSON file.
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  # Given a car dictionary, returns a nicely formatted name.
  return f"{car['car_make']} {car['car_model']} ({car['car_year']})"


def process_data(data):
  # Analyzes the data, looking for maximums.
  # Returns a list of lines that summarize the information.

  max_sales = {"total_sales": 0}
  max_revenue = {"revenue": 0}
  # A dictionary with automatic default value 0
  car_year_sales = collections.defaultdict(int)

  for item in data:
    # Converts "$1234.56" → 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price

    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item

    if item["total_sales"] > max_sales["total_sales"]:
      max_sales = item

    car_year_sales[item["car"]["car_year"]] += item["total_sales"]

  max_car_sales_year = (0, 0)

  for year, sales in car_year_sales.items():
    if sales > max_car_sales_year[1]:
      max_car_sales_year = (year, sales)

  summary = []

  summary.append(
    f"The {format_car(max_revenue['car'])} generated the most revenue: ${max_revenue['revenue']}"
  )

  summary.append(
    f"The {format_car(max_sales['car'])} had the most sales: {max_sales['total_sales']}"
  )

  summary.append(
    f"The most popular year was {max_car_sales_year[0]} with {max_car_sales_year[1]} sales."
  )

  return summary


def cars_dict_to_table(car_data):
  # Turns the data in car_data into a list of lists.

  table_data = [["ID", "Car", "Price", "Total Sales"]]

  """ An example:
  [
  ["ID", "Car", "Price", "Total Sales"],

  [47, "Lamborghini Murciélago (2002)", "$13724.05", 149],
  [12, "Toyota Corolla (2018)", "$18000.00", 320],
  [88, "Honda Civic (2020)", "$21000.00", 275],
  ]"""

  for item in car_data:
    table_data.append([
      item["id"],
      format_car(item["car"]),
      item["price"],
      item["total_sales"]
    ])

  return table_data


def main(argv):
  data = load_data("car_sales.json")
  summary = process_data(data)

  # Create paragraph for PDF
  paragraph = "<br/>".join(summary)

  # Create table for PDF
  table_data = cars_dict_to_table(data)

  # Generate PDF report
  title = "Sales summary for last month"
  attachment = "/tmp/cars.pdf"
  reports.generate(attachment, title, paragraph, table_data)

  # Send email
  sender = "<sender>@example.com"
  receiver = "<user>@example.com"
  body = "\n".join(summary)

  message = emails.generate(sender, receiver, title, body, attachment)
  emails.send(message)


if __name__ == "__main__":
  main(sys.argv)