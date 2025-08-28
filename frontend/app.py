
import streamlit as st
import os
import sys

# Dynamically add backend folder to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)



import retriever
