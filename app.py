import streamlit as st

# st.header("welcome to my app", anchor=False)
# st.title("Hello, Streamlit!")
# st.write("Welcome to your first Streamlit app.")

# name = st.text_input("Enter your name:")
# st.write(f"Hello, {name}!")
# checkbox = st.checkbox("show greeting")
# radio = st.radio("choose a greeting style", ("Formal", "Informal"))
# date = st.date_input("Select a date:")
# color = st.color_picker("Pick a color: #00f900")
# image = st.file_uploader("upload an image", type=["png", "jpg", "jpeg"])
# select =st.select_slider("select", ("junior", "mid", "senior"))

# image = st.image("https://streamlit.io/images/brand/streamlit-mark-color.png",  caption="Streamlit Logo", use_column_width=None)
# audio = st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
# video = st.video("https://www.youtube.com/watch?v=JwSS70SZdyM")
# st.markdown("This is a **markdown** text with _italic_ and **bold** formatting.")
# st.sidebar.title("Side Menu")
# name = st.sidebar.text_input("Enter your name: ")
# st.sidebar.write(f"My name is {name}")

first, second = st.columns(2)

with first:
    name = st.text_area("Enter your name:")
    st.write(f"Hello, {name}!")

with second:
    audio = st.audio_input("Upload an audio file:", type=["mp3", "wav"])
    chat = st.chat_input("Type your message here...")
    