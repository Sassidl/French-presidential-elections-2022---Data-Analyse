import streamlit as st

def write_card(title, stack, repo, last_update):
    # Define the card style using CSS
    card_css = """
    <style>
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            text-align : center;
        }
        .card-tech-stack {
            margin-bottom: 15px;
        }
        .tech {
            display: inline-block;
            background-color: #f0f0f0;
            border-radius: 5px;
            padding: 5px 10px;
            margin-right: 10px;
            font-size: 14px;
        }
        .github-button {
            display: inline-block;
            padding: 10px 15px;
            background-color: #24292e;
            color: white !important;
            border-radius: 5px;
            text-decoration: none !important;
            font-size: 14px;
        }
        .github-button:hover {
            background-color: #333;
            text-decoration: none;
            color: white !important;
        }
        .last-updated {
            margin-top: 10px;
            font-size: 12px;
            color: #888;
        }
    </style>
    """

    # Inject the CSS into Streamlit
    st.markdown(card_css, unsafe_allow_html=True)

    # Create the card layout using HTML
    card_html = f"""
    <div class="card">
        <div class="card-title">{title}</div>
        </div>
        <div class="card-tech-stack">
            <span class="tech">{stack[0]}</span>
            <span class="tech">{stack[1]}</span>
            <span class="tech">{stack[2]}</span>
            <span class="tech">{stack[3]}</span>
        </div>
        <a href="https://github.com/{repo}" class="github-button">View on GitHub</a>
        <div class="last-updated">Last updated: {last_update}</div>
    </div>
    """

    # Inject the HTML for the card into Streamlit
    st.markdown(card_html, unsafe_allow_html=True)