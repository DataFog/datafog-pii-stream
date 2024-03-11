import streamlit as st
import json
from kafka import KafkaProducer
import uuid

producer = KafkaProducer(
    bootstrap_servers=["redpanda-1:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

st.title("Customer Support Ticket")
name = st.text_input("Your name")
requesttype = st.selectbox(
    "What can we help you with today?",
    ["General Question", "Request a Feature", "Report a Bug", "Other"],
)
priority = st.number_input("Priority of request", min_value=1, max_value=5, value=5)
comment = st.text_input("What would you like to tell us?")


if st.button("Submit"):
    unique_id = str(uuid.uuid4())

    data = {
        "name": name,
        "request": requesttype,
        "priority": priority,
        "comment": comment,
        "request_id": unique_id,
    }

    producer.send("tickets", value=data)
    st.write(f"Request ID: {unique_id}")
