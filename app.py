import os
import tempfile

import streamlit as st

from create_database import create_database
from shopping_agent import agent


DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")


def ensure_database() -> None:
	if not os.path.exists(DB_PATH):
		create_database()


def extract_assistant_text(response: object) -> str:
	if isinstance(response, dict) and "messages" in response and response["messages"]:
		last_message = response["messages"][-1]
		if isinstance(last_message, dict):
			return last_message.get("content", "")
		return getattr(last_message, "content", str(last_message))
	return str(response)


st.set_page_config(page_title="Shopping Agent", page_icon="🛒")

st.title("Shopping Agent")
st.caption("Chat to search products and place orders.")

ensure_database()

with st.sidebar:
	st.subheader("Image search")
	uploaded_image = st.file_uploader("Upload a product image", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
	st.session_state.messages = [
		{
			"role": "assistant",
			"content": (
				"Hi! Tell me what you want to buy, including any price, rating, or organic filters."
			),
		}
	]

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.write(message["content"])

prompt = st.chat_input("What are you shopping for?")

if uploaded_image and not prompt:
	suffix = os.path.splitext(uploaded_image.name)[1] or ".jpg"
	with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
		temp_file.write(uploaded_image.getbuffer())
		image_path = temp_file.name
	prompt = f"Image path: {image_path}"

if prompt:
	st.session_state.messages.append({"role": "user", "content": prompt})
	with st.chat_message("user"):
		st.write(prompt)

	with st.chat_message("assistant"):
		with st.spinner("Thinking..."):
			response = agent.invoke(
				{
					"messages": st.session_state.messages,
				}
			)
			assistant_text = extract_assistant_text(response)
			st.write(assistant_text)

	st.session_state.messages.append(
		{"role": "assistant", "content": assistant_text}
	)
