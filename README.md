# 🚘 CorpRide Command Center

CorpRide Command Center is an enterprise-grade mobility operations analytics platform designed to aggregate, audit, and visualize employee transit performance. By consolidating booking logs, driver rosters, vehicle utilization, safety events, and billing invoices, the platform transforms fragmented, post-facto spreadsheets into actionable operational intelligence.

Designed around a **persona-based dashboard structure**, CorpRide empowers leadership, operations, finance, and security teams with customized, high-fidelity views powered by a robust SQL analytics engine.

---

## 🚀 Key Features

*   **Executive Leadership Dashboard:** High-level strategic overview of overall capital efficiency, carbon/sustainability metrics, and fleet utilization trends.
*   **Operations Dashboard:** Real-time visibility into daily transit runs, passenger occupancy, peak-hour delays, and vendor SLA tracking.
*   **Finance & Audit Dashboard:** Auditing tool specialized in tracking billing discrepancies, detecting invoice leaks (such as "Ghost Billing"), and managing departmental cost allocation.
*   **HR & Safety Dashboard:** Enforces employee duty of care by logging route deviations, active SOS/panic signals, and monitoring responder SLA.
*   **Analytics-First Query Engine:** Uses raw, optimized SQL queries mapped dynamically through an ORM wrapper, with automated fallback compilation for local SQLite development and MySQL production workloads.

---

## 🏗️ Architecture & Technology Stack

The platform is designed to run efficiently on local development environments or scale in containerized cloud infrastructure:

*   **Frontend & UI:** [Streamlit](https://streamlit.io/) with custom-injected CSS providing premium typography (Inter font family) and interactive glassmorphism KPI widgets.
*   **Visualizations:** [Plotly Express](https://plotly.com/) for interactive, responsive charts and spatial representations.
*   **Backend & Data Layer:** [SQLAlchemy ORM](https://www.sqlalchemy.org/) running Python-based database models.
*   **Database Dialect Engine:** 
    *   **Local Dev:** Zero-config SQLite engine (`corpride.db` auto-initializes and auto-seeds).
    *   **Production:** PyMySQL integration for cloud-native MySQL instances.
*   **SQL Analytics:** Custom-compiled SQL templates (`/sql` folder) executed via Pandas with regex-based syntax translation for query compatibility across SQLite and MySQL.

---

## 📈 Metric Framework & KPI Tree

The platform measures enterprise transit performance through a structured KPI hierarchy aimed at reducing waste, saving capital, and securing staff.

```mermaid
graph TD
    %% Objectives
    Obj1[Reduce Transport Waste]
    Obj2[Strengthen Compliance & Care]
    Obj3[Contain Operational Costs]
    
    %% North Star
    NS[North Star: Fleet Utilization Rate]
    
    %% Supporting KPIs
    K_CO[Vehicle Occupancy]
    K_CP[Cost per Ride]
    K_GB[Ghost Billing Loss]
    K_SR[Ride Completion %]
    K_PD[Average Pickup Delay]
    K_RD[Route Deviation Rate]
    K_ST[Active SOS & Resolution Time]

    %% Mappings
    NS --> Obj1
    NS --> Obj3
    
    K_CO --> NS
    K_CP --> Obj3
    K_GB --> Obj3
    
    K_SR --> Obj2
    K_PD --> Obj2
    K_RD --> Obj2
    K_ST --> Obj2
```

### Key Metrics Definition
1.  **Fleet Utilization Rate (North Star):** The percentage of active passenger capacity utilized during operational transits.
2.  **Cost per Ride:** Baseline metric representing total invoice amount divided by total completed rides.
3.  **Ghost Billing Losses:** Financial leakage incurred by invoices submitted for cancelled, failed, or non-existent trips.
4.  **Ride Completion Rate:** Percentage of booked passenger trips completed successfully (measures reliability).
5.  **Average Pickup Delay:** The difference in minutes between driver check-in and scheduled employee pickup.
6.  **Route Deviation Rate:** Percentage of trips where driver GPS coordinates departed from designated geofences.
7.  **SOS SLA Response:** Dispatch desk response times to resolve active SOS distress events.

---

## 🗄️ Database Schema (Entity-Relationship)

The system models complex real-world logistics connections with the following database structure:

```mermaid
erDiagram
    offices ||--o{ employees : "has"
    departments ||--o{ employees : "employs"
    employees ||--o{ ride_bookings : "makes"
    routes ||--o{ ride_bookings : "assigned_to"
    ride_bookings ||--o{ ride_logs : "logs"
    drivers ||--o{ ride_logs : "drives"
    vehicles ||--o{ ride_logs : "used_in"
    ride_bookings ||--o{ billing : "billed_for"
    ride_logs ||--o{ billing : "referenced_by"
    ride_logs ||--o{ incidents : "has"
    
    offices {
        int id PK
        string name
        string city
    }
    departments {
        int id PK
        string name
    }
    employees {
        int id PK
        string name
        int department_id FK
        int office_id FK
    }
    drivers {
        int id PK
        string name
        string license_number
        string vendor_name
        string status
    }
    vehicles {
        int id PK
        string license_plate
        string model
        int capacity
        string vendor_name
        string fuel_type
    }
    routes {
        int id PK
        string name
        string start_location
        string end_location
        float scheduled_distance_km
        int scheduled_duration_mins
    }
    ride_bookings {
        int id PK
        int employee_id FK
        int route_id FK
        datetime booking_time
        datetime scheduled_pickup_time
        string status
    }
    ride_logs {
        int id PK
        int booking_id FK
        int driver_id FK
        int vehicle_id FK
        datetime actual_pickup_time
        datetime actual_drop_time
        float distance_travelled_km
        int duration_mins
        boolean route_deviation
        int delay_minutes
        string status
    }
    billing {
        int id PK
        string invoice_number
        int ride_booking_id FK
        int ride_log_id FK
        float invoice_amount
        string billing_status
    }
    incidents {
        int id PK
        int ride_log_id FK
        string incident_type
        string description
        string severity
        string status
        datetime created_at
        datetime resolved_at
        string resolution_notes
    }
```

---

## 🛠️ Installation & Getting Started

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Data Verification
The project uses a database auto-generator. Running the verification script initializes `corpride.db` (SQLite) locally and seeds it with 30 days of realistic corporate mobility logs, invoice records, and safety tickets.

```bash
python utils/verify_data_layer.py
```

### 5. Running the Web Application
Launch the interactive Streamlit command center:
```bash
streamlit run app.py
```

Once running, open `http://localhost:8501` in your browser.

> [!NOTE]
> By default, the application falls back to SQLite `corpride.db` for zero-configuration setup. To connect to a production MySQL database, specify connection parameters in your environment:
> - `MYSQL_USER`
> - `MYSQL_PASSWORD`
> - `MYSQL_HOST`
> - `MYSQL_PORT`
> - `MYSQL_DATABASE`
> - Or directly supply `DATABASE_URL` (e.g., `mysql+pymysql://user:pass@host:port/dbname`).

---

## 📂 Project Structure

```
CorpRide-Command-Center/
├── app.py                     # Main dashboard entrypoint & Router
├── requirements.txt           # Project library requirements
├── corpride.db                # Auto-generated SQLite Database (generated at runtime)
├── components/
│   ├── common.py              # CSS styles & styled KPI metric HTML components
│   └── filters.py             # Global and regional data filtering sidebar logic
├── database/
│   ├── connection.py          # SQLAlchemy engine constructor & dialect fallback
│   ├── models.py              # Database Schema (Declarative ORM models)
│   └── query_runner.py        # SQL loader, dialect converter (MySQL -> SQLite)
├── docs/
│   ├── kpi_tree.md            # Supporting business KPI hierarchies
│   └── problem_definition.md  # Core business scope and design definitions
├── pages/
│   ├── 1_Executive_Dashboard.py
│   ├── 2_Operations_Dashboard.py
│   ├── 3_Finance_Dashboard.py
│   └── 4_HR_Safety_Dashboard.py
├── sql/
│   └── *.sql                  # Standard optimized SQL query files
└── utils/
    ├── seeder.py              # Synthetic operations dataset generator
    └── verify_data_layer.py   # Test execution of backend queries
