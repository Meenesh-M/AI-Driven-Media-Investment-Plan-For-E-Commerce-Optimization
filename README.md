
# Budget Allocation Model Using Ad Performance Data

This project is a simplified version of a budget allocation model that. It calculates how to distribute a fixed marketing budget across platforms like **Google, Meta, and Microsoft** based on historical performance data.

---

## Dataset Format

The dataset must contain the following fields:

```
Date, Impressions, Reach, Cost, Clicks, Conversions, Revenue
```

### Sample Row:
```
2025-07-15,1000,850,200,80,10,800
```

---

## Calculated Metrics

- **CTR (Click-Through Rate)** = Clicks / Impressions
- **CPC (Cost Per Click)** = Cost / Clicks
- **Conversion Rate** = Conversions / Clicks
- **ROI (Return on Investment)** = (Revenue - Cost) / Cost

---

## Budget Allocation Logic

The model recommends how to split a total budget based on:
- Historical **ROI** per platform
- Weighted performance over time

For example, if Google ads had the highest ROI last week, it receives a larger portion of the future budget.

---

## Tools Used

- Python
- pandas, numpy
- VS Code (or any Python IDE)

---

## Usage

1. Place your dataset in CSV format in the `data/` folder.
2. Run the Python script in `scripts/` to see the recommended allocation.
3. Modify budget value in code as needed.

---

## 🙋‍♂️ Author

**Meenesh Arumuga Velan M, Abi U, Shreenidhi S - M. MTech (CSE)**  
Sri Ramakrishna Engineering College
