"""Revenue driver tree and month-to-month bridge for the retail sales data.

Revenue = Orders x Units per order x Avg price per unit x Net rate (1 - discount)

Usage:
    python driver_tree.py Revenue_Driver_Tree.xlsx Feb Jun
"""
import sys
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]


def load(path):
    df = pd.read_excel(path, sheet_name="Data")
    df["Gross"] = df["Units"] * df["Unit_Price"]
    df["Revenue"] = df["Gross"] * (1 - df["Discount_Pct"])
    df["Month"] = df["Order_Date"].dt.month.map(lambda m: MONTHS[m - 1])
    return df


def drivers(g):
    orders, units = len(g), g["Units"].sum()
    gross, revenue = g["Gross"].sum(), g["Revenue"].sum()
    return pd.Series({
        "Revenue": revenue,
        "Orders": orders,
        "Units_per_order": units / orders,
        "Avg_price": gross / units,
        "Net_rate": revenue / gross,
    })


def bridge(monthly, base, compare):
    a, b = monthly.loc[base], monthly.loc[compare]
    effects = {
        "Orders": (b.Orders - a.Orders) * a.Units_per_order * a.Avg_price * a.Net_rate,
        "Units per order": b.Orders * (b.Units_per_order - a.Units_per_order) * a.Avg_price * a.Net_rate,
        "Price / product mix": b.Orders * b.Units_per_order * (b.Avg_price - a.Avg_price) * a.Net_rate,
        "Discount": b.Orders * b.Units_per_order * b.Avg_price * (b.Net_rate - a.Net_rate),
    }
    out = pd.Series(effects, name=f"{base} -> {compare}")
    assert abs(out.sum() - (b.Revenue - a.Revenue)) < 0.01, "bridge does not add up"
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "Revenue_Driver_Tree.xlsx"
    base = sys.argv[2] if len(sys.argv) > 2 else "Feb"
    compare = sys.argv[3] if len(sys.argv) > 3 else "Jun"
    df = load(path)

    monthly = df.groupby("Month").apply(drivers).reindex(MONTHS)
    print("Monthly drivers\n", monthly.round(2), "\n")
    print("Correlation of revenue with avg price:", round(monthly.Revenue.corr(monthly.Avg_price), 2))
    print("Correlation of revenue with orders:   ", round(monthly.Revenue.corr(monthly.Orders), 2), "\n")

    print("Revenue bridge", base, "->", compare, "\n", bridge(monthly, base, compare).round(0), "\n")

    for col in ["Category", "Region", "Customer_Segment"]:
        seg = df.groupby(col).apply(drivers)
        seg["Avg_discount"] = df.groupby(col)["Discount_Pct"].mean()
        print(f"By {col}\n", seg.sort_values("Revenue", ascending=False).round(2), "\n")

    monthly.round(4).to_csv("monthly_drivers.csv")


if __name__ == "__main__":
    main()
