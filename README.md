# String Reverser using Pushdown Automata

This project implements a String Reverser using Pushdown Automata (PDA) with a Streamlit-based user interface. It's part of the Automata Theory and Compiler Design (CSE2240) course project.

## Features

- Interactive web interface using Streamlit
- Visual representation of the PDA using Graphviz
- Step-by-step visualization of the PDA execution
- Stack operations visualization
- Support for alphanumeric input strings

## Requirements

- Python 3.7+
- Streamlit
- Graphviz

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Install Graphviz system dependency:
- Windows: Download and install from [Graphviz Download Page](https://graphviz.org/download/)
- Linux: `sudo apt-get install graphviz`
- macOS: `brew install graphviz`

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter any string in the input field and click "Reverse String" to see the PDA in action

## How it Works

The PDA operates in three phases:
1. Initial State (q0): Reads input string and pushes characters onto the stack
2. Processing State (q1): Pops characters from stack to create reversed string
3. Final State (q2): Accepts when stack is empty except for bottom marker

## Authors

[Your Name] 