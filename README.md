# MerchantOfVenice-
Designed an end-to-end e-commerce analytics pipeline: cleaned and transformed raw data, built SQL tables, developed Python ETL scripts, modeled KPIs, and created BI dashboards for sales, customer behavior, and product performance insights.

# Merchant of Venice 🎭

**E-Commerce Business Intelligence Platform**

## Project Status
✅ Day 1 Complete - Data Foundation

## What I Built Today
- Designed normalized database schema (3 tables)
- Created data loading pipeline with error handling
- Loaded 400k+ transactions into SQL Server
- Established customer and product master tables

## Tech Stack
- **Database:** SQL Server
- **Processing:** Python, Pandas
- **Connection:** PyODBC
- **Data Source:** UCI Online Retail Dataset (541k transactions)

## Database Schema

### Tables:
1. **transactions** (~400k rows) - All purchase events
2. **customers** (~4k rows) - Customer master with aggregates
3. **products** (~3k rows) - Product catalog

### Design Principles:
- Normalized structure (3NF)
- Referential integrity
- Calculated columns for performance
- Duplicate prevention in loading

## Project Structure
```
merchant-of-venice/
├── data/                    # Raw dataset
├── scripts/                 # Python ETL scripts
│   └── load_data.py        # Data loading pipeline
├── database/               
│   └── schema.sql          # SQL Server schema
├── visualizations/         # (Coming: Week 2)
├── powerbi/               # (Coming: Week 2)
└── docs/                  # Documentation
```

## Progress

### Week 1: Data Foundation ✅
- [x] Database design
- [x] Schema creation
- [x] Data loading pipeline
- [x] Data validation
- [ ] Analysis queries (Next)

### Week 2: Analysis & Visualization (Upcoming)
- [ ] Customer segmentation (RFM)
- [ ] Product performance analysis
- [ ] Plotly interactive dashboard
- [ ] Power BI executive dashboard

## Key Metrics (Preliminary)
- **Total Transactions:** 400,000+
- **Unique Customers:** 4,000+
- **Unique Products:** 3,000+
- **Date Range:** Dec 2010 - Dec 2011
- **Countries:** 38

## What's Next
- Customer segmentation analysis
- Sales trend analysis
- Product performance metrics
- Interactive visualizations

## Author
**Abubakar Yahya Ibrahim**

Building in public | Full Stack Data Analytics

---

**Day 1 Status:** Foundation Complete ✅  
**Focus Tomorrow:** Analysis & Insights

## Progress

### Week 1: Data Foundation & Analysis ✅
- [x] Database design & data loading
- [x] Customer segmentation (RFM)
- [x] Product performance analysis
- [x] Interactive Plotly dashboard with 5 visualizations
- [x] Exported HTML dashboard

### Visualizations Created
1. Monthly Revenue Trend (Line Chart)
2. Customer Segment Distribution (Pie Chart)
3. Top 10 Products by Revenue (Bar Chart)
4. Geographic Revenue Distribution (Bar Chart)
5. RFM Customer Analysis (Scatter Plot)

**View Dashboard:** `visualizations/merchant_of_venice_dashboard.html`

*Last updated: 2025-12-11
