import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Lead Prioritizer", layout="wide")

st.title("AI Lead Prioritizer & Smart Outreach Assistant")
st.markdown("""
Upload your leads and let the AI score them as Hot, Warm, or Cold.
You’ll also get personalized message suggestions and filters to help you focus on the right customers.
""")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file with leads", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Scoring logic
    def score_lead(row):
        if row['salary'] >= 40000 and row['interest'].strip().lower() == 'yes' and row['last_interaction_days'] <= 7:
            return 'Hot'
        elif row['salary'] >= 30000 and row['last_interaction_days'] <= 14:
            return 'Warm'
        else:
            return 'Cold'

    def generate_message(row):
        name = row['name']
        product = row['product'].strip().lower()
        if product == 'credit card':
            return f"Hi {name}, you could save ₹5,000/year with our cashback card. Shall I show you how?"
        elif product == 'loan':
            return f"Hi {name}, our loan offer is quick and paperless. Want to know your eligibility today?"
        elif product == 'demat':
            return f"Hi {name}, opening a Demat account is free this month. Shall I help you get started?"
        elif product == 'insurance':
            return f"Hi {name}, protect your family with our instant, paperless insurance plans. Can I help?"
        else:
            return f"Hi {name}, we have a special offer for you. Can I share the details?"

    # Apply scoring and message logic
    df['Lead Score'] = df.apply(score_lead, axis=1)
    df['Suggested Message'] = df.apply(generate_message, axis=1)

    # Summary metrics
    st.subheader("Lead Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Hot Leads", df[df['Lead Score'] == 'Hot'].shape[0])
    col2.metric("Warm Leads", df[df['Lead Score'] == 'Warm'].shape[0])
    col3.metric("Cold Leads", df[df['Lead Score'] == 'Cold'].shape[0])

    # Filter options
    st.subheader("Filter Leads")
    score_filter = st.selectbox("Filter by Score", ["All", "Hot", "Warm", "Cold"])
    product_filter = st.selectbox("Filter by Product", ["All"] + sorted(df['product'].unique()))

    filtered_df = df.copy()
    if score_filter != "All":
        filtered_df = filtered_df[filtered_df["Lead Score"] == score_filter]
    if product_filter != "All":
        filtered_df = filtered_df[filtered_df["product"] == product_filter]

    # Show full table
    st.subheader("Leads Table View")
    st.dataframe(filtered_df.sort_values(by="Lead Score", ascending=True), use_container_width=True)

    # Show card view
    st.subheader("Lead Cards View")
    for i, row in filtered_df.iterrows():
        with st.container():
            st.markdown("---")
            cols = st.columns([2, 2, 6])
            with cols[0]:
                st.markdown(f"**{row['name']}**")
                st.markdown(f"Salary: ₹{row['salary']:,}")
                st.markdown(f"Last Contact: {row['last_interaction_days']} days ago")
                st.markdown(f"Product: {row['product']}")
                st.markdown(f"Lead Score: **{row['Lead Score']}**")
            with cols[1]:
                st.markdown("**Suggested Message**")
                st.info(row['Suggested Message'])
            with cols[2]:
                st.markdown("**Actions**")
                st.button(f"Mark {row['name']} as Contacted", key=f"contacted_{i}")
                st.button(f"Send WhatsApp to {row['name']}", key=f"whatsapp_{i}")
else:
    st.info("Please upload a CSV file with columns: name, salary, interest, product, last_interaction_days.")
