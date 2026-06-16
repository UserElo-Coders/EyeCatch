# EyeCatch v2.0

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-2.0-orange)

Next-generation system monitoring platform built with scalability, modularity and advanced visualization in mind.

EyeCatch V2 introduces a completely redesigned architecture focused on maintainability, performance and future enterprise-grade features.

---

# What's New

## New Dashboard Architecture

The UI has been rebuilt using reusable components:

* BasePage
* ResourcePage
* MetricCard
* ChartCard
* PageHeader
* ScrollableFrame

This allows new monitoring pages to be created with minimal code.

---

## Advanced Charts

### Real-Time Graphs

* Historical metrics
* Animated transitions
* Area-filled charts
* Glow effects
* Dynamic tooltips
* Current value highlighting
* Responsive layout

Powered by:

* Matplotlib
* NumPy

---

## Resource History

Every monitored metric now stores historical data.

Examples:

* CPU usage history
* RAM consumption history
* Network throughput history
* Disk activity history

This enables future:

* Analytics
* Forecasting
* Alerts
* Reporting

---

## Improved Performance

### Smart Updates

The system updates only the information currently required.

Benefits:

* Lower CPU usage
* Lower RAM usage
* Faster navigation
* Reduced UI blocking

### Process Optimization

Process monitoring now uses:

* Intelligent caching
* Delayed refresh intervals
* Efficient sorting

---

## Design System

EyeCatch now follows a dedicated design system.

### UserEx Design Language

Color palette:

```text
Background: #0F1115
Surface:    #171A21
Primary:    #4F8CFF
Text:       #FFFFFF
Secondary:  #9CA3AF
```

### UX Improvements

* Consistent spacing
* Responsive cards
* Scrollable layouts
* Unified typography
* Better information hierarchy

---

## Architecture

```text
EyeCatch/
│
├── core/
│   ├── monitor.py
│   ├── history_service.py
│   └── view_model.py
│
├── models/
│
├── ui/
│   ├── components/
│   │   ├── metric_card.py
│   │   ├── chart_card.py
│   │   ├── page_header.py
│   │   └── scrollable_frame.py
│   │
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── resource_page.py
│   │   ├── cpu_page.py
│   │   ├── ram_page.py
│   │   ├── disk_page.py
│   │   ├── network_page.py
│   │   └── process_page.py
│   │
│   └── theme/
│
└── main.py
```

---

## Roadmap

### V2.1

* Export data to CSV
* Export charts to PNG
* Configurable refresh interval
* Dark/Light themes

### V2.2

* Process search
* Process termination
* System notifications
* Alert system

### V3.0

* Multi-platform installer
* Plugin system
* Cloud synchronization
* Remote monitoring
* UserEx ecosystem integration

---

## Installation

### Windows

Download the latest executable from Releases.

### From Source

```bash
git clone https://github.com/your-username/EyeCatch.git

cd EyeCatch

pip install -r requirements.txt

python main.py
```

---

## License

MIT License

---

## Author

Developed by Guilherme Döge.

Built as part of the UserEx ecosystem.
