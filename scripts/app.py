import streamlit as st
import backend.recommender as rec

st.set_page_config(page_title="Research Paper Recommender")
st.title("Research Paper Recommender")

query = st.text_input("Enter a topic, keyword, or question:")

if query:
    st.subheader("Top Recommendations:")
    results = rec.recommend(query)
    for r in results:
        st.markdown(f"### [{r[0]['title']}]({r[0]['link']})")
        st.write(r[0]["summary"])
        st.caption(f"Category: {r[0]['category']} | Score: {r[1]:.4f}")
        st.markdown("---")
