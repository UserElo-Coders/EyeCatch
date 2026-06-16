# EyeCatch v1.0

A modern desktop system monitoring application built with Python and Tkinter.

EyeCatch provides real-time monitoring of CPU, RAM, Disk, Network, and running Processes through a clean and lightweight interface inspired by modern dashboard systems.

---

## Features

### CPU Monitoring

* Real-time CPU usage
* CPU frequency
* Physical cores count
* Logical threads count
* Temperature monitoring (when supported)

### RAM Monitoring

* Total memory
* Used memory
* Available memory
* Cached memory
* Usage percentage

### Disk Monitoring

* Total storage
* Free storage
* Disk usage percentage
* Read speed
* Write speed

### Network Monitoring

* Upload speed
* Download speed
* Total bytes sent
* Total bytes received

### Process Monitoring

* Running processes list
* CPU consumption per process
* Memory consumption per process
* Process status
* Performance-optimized caching

---

## Technology Stack

* Python 3.12+
* Tkinter
* psutil
* Pillow

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/EyeCatch.git
cd EyeCatch
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## Screenshots

Add screenshots here.

---

## Project Structure

```text
EyeCatch/
│
├── assets/
├── core/
├── models/
├── ui/
│   ├── components/
│   ├── pages/
│   └── theme/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Performance Improvements

Version 1 includes:

* Process caching
* Reduced UI refresh workload
* Optimized system polling
* Faster page navigation

---

## License

MIT License

---

## Author

Developed by Guilherme Döge.
