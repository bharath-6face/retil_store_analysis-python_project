import csv
import os

PRODUCT_FILE = "product.csv"
SALES_FILE = "sales_data.csv"


# ---------- CREATE SALES FILE  ----------
def create_sales_file():

    if not os.path.exists(SALES_FILE):

        with open(SALES_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "product",
                "quantity",
                "sell_price",
                "buy_price",
                "gst",
                "final_amount",
                "profit"
            ])


# ---------- LOAD PRODUCT ----------
def load_stock():

    stock = {}

    with open(PRODUCT_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            stock[row["product"]] = {

                "buy_price": float(row["buy_price"]),
                "sell_price": float(row["sell_price"]),
                "stock_qty": int(row["stock_qty"]),
                "gst": float(row["gst"])
            }

    return stock


# ---------- SAVE PRODUCT ----------
def save_stock(stock):

    with open(PRODUCT_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "product",
            "buy_price",
            "sell_price",
            "stock_qty",
            "gst"
        ])

        for name, d in stock.items():

            writer.writerow([
                name,
                d["buy_price"],
                d["sell_price"],
                d["stock_qty"],
                d["gst"]
            ])


# ---------- BILLING ----------
def billing(stock):

    grand_total = 0
    total_profit = 0

    while True:

        print("\nProducts:")

        for p in stock:
            print(p, "Stock:", stock[p]["stock_qty"])

        item = input("\nEnter product (or done): ")

        if item.lower() == "done":
            break

        if item not in stock:
            print("Invalid product")
            continue

        qty = int(input("Quantity: "))

        d = stock[item]

        if qty > d["stock_qty"]:
            print("Stock not available")
            continue

        sell = d["sell_price"]
        buy = d["buy_price"]
        gst = d["gst"]

        price = sell * qty

        gst_amount = price * gst / 100

        final = price + gst_amount

        profit = (sell - buy) * qty

        d["stock_qty"] -= qty

        grand_total += final
        total_profit += profit


        # WRITE SAFE ROW
        with open(SALES_FILE, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                item,
                qty,
                sell,
                buy,
                gst,
                round(final, 2),
                round(profit, 2)
            ])

        print("Added successfully")


    print("\nTotal Sales:", grand_total)
    print("Total Profit:", total_profit)

    save_stock(stock)


# ---------- ANALYSIS ----------
def analysis():

    total_sales = 0
    total_profit = 0

    with open(SALES_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            total_sales += float(row["final_amount"])
            total_profit += float(row["profit"])

    print("\nTotal Sales:", total_sales)
    print("Total Profit:", total_profit)


# ---------- MAIN ----------
def main():

    create_sales_file()

    stock = load_stock()

    while True:

        print("\n1 Billing")
        print("2 Analysis")
        print("3 Exit")

        ch = input("Choice: ")

        if ch == "1":
            billing(stock)

        elif ch == "2":
            analysis()

        elif ch == "3":
            break


main()