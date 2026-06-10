-- Example portfolio SQL questions

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
