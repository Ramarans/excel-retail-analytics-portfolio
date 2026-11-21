# Revenue Driver Tree – Excel & Python

A business performance deep-dive on 150 retail orders (Jan–Jun 2026). It breaks revenue into its drivers, explains why revenue changes from month to month, and turns the result into recommendations.

**Revenue = Orders × Units per order × Average price per unit × Net rate (1 − discount)**

## Question

Revenue swings a lot from month to month. Is that because fewer people order, because baskets get smaller, because of what they buy, or because of discounts?

## What the workbook covers

| Sheet | What it shows | Excel skills |
|---|---|---|
| **Driver_Tree** | The driver tree, revenue split by category, key findings and recommendations | Linked formulas, TEXT-built live findings |
| **Monthly_Drivers** | All four drivers per month, a check that they multiply back to revenue, month-on-month change, correlation | COUNTIFS, SUMIFS, CORREL, IF |
| **Bridge** | Revenue bridge between any two months, split into orders, basket size, price/product mix and discount effects | INDEX/MATCH, sequential substitution, bar chart |
| **Segments** | The same drivers by category, region, channel and customer segment | COUNTIFS, SUMIFS, AVERAGEIFS |
| **Data** | The 150 orders | Excel Tables, formulas |

Change the two yellow month cells on **Bridge** to compare any two months. Every number updates.

`driver_tree.py` repeats the analysis in Python (pandas) and checks that the bridge adds up.

```
python driver_tree.py Revenue_Driver_Tree.xlsx Feb Jun
```

## Key findings

- **Orders are stable** (23–26 per month), but revenue swings between 6,202 and 12,513. Revenue follows the average price per unit (correlation 0.94), not order count.
- **Feb → Jun:** revenue fell by 6,311. The price / product-mix effect alone was −8,205. More orders and bigger baskets actually added 2,121.
- **North** has 32 orders but the lowest average price (96 vs 149 overall). The gap is product mix, not demand.
- **Returning customers** get the highest average discount (12.0%), more than VIP customers (8.5%).

## Recommendations

1. In the monthly report, track product mix (Electronics orders and average price) as the lead driver, not only order count.
2. In the North region, push higher-value categories (Electronics, Home) instead of trying to win more orders.
3. Review the discount rules for returning customers, so they do not get more discount than VIP customers.

## Repository structure

```
revenue-driver-tree/
├── Revenue_Driver_Tree.xlsx
├── driver_tree.py
└── README.md
```

Data: the same retail dataset as the main [Excel Retail Analytics Portfolio](../README.md) in this repository.

---
**Saideepak Ramarangula** · Berlin
