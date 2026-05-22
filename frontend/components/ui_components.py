import streamlit as st

class UIComponents:
    @staticmethod
    def render_metric_card(label: str, value: str, delta: str = None, help_text: str = None):
        """Standardized modular metric components containing brand theme patterns."""
        st.metric(label=label, value=value, delta=delta, help=help_text)
