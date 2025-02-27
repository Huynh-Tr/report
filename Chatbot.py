import google.generativeai as genai
# gg_key = r"AIzaSyALfue942SkEWGJPG6P8GZGgm7Bnkevd7Q"
genai.configure(api_key=st.secrets["gg_key"])
import re
import streamlit as st
import PIL.Image
import time


# if "chat" not in st.session_state:
#     st.session_state.chat = []
if "history" not in st.session_state:
    st.session_state.history = []
col1, col2, col3 = st.columns(3)
col1.button("reset", on_click=(st.session_state.history.clear))

# uploaded_file = col2.file_uploader("Upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed", accept_multiple_files=False)
# if uploaded_file is not None:
#     image = PIL.Image.open(uploaded_file)
#     col2.image(image, width=200)

uploaded_file = col2.file_uploader("Upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed", accept_multiple_files=True)
if uploaded_file:
    images = [PIL.Image.open(file) for file in uploaded_file]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    combined_image = PIL.Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        combined_image.paste(im, (x_offset, 0))
        x_offset += im.width

    col2.image(combined_image, width=200)



# image
st.title("ChatBot")
model = genai.GenerativeModel(
    'gemini-2.0-flash', 
    system_instruction=[f"ngoài sử dụng thông tin của model và sau đó là sử dụng thông tin {st.session_state.history} để trả lời các câu hỏi tiếp theo"]
)
chat = model.start_chat(history=[])

for his in st.session_state.history:
    with st.chat_message(his["role"]):
        st.markdown(his["content"])

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

st.session_state.chat = chat
if prompt := st.chat_input("What is up?"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if len(uploaded_file) > 0:
            response = chat.send_message([prompt, combined_image])
        else:
            response = chat.send_message(prompt)

        st.write_stream(stream_data(response.text))
    st.session_state.history.append({"role": "assistant", "content": response.text})

# st.session_state
# 
