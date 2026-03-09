# ⛵ Missionaries and Cannibals Game

An interactive implementation of the classic **Missionaries and Cannibals river crossing puzzle**, built using **Python and Streamlit**.

The objective of the puzzle is to move **three missionaries and three cannibals** safely across a river using a boat that can carry **at most two people at a time**, while ensuring that **cannibals never outnumber missionaries on either bank**.


## 🎮 Play the Game Online

You can play the game directly here:

👉 **Live Demo:**
https://missionaries-and-cannibals-game.streamlit.app/


## 🎯 Objective

Transport all missionaries and cannibals from the **right bank to the left bank** without violating the safety rules.


## 📜 Game Rules

* The boat can carry **1 or 2 people only**
* The boat **cannot cross empty**
* Cannibals must **never outnumber missionaries** on either bank (unless there are zero missionaries there)
* If cannibals outnumber missionaries on any bank, the missionaries get eaten and the **game ends**


## 🚀 Features

* Interactive **river simulation interface**
* Visual representation using **emoji characters**
* **Boat movement animation**
* **Move history tracking**
* **Win/Loss detection**
* Quick move buttons for faster gameplay
* Clean and responsive **Streamlit UI**


## 🛠 Technologies Used

* **Python**
* **Streamlit**
* HTML & CSS styling within Streamlit


## ▶️ How to Run the Project Locally

### 1. Clone the repository

```bash
https://github.com/psumarani/Missionaries-and-Cannibals-Game.git
```

### 2. Navigate to the project directory

```bash
cd Missionaries-and-Cannibals-Game
```

### 3. Install required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```
if prompts error use 
```bash
python -m streamlit run app.py
```

### 5. Open in browser

Streamlit will automatically open the app in your browser.
If it does not open automatically, visit:

```
http://localhost:8501
```


## 🧠 About the Puzzle

The **Missionaries and Cannibals problem** is a well-known puzzle in **Artificial Intelligence and problem-solving**, commonly used to demonstrate **state-space search, constraints, and logical reasoning**.


## 📌 Author
Prasad Umarani

Developed as part of an academic project using **Python and Streamlit**.
