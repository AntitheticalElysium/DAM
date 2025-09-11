import streamlit as st
import requests
import PyPDF2

st.set_page_config(page_title="🐐 GOAT Text Summarizer", layout="wide")
st.title("🐐 GOAT Text Summarizer")
st.write("Paste text or upload a TXT/PDF document to get an AI-powered summary!")

if 'history' not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([3, 1])

with col1:
    text = st.text_area("Enter your text here", height=250)

    if st.button("Summarize"):
        if text.strip() == "":
            st.warning("Please enter some text or upload a file!")
        else:
            with st.spinner("Summarizing..."):
                try:
                    response = requests.post(
                        "http://localhost:8888/summarize",
                        json={"text": text}
                    )
                    response.raise_for_status()
                    summary = response.json()["summary"]

                    st.markdown(
                        f'''
                        <div style="background-color:#22223b; color:#f8f8f2; padding:15px; border-radius:10px;">
                        {summary}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

                    st.session_state.history.append({"input": text, "summary": summary})

                except Exception as e:
                    st.error(f"Error calling API: {e}")

with col2:
    st.subheader("Upload a file")
    uploaded_file = st.file_uploader("TXT or PDF", type=["txt", "pdf"])
    if uploaded_file is not None:
        raw_text = ""
        if uploaded_file.type == "application/pdf":
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    raw_text += page_text
        else:
            raw_text = uploaded_file.read().decode("utf-8")

        st.write("Preview:")
        st.text_area("File content", value=raw_text[:500], height=200)

        if st.button("Summarize File"):
            if raw_text.strip() == "":
                st.warning("Uploaded file is empty!")
            else:
                with st.spinner("Summarizing file..."):
                    try:
                        response = requests.post(
                            "http://localhost:8888/summarize",
                            json={"text": raw_text}
                        )
                        response.raise_for_status()
                        summary = response.json()["summary"]

                        st.markdown(
                            f'''
                            <div style="background-color:#22223b; color:#f8f8f2; padding:15px; border-radius:10px;">
                            {summary}
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )

                        st.session_state.history.append({"input": raw_text, "summary": summary})

                    except Exception as e:
                        st.error(f"Error calling API: {e}")

if st.session_state.history:
    st.subheader("📝 Previous summaries")
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Summary #{i}"):
            st.markdown(f"**Input (first 200 chars):** {entry['input'][:200]}...")
            st.markdown(f"**Summary:** {entry['summary']}")

