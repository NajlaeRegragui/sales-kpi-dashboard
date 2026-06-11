from __future__ import annotations

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "cleaned"
DOCS = ROOT / "docs"
DAX = ROOT / "dax"
SQL = ROOT / "sql"
INSIGHTS = ROOT / "insights"
POWERBI = ROOT / "powerbi"

random.seed(42010)


def ensure_dirs() -> None:
    for path in [RAW, CLEAN, DOCS, DAX, SQL, INSIGHTS, POWERBI]:
        path.mkdir(parents=True, exist_ok=True)


def daterange(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def money(value: float) -> str:
    return f"{value:.2f}"


def pct(value: float) -> str:
    return f"{value:.4f}"


def make_date_dim() -> list[dict]:
    rows = []
    for d in daterange(date(2024, 1, 1), date(2026, 12, 31)):
        iso_year, iso_week, _ = d.isocalendar()
        quarter = (d.month - 1) // 3 + 1
        fiscal_year = d.year if d.month >= 1 else d.year - 1
        rows.append(
            {
                "Date": d.isoformat(),
                "DateKey": int(d.strftime("%Y%m%d")),
                "Year": d.year,
                "Quarter": f"Q{quarter}",
                "QuarterNo": quarter,
                "MonthNo": d.month,
                "MonthName": d.strftime("%B"),
                "YearMonth": d.strftime("%Y-%m"),
                "ISOWeek": iso_week,
                "ISOYear": iso_year,
                "DayOfWeekNo": d.isoweekday(),
                "DayOfWeek": d.strftime("%A"),
                "IsWeekend": d.isoweekday() >= 6,
                "FiscalYear": fiscal_year,
            }
        )
    return rows


def make_dimensions():
    regions = [
        ("R01", "West", "Koeln", "Media-Allee 1", 1.12),
        ("R02", "Rhein-Ruhr", "Duesseldorf", "Königsallee", 1.08),
        ("R03", "South", "Muenchen", "Leopoldstrasse", 1.20),
        ("R04", "North", "Hamburg", "HafenCity", 1.05),
        ("R05", "East", "Berlin", "Alexanderplatz", 1.15),
        ("R06", "Central", "Frankfurt", "Mainzer Landstrasse", 1.10),
    ]
    dim_region = [
        {
            "RegionKey": key,
            "SalesRegion": name,
            "MainCity": city,
            "OfficeAddress": addr,
            "MarketIndex": pct(idx),
        }
        for key, name, city, addr, idx in regions
    ]

    products = [
        ("P001", "City-Light-Poster", "OOH Analog", "Street Furniture", 0.42, 145, 1.00),
        ("P002", "Grossflaeche", "OOH Analog", "Billboard", 0.45, 210, 1.07),
        ("P003", "Mega-Light", "OOH Analog", "Premium Billboard", 0.39, 310, 1.18),
        ("P004", "Public Video", "Digital OOH", "Digital Screen", 0.34, 380, 1.32),
        ("P005", "Roadside Screen", "Digital OOH", "Digital Network", 0.33, 420, 1.38),
        ("P006", "Online Display Extension", "Digital Media", "Programmatic", 0.28, 95, 0.92),
        ("P007", "Dialog Media Lead Package", "Dialog Media", "Performance", 0.31, 125, 0.96),
        ("P008", "OOH Plus Crossmedia Bundle", "Crossmedia", "Bundle", 0.36, 560, 1.48),
    ]
    dim_product = [
        {
            "ProductKey": key,
            "ProductName": name,
            "MediaChannel": channel,
            "ProductGroup": group,
            "BaseCostRatio": pct(cost),
            "ListPricePerDay": money(price),
            "PremiumIndex": pct(premium),
        }
        for key, name, channel, group, cost, price, premium in products
    ]

    industries = [
        ("Retail", 1.10),
        ("Automotive", 1.20),
        ("Telecom", 1.05),
        ("FMCG", 1.15),
        ("Finance", 1.00),
        ("Travel", 0.95),
        ("Public Sector", 0.85),
        ("Entertainment", 1.08),
    ]
    customer_names = [
        "RheinMarkt AG",
        "Nova Mobility GmbH",
        "BlueWave Telecom",
        "UrbanSnack GmbH",
        "MediCare Plus",
        "Finova Bank",
        "SunTrip Travel",
        "City Events Group",
        "EcoDrive Deutschland",
        "Koeln Retail Union",
        "MetroStyle Fashion",
        "FoodHero GmbH",
        "NorthAir Logistics",
        "Spark Mobile",
        "Public Health NRW",
        "Berg & Partner Insurance",
        "GamePlanet Media",
        "FreshHome Retail",
        "Autohaus SternWest",
        "GreenCharge Energy",
        "KulturTicket GmbH",
        "FitLife Studios",
        "BauPlus Gruppe",
        "EduCampus Digital",
        "QuickServe Restaurants",
        "Premium Watches DE",
        "CinemaWave",
        "CloudWorks B2B",
        "LocalGov Services",
        "ShopSphere Online",
    ]
    dim_customer = []
    for i, name in enumerate(customer_names, 1):
        industry, weight = random.choice(industries)
        size = random.choices(["Enterprise", "Mid Market", "SMB"], weights=[35, 45, 20])[0]
        dim_customer.append(
            {
                "CustomerKey": f"C{i:03d}",
                "CustomerName": name,
                "Industry": industry,
                "CustomerSegment": size,
                "HQCity": random.choice([r[2] for r in regions]),
                "StrategicAccount": size == "Enterprise" and random.random() < 0.65,
                "IndustryDemandIndex": pct(weight),
            }
        )

    dim_sales_rep = []
    rep_names = [
        "Anna Keller",
        "Jonas Weber",
        "Mira Schmitt",
        "David Klein",
        "Lea Fischer",
        "Nico Wagner",
        "Sofia Hartmann",
        "Felix Braun",
        "Nora Becker",
        "Tim Hoffmann",
        "Amira Yilmaz",
        "Lukas Neumann",
    ]
    for i, name in enumerate(rep_names, 1):
        region = regions[(i - 1) % len(regions)]
        dim_sales_rep.append(
            {
                "SalesRepKey": f"S{i:03d}",
                "SalesRepName": name,
                "RegionKey": region[0],
                "Team": random.choice(["Agency Sales", "Direct Sales", "Key Account", "Digital Sales"]),
                "Seniority": random.choice(["Junior", "Professional", "Senior"]),
                "HireDate": (date(2018, 1, 1) + timedelta(days=random.randint(0, 2200))).isoformat(),
            }
        )

    return dim_region, dim_product, dim_customer, dim_sales_rep


def campaign_seasonality(month: int) -> float:
    return {
        1: 0.78,
        2: 0.86,
        3: 0.97,
        4: 1.04,
        5: 1.11,
        6: 1.15,
        7: 1.02,
        8: 0.94,
        9: 1.18,
        10: 1.25,
        11: 1.34,
        12: 1.10,
    }[month]


def generate_facts(dim_region, dim_product, dim_customer, dim_sales_rep):
    products_by_key = {p["ProductKey"]: p for p in dim_product}
    customers_by_key = {c["CustomerKey"]: c for c in dim_customer}
    regions_by_key = {r["RegionKey"]: r for r in dim_region}
    reps_by_region = {}
    for rep in dim_sales_rep:
        reps_by_region.setdefault(rep["RegionKey"], []).append(rep)

    fact_sales = []
    fact_pipeline = []
    fact_plan = []
    fact_forecast = []
    fact_targets = []
    bridge_campaign_product = []

    campaign_id = 1
    opp_id = 1

    month_starts = []
    d = date(2024, 1, 1)
    while d <= date(2026, 12, 1):
        month_starts.append(d)
        d = date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)

    for month_start in month_starts:
        month_factor = campaign_seasonality(month_start.month)
        for region in dim_region:
            region_factor = float(region["MarketIndex"])
            for product in dim_product:
                product_factor = float(product["PremiumIndex"])
                base = 70000 * month_factor * region_factor * product_factor
                if month_start.year == 2025:
                    base *= 1.08
                elif month_start.year == 2026:
                    base *= 1.16
                if product["MediaChannel"] == "Digital OOH" and month_start >= date(2025, 7, 1):
                    base *= 1.16
                if region["SalesRegion"] == "West" and product["MediaChannel"] == "Crossmedia":
                    base *= 1.10

                plan_revenue = base * random.uniform(0.94, 1.08)
                plan_cost = plan_revenue * (float(product["BaseCostRatio"]) + random.uniform(-0.015, 0.018))
                fact_plan.append(
                    {
                        "PlanKey": f"PL{month_start.strftime('%Y%m')}{region['RegionKey']}{product['ProductKey']}",
                        "MonthStartDate": month_start.isoformat(),
                        "RegionKey": region["RegionKey"],
                        "ProductKey": product["ProductKey"],
                        "PlanRevenue": money(plan_revenue),
                        "PlanCost": money(plan_cost),
                        "PlanBookings": round(plan_revenue / float(product["ListPricePerDay"]) / 19, 0),
                    }
                )

                forecast_bias = 1.0
                if month_start >= date(2026, 4, 1) and product["MediaChannel"] == "Digital Media":
                    forecast_bias = 0.90
                if month_start >= date(2026, 2, 1) and region["SalesRegion"] == "South":
                    forecast_bias *= 1.06
                forecast_revenue = plan_revenue * random.uniform(0.91, 1.13) * forecast_bias
                fact_forecast.append(
                    {
                        "ForecastKey": f"FC{month_start.strftime('%Y%m')}{region['RegionKey']}{product['ProductKey']}",
                        "MonthStartDate": month_start.isoformat(),
                        "RegionKey": region["RegionKey"],
                        "ProductKey": product["ProductKey"],
                        "ForecastRevenue": money(forecast_revenue),
                        "ForecastCost": money(forecast_revenue * (float(product["BaseCostRatio"]) + random.uniform(-0.01, 0.02))),
                        "ForecastVersion": "Rolling Forecast",
                    }
                )

            for rep in [r for r in dim_sales_rep if r["RegionKey"] == region["RegionKey"]]:
                target = 145000 * month_factor * region_factor * random.uniform(0.92, 1.14)
                fact_targets.append(
                    {
                        "TargetKey": f"TG{month_start.strftime('%Y%m')}{rep['SalesRepKey']}",
                        "MonthStartDate": month_start.isoformat(),
                        "SalesRepKey": rep["SalesRepKey"],
                        "RegionKey": rep["RegionKey"],
                        "TargetRevenue": money(target),
                        "TargetMargin": money(target * random.uniform(0.58, 0.66)),
                        "TargetNewBusiness": money(target * random.uniform(0.22, 0.34)),
                    }
                )

    for month_start in month_starts:
        if month_start > date(2026, 5, 1):
            continue
        campaigns_this_month = random.randint(42, 72)
        for _ in range(campaigns_this_month):
            region = random.choice(dim_region)
            rep = random.choice(reps_by_region[region["RegionKey"]])
            customer = random.choice(dim_customer)
            n_products = random.choices([1, 2, 3], weights=[68, 25, 7])[0]
            selected_products = random.sample(dim_product, n_products)
            start_offset = random.randint(0, 27)
            start_date = month_start + timedelta(days=start_offset)
            duration = random.choice([7, 10, 14, 21, 28, 35])
            end_date = start_date + timedelta(days=duration - 1)
            campaign_key = f"CA{campaign_id:05d}"
            campaign_id += 1
            campaign_name = f"{customer['CustomerName']} {start_date.strftime('%b %Y')} Flight"
            booking_status = random.choices(["Booked", "Completed", "Cancelled"], weights=[15, 80, 5])[0]
            if end_date > date(2026, 5, 31):
                booking_status = "Booked"

            total_campaign_revenue = 0
            total_campaign_cost = 0
            total_impressions = 0
            total_available = 0
            weighted_discount = 0

            for product in selected_products:
                list_price = float(product["ListPricePerDay"])
                region_factor = float(region["MarketIndex"])
                industry_factor = float(customer["IndustryDemandIndex"])
                digital_factor = 1.15 if product["MediaChannel"] in ["Digital OOH", "Crossmedia"] else 1.0
                season = campaign_seasonality(start_date.month)
                booked_units = max(1, int(random.gauss(18, 7) * digital_factor))
                available_units = int(booked_units / random.uniform(0.72, 0.96))
                discount_rate = min(0.32, max(0.02, random.gauss(0.115, 0.05)))
                if customer["StrategicAccount"] == "True" or customer["StrategicAccount"] is True:
                    discount_rate += random.uniform(0.015, 0.045)
                revenue = list_price * duration * booked_units * region_factor * industry_factor * season * (1 - discount_rate)
                if booking_status == "Cancelled":
                    revenue *= random.uniform(0.0, 0.18)
                cost_ratio = float(product["BaseCostRatio"]) + random.uniform(-0.025, 0.035)
                delivery_cost = revenue * cost_ratio
                impressions = int(booked_units * duration * random.uniform(8500, 38000) * float(product["PremiumIndex"]))

                bridge_campaign_product.append(
                    {
                        "CampaignKey": campaign_key,
                        "ProductKey": product["ProductKey"],
                        "BookedUnits": booked_units,
                        "AvailableUnits": available_units,
                        "ProductRevenue": money(revenue),
                        "ProductCost": money(delivery_cost),
                    }
                )
                total_campaign_revenue += revenue
                total_campaign_cost += delivery_cost
                total_impressions += impressions
                total_available += available_units
                weighted_discount += discount_rate / n_products

            if region["SalesRegion"] == "East" and start_date >= date(2025, 9, 1):
                total_campaign_revenue *= 0.90
            if product["MediaChannel"] == "Digital Media" and start_date >= date(2026, 3, 1):
                total_campaign_revenue *= 0.87

            fact_sales.append(
                {
                    "CampaignKey": campaign_key,
                    "CampaignName": campaign_name,
                    "StartDate": start_date.isoformat(),
                    "EndDate": end_date.isoformat(),
                    "BookingDate": (start_date - timedelta(days=random.randint(8, 60))).isoformat(),
                    "CustomerKey": customer["CustomerKey"],
                    "SalesRepKey": rep["SalesRepKey"],
                    "RegionKey": region["RegionKey"],
                    "PrimaryProductKey": selected_products[0]["ProductKey"],
                    "BookingStatus": booking_status,
                    "Revenue": money(total_campaign_revenue),
                    "DeliveryCost": money(total_campaign_cost),
                    "GrossMargin": money(total_campaign_revenue - total_campaign_cost),
                    "DiscountAmount": money(total_campaign_revenue * weighted_discount / max(0.01, 1 - weighted_discount)),
                    "DiscountRate": pct(weighted_discount),
                    "Impressions": total_impressions,
                    "BookedUnits": sum(int(x["BookedUnits"]) for x in bridge_campaign_product if x["CampaignKey"] == campaign_key),
                    "AvailableUnits": total_available,
                    "DataQualityFlag": random.choices(
                        ["OK", "Missing CRM Industry", "Late Booking Date", "Manual Price Override", "Unmapped Product"],
                        weights=[88, 3, 4, 4, 1],
                    )[0],
                    "CRMSource": random.choices(["Salesforce", "Manual Upload", "Legacy CRM"], weights=[82, 10, 8])[0],
                }
            )

            stage = random.choices(
                ["Prospecting", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
                weights=[16, 18, 20, 15, 22, 9],
            )[0]
            stage_probability = {
                "Prospecting": 0.15,
                "Qualified": 0.30,
                "Proposal": 0.55,
                "Negotiation": 0.72,
                "Closed Won": 1.00,
                "Closed Lost": 0.00,
            }[stage]
            expected_close = start_date - timedelta(days=random.randint(2, 25))
            opp_amount = total_campaign_revenue * random.uniform(0.8, 1.35)
            fact_pipeline.append(
                {
                    "OpportunityKey": f"OP{opp_id:05d}",
                    "CampaignKey": campaign_key,
                    "CreatedDate": (expected_close - timedelta(days=random.randint(12, 90))).isoformat(),
                    "ExpectedCloseDate": expected_close.isoformat(),
                    "CustomerKey": customer["CustomerKey"],
                    "SalesRepKey": rep["SalesRepKey"],
                    "RegionKey": region["RegionKey"],
                    "PrimaryProductKey": selected_products[0]["ProductKey"],
                    "SalesStage": stage,
                    "StageProbability": pct(stage_probability),
                    "OpportunityAmount": money(opp_amount),
                    "WeightedPipeline": money(opp_amount * stage_probability),
                    "LostReason": "" if stage != "Closed Lost" else random.choice(["Price", "Timing", "Competitor", "Budget Frozen"]),
                    "NextStepMissing": random.random() < 0.11,
                }
            )
            opp_id += 1

    return fact_sales, fact_pipeline, fact_plan, fact_forecast, fact_targets, bridge_campaign_product


def write_docs() -> None:
    (DOCS / "project_brief.md").write_text(
        """# Sales Data Analyst Portfolio Project

## Business Context
This project simulates a Sales Data Analyst role at a German out-of-home and digital media company. The analyst supports Sales, Management, IT/Product Development and Controlling by turning CRM, campaign and planning data into one trusted KPI model.

## Job-Ad Translation
- Main tasks: ad-hoc analysis, KPI dashboards, management reporting, requirements analysis, user stories, internal tool improvement and project ownership.
- Business areas: Sales, Key Account, Digital Sales, Campaign Operations, Controlling, IT/Development and Management.
- Tools reflected: Power BI, Excel-ready CSV exports, Salesforce-like CRM fields, DAX measures and SQL analysis queries.
- Core data types: actual campaign bookings, media inventory, customer and industry master data, Salesforce pipeline, monthly plan, rolling forecast and sales targets.

## Business Logic
- Revenue is campaign booking revenue after discounts.
- Delivery cost is calculated from product-level cost ratios with realistic variance.
- Gross margin is revenue minus delivery cost.
- Utilization is booked media units divided by available media units.
- Pipeline uses stage probability to calculate weighted pipeline.
- Plan and forecast are monthly by region and product.
- Targets are monthly by sales representative and region.

## Interview Story
The model shows how a Sales Data Analyst can align Sales, IT and Management around common metrics, identify revenue gaps, explain margin pressure, validate pipeline quality and detect data quality issues before they affect decisions.
""",
        encoding="utf-8",
    )

    (DOCS / "data_dictionary.md").write_text(
        """# Data Dictionary

## DimDate
Calendar table from 2024-01-01 to 2026-12-31. Use `Date` as date table column.

## DimCustomer
Customer master data with industry, segment, HQ city, strategic account flag and industry demand index.

## DimProduct
Media products across OOH Analog, Digital OOH, Digital Media, Dialog Media and Crossmedia. Includes base cost ratio and list price per day.

## DimRegion
Sales regions and office markets with a market demand index.

## DimSalesRep
Sales representative master data with team, region, seniority and hire date.

## FactSales
Actual campaign bookings. Grain: one row per campaign. Contains booking dates, customer, sales rep, region, primary product, revenue, cost, margin, discounts, impressions, inventory units, CRM source and data quality flag.

## BridgeCampaignProduct
Campaign-to-product bridge. Grain: one row per campaign/product. Supports product mix analysis for bundled campaigns.

## FactPipeline
Salesforce-like opportunity pipeline. Grain: one row per opportunity. Contains sales stage, probability, opportunity amount, weighted pipeline and lost reason.

## FactPlan
Monthly plan by region and product. Scenario: Plan.

## FactForecast
Monthly rolling forecast by region and product. Scenario: Forecast.

## FactTargets
Monthly target by sales representative and region. Scenario: Target.
""",
        encoding="utf-8",
    )

    (DAX / "measures.md").write_text(
        """# DAX Measures

Create these measures in the `_Measures` table.

```DAX
Revenue = SUM(FactSales[Revenue])
Delivery Cost = SUM(FactSales[DeliveryCost])
Gross Margin = [Revenue] - [Delivery Cost]
Gross Margin % = DIVIDE([Gross Margin], [Revenue])
Discount Amount = SUM(FactSales[DiscountAmount])
Discount Rate % = DIVIDE([Discount Amount], [Revenue] + [Discount Amount])
Campaigns = DISTINCTCOUNT(FactSales[CampaignKey])
Avg Campaign Revenue = DIVIDE([Revenue], [Campaigns])
Impressions = SUM(FactSales[Impressions])
CPM = DIVIDE([Revenue], [Impressions]) * 1000
Booked Units = SUM(FactSales[BookedUnits])
Available Units = SUM(FactSales[AvailableUnits])
Inventory Utilization % = DIVIDE([Booked Units], [Available Units])
Plan Revenue = SUM(FactPlan[PlanRevenue])
Revenue vs Plan = [Revenue] - [Plan Revenue]
Revenue vs Plan % = DIVIDE([Revenue vs Plan], [Plan Revenue])
Forecast Revenue = SUM(FactForecast[ForecastRevenue])
Revenue vs Forecast = [Revenue] - [Forecast Revenue]
Revenue vs Forecast % = DIVIDE([Revenue vs Forecast], [Forecast Revenue])
Target Revenue = SUM(FactTargets[TargetRevenue])
Target Attainment % = DIVIDE([Revenue], [Target Revenue])
Weighted Pipeline = SUM(FactPipeline[WeightedPipeline])
Pipeline Coverage = DIVIDE([Weighted Pipeline], [Target Revenue])
Open Pipeline = CALCULATE(SUM(FactPipeline[OpportunityAmount]), NOT FactPipeline[SalesStage] IN {"Closed Won", "Closed Lost"})
Win Rate % = DIVIDE(CALCULATE(COUNTROWS(FactPipeline), FactPipeline[SalesStage] = "Closed Won"), CALCULATE(COUNTROWS(FactPipeline), FactPipeline[SalesStage] IN {"Closed Won", "Closed Lost"}))
Data Quality Issues = CALCULATE(COUNTROWS(FactSales), FactSales[DataQualityFlag] <> "OK")
Data Quality Issue % = DIVIDE([Data Quality Issues], COUNTROWS(FactSales))
Digital Revenue = CALCULATE([Revenue], DimProduct[MediaChannel] IN {"Digital OOH", "Digital Media", "Crossmedia"})
Digital Revenue Share % = DIVIDE([Digital Revenue], [Revenue])

-- Optional generic portfolio aliases
Total Sales = [Revenue]
Total Profit = [Gross Margin]
Order Count = [Campaigns]
Total Quantity = [Booked Units]
Average Order Value = [Avg Campaign Revenue]
Profit Margin % = [Gross Margin %]
```
""",
        encoding="utf-8",
    )

    (SQL / "sales_analysis_queries.sql").write_text(
        """-- Example portfolio SQL questions

-- 1. Revenue and margin by region and month
SELECT
  d.YearMonth,
  r.SalesRegion,
  SUM(s.Revenue) AS Revenue,
  SUM(s.GrossMargin) AS GrossMargin,
  SUM(s.GrossMargin) / NULLIF(SUM(s.Revenue), 0) AS GrossMarginPct
FROM FactSales s
JOIN DimDate d ON s.StartDate = d.Date
JOIN DimRegion r ON s.RegionKey = r.RegionKey
GROUP BY d.YearMonth, r.SalesRegion;

-- 2. Data quality issues by CRM source
SELECT CRMSource, DataQualityFlag, COUNT(*) AS IssueRows
FROM FactSales
WHERE DataQualityFlag <> 'OK'
GROUP BY CRMSource, DataQualityFlag;

-- 3. Pipeline coverage by sales team
SELECT
  sr.Team,
  SUM(p.WeightedPipeline) AS WeightedPipeline,
  SUM(t.TargetRevenue) AS TargetRevenue
FROM FactPipeline p
JOIN DimSalesRep sr ON p.SalesRepKey = sr.SalesRepKey
JOIN FactTargets t ON p.SalesRepKey = t.SalesRepKey
GROUP BY sr.Team;
""",
        encoding="utf-8",
    )

    (INSIGHTS / "interview_insights.md").write_text(
        """# Interview Insights

- Digital OOH grows faster after mid-2025, but delivery cost and discount pressure reduce margin in selected regions.
- East region underperforms after September 2025, creating a useful Actual vs Plan investigation.
- Digital Media forecast becomes too optimistic in 2026, which creates a Forecast Accuracy story.
- Strategic accounts generate high revenue but require higher discounts, so margin should be monitored separately from revenue.
- Salesforce/manual/legacy CRM sources contain different data quality flags, useful for a process-improvement discussion with IT and Sales Operations.
- Pipeline coverage and target attainment can be shown by sales team to support management steering.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    dim_date = make_date_dim()
    dim_region, dim_product, dim_customer, dim_sales_rep = make_dimensions()
    fact_sales, fact_pipeline, fact_plan, fact_forecast, fact_targets, bridge = generate_facts(
        dim_region, dim_product, dim_customer, dim_sales_rep
    )

    tables = {
        "DimDate": dim_date,
        "DimRegion": dim_region,
        "DimProduct": dim_product,
        "DimCustomer": dim_customer,
        "DimSalesRep": dim_sales_rep,
        "FactSales": fact_sales,
        "BridgeCampaignProduct": bridge,
        "FactPipeline": fact_pipeline,
        "FactPlan": fact_plan,
        "FactForecast": fact_forecast,
        "FactTargets": fact_targets,
    }
    for name, rows in tables.items():
        fieldnames = list(rows[0].keys())
        write_csv(RAW / f"{name}.csv", rows, fieldnames)
        write_csv(CLEAN / f"{name}.csv", rows, fieldnames)

    write_csv(RAW / "sales_data_raw.csv", fact_sales, list(fact_sales[0].keys()))
    write_csv(CLEAN / "sales_data_cleaned.csv", fact_sales, list(fact_sales[0].keys()))

    write_docs()
    print("Generated tables:")
    for name, rows in tables.items():
        print(f"- {name}: {len(rows):,} rows")


if __name__ == "__main__":
    main()
