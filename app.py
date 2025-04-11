import streamlit as st
import graphviz
from typing import List, Tuple, Dict, Set
import time
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PDAConfiguration:
    """Formal representation of PDA configuration"""
    state: str
    remaining_input: str
    stack: List[str]

class PDA_StringReverser:
    def __init__(self):
        # Formal definition of PDA components
        self.states: Set[str] = {'q0', 'q1', 'q2'}
        self.input_alphabet: Set[str] = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.stack_alphabet: Set[str] = self.input_alphabet | {'Z'}  # Z is stack bottom
        self.transitions: List[Tuple[str, str, List[str]]] = []
        self.trace: List[PDAConfiguration] = []
        self.transition_function: Dict = self._build_transition_function()
        
        # Performance metrics
        self.space_complexity: int = 0
        self.time_complexity: int = 0
        self.steps_count: int = 0

    def _build_transition_function(self) -> Dict:
        """Builds the formal transition function δ(q, a, Z) → (q', γ)"""
        delta = defaultdict(list)
        # Phase 1: Push input symbols
        for symbol in self.input_alphabet:
            delta[('q0', symbol, 'Z')].append(('q0', [symbol, 'Z']))
            for stack_sym in self.stack_alphabet:
                delta[('q0', symbol, stack_sym)].append(('q0', [symbol, stack_sym]))
        
        # Phase 2: Transition to popping phase
        delta[('q0', 'ε', 'Z')].append(('q1', ['Z']))
        
        # Phase 3: Pop and output
        for symbol in self.stack_alphabet:
            if symbol != 'Z':
                delta[('q1', 'ε', symbol)].append(('q1', []))
        
        # Final transition
        delta[('q1', 'ε', 'Z')].append(('q2', ['Z']))
        return delta

    def push(self, symbol: str) -> None:
        self.stack.append(symbol)
        self.space_complexity = max(self.space_complexity, len(self.stack))
        
    def pop(self) -> str:
        if self.stack:
            return self.stack.pop()
        return None

    def process_input(self, input_string: str, store_trace: bool = False) -> Tuple[bool, List[str], Dict]:
        start_time = time.time()
        self.stack = ['Z']
        self.current_state = 'q0'
        self.transitions = []
        self.trace = []
        self.steps_count = 0
        
        # Phase 1: Push all characters to stack
        remaining_input = input_string
        for char in input_string:
            self.steps_count += 1
            self.transitions.append((self.current_state, char, self.stack.copy()))
            if store_trace:
                self.trace.append(PDAConfiguration(self.current_state, remaining_input, self.stack.copy()))
            self.push(char)
            remaining_input = remaining_input[1:]
            
        self.current_state = 'q1'
        self.transitions.append((self.current_state, 'ε', self.stack.copy()))
        if store_trace:
            self.trace.append(PDAConfiguration(self.current_state, '', self.stack.copy()))
        
        # Phase 2: Pop all characters from stack
        reversed_string = []
        while len(self.stack) > 1:  # Stop before popping Z
            self.steps_count += 1
            char = self.pop()
            reversed_string.append(char)
            self.transitions.append((self.current_state, 'ε', self.stack.copy()))
            if store_trace:
                self.trace.append(PDAConfiguration(self.current_state, '', self.stack.copy()))
            
        self.current_state = 'q2'
        self.transitions.append((self.current_state, 'ε', self.stack.copy()))
        if store_trace:
            self.trace.append(PDAConfiguration(self.current_state, '', self.stack.copy()))
        
        # Calculate complexity metrics
        self.time_complexity = self.steps_count  # O(n) time complexity
        execution_time = time.time() - start_time
        
        metrics = {
            'time_complexity': 'O(n)',
            'space_complexity': 'O(n)',
            'steps_count': self.steps_count,
            'execution_time': execution_time,
            'max_stack_depth': self.space_complexity
        }
        
        return True, reversed_string, metrics

def create_pda_diagram(mode: str = 'simple'):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    
    if mode == 'simple':
        # Basic PDA visualization
        dot.attr('node', shape='circle')
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.attr('node', shape='doublecircle')
        dot.node('q2', 'q2')
        
        dot.edge('q0', 'q0', 'a, Z → aZ\n(for all input symbols)')
        dot.edge('q0', 'q1', 'ε, Z → Z')
        dot.edge('q1', 'q1', 'ε, a → ε\n(pop and output)')
        dot.edge('q1', 'q2', 'ε, Z → Z')
    else:
        # Detailed academic visualization
        dot.attr('node', shape='circle')
        dot.node('q0', 'q0\nPush Phase')
        dot.node('q1', 'q1\nPop Phase')
        dot.attr('node', shape='doublecircle')
        dot.node('q2', 'q2\nAccept')
        
        # Add detailed transitions
        dot.edge('q0', 'q0', 'σ ∈ Σ, γ → σγ\nΣ = {a-z, A-Z, 0-9}\nγ ∈ Γ')
        dot.edge('q0', 'q1', 'ε, Z → Z\nEmpty input')
        dot.edge('q1', 'q1', 'ε, σ → ε\nσ ≠ Z')
        dot.edge('q1', 'q2', 'ε, Z → Z\nStack empty')
        
        # Add formal definition note
        dot.attr(label='''M = (Q, Σ, Γ, δ, q0, Z, {q2})
Q = {q0, q1, q2}
Σ = {a-z, A-Z, 0-9}
Γ = Σ ∪ {Z}''')
    
    return dot

def main():
    st.set_page_config(page_title="Advanced PDA String Reverser", layout="wide")
    
    st.title("Advanced Pushdown Automata String Reverser")
    st.markdown("""
    ### Formal Definition
    This PDA is defined as a 7-tuple (Q, Σ, Γ, δ, q₀, Z, F) where:
    - Q = {q₀, q₁, q₂} is the set of states
    - Σ is the input alphabet (alphanumeric characters)
    - Γ = Σ ∪ {Z} is the stack alphabet
    - δ is the transition function
    - q₀ is the initial state
    - Z is the initial stack symbol
    - F = {q₂} is the set of accepting states
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        input_string = st.text_input("Enter a string to reverse:", "hello")
        visualization_mode = st.radio(
            "Select PDA Visualization Mode:",
            ('Simple', 'Academic'),
            help="Simple mode shows basic transitions, Academic mode includes formal notation"
        )
    
    with col2:
        st.markdown("""
        ### Process Description
        1. **Push Phase (q₀)**: 
           - Read input symbols and push onto stack
           - Maintain stack bottom marker (Z)
        2. **Pop Phase (q₁)**:
           - Pop symbols from stack to generate output
           - Preserve stack bottom marker
        3. **Accept Phase (q₂)**:
           - Reached when stack contains only Z
        """)
    
    if st.button("Process String"):
        # Add session state to prevent recomputation
        if 'pda' not in st.session_state:
            st.session_state.pda = PDA_StringReverser()
        
        pda = st.session_state.pda
        accepted, reversed_chars, metrics = pda.process_input(input_string, visualization_mode == 'Academic')
        
        # Display PDA diagram
        st.subheader("PDA State Diagram")
        dot = create_pda_diagram('academic' if visualization_mode == 'Academic' else 'simple')
        st.graphviz_chart(dot)
        
        # Display execution trace
        st.subheader("Step-by-Step Execution Trace")
        for i, config in enumerate(pda.trace):
            with st.expander(f"Step {i+1}: State {config.state}"):
                st.write(f"Remaining Input: '{config.remaining_input}'")
                st.write(f"Stack Content: {' '.join(config.stack)}")
        
        # Display results and metrics
        if accepted:
            reversed_string = ''.join(reversed_chars)
            st.success(f"Input string: {input_string}")
            st.success(f"Reversed string: {reversed_string}")
            
            # Display complexity analysis
            st.subheader("Complexity Analysis")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Time Complexity", metrics['time_complexity'])
            with col2:
                st.metric("Space Complexity", metrics['space_complexity'])
            with col3:
                st.metric("Steps Count", metrics['steps_count'])
            
            st.info(f"Execution Time: {metrics['execution_time']:.6f} seconds")
            st.info(f"Maximum Stack Depth: {metrics['max_stack_depth']}")
        else:
            st.error("Error in processing the input string")

if __name__ == "__main__":
    main()
