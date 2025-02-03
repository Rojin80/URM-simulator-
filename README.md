# **URM Simulator**

A web-based **Universal Register Machine (URM)** simulator built with Flask. This project is the final assignment for the **Computability Theory** course by **Dr. Alizadeh**.

## **Features**

- Simulates URM programs.
- Provides a UI-based version using Flask.
- Also includes a simple command-line version.

---

## **Installation & Setup**

To set up and run the simulator locally, follow these steps:

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/URM-simulator.git
cd URM-simulator
```

### **2. Install Dependencies**

Ensure you have Python installed, then run:

```bash
pip install -r requirement.txt
```

---

## **Running the Simulator**

### **Option 1: Run the Web-Based UI**

Start the Flask-based UI simulator:

```bash
python app.py
```

Then, open a browser and go to:\
➡ **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

### **Option 2: Run the Simple Command-Line Version**

If you prefer a terminal-based version, run:

```bash
python simulator.py
```

---

## **Usage**

- The web version allows interactive program execution.
- The command-line version processes URM instructions from a file or standard input.

---

## **File Structure**

```
URM-simulator/
│── app.py            # Flask-based web interface
│── GUI.py            # GUI logic (if applicable)
│── logic.py          # Core computation logic
│── main.py           # Entry point for the application
│── simulator.py      # Core URM simulation logic
│── requirement.txt   # Required dependencies
│── templates/        # HTML templates
│── readme.md         # Documentation
│── __pycache__/      # Compiled Python files
│── app.spec          # Build specification file
│── main.spec         # Build specification file
```

---



