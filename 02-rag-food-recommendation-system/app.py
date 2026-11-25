
import streamlit as st
from src.rag_pipeline import rag_pipeline


def main():
    st.set_page_config(
        page_title="FOOD RECOMMENDATION SYSTEM",
        page_icon="🍽️",
        layout="centered"
    )

    st.title("🍽️ Food Recommendation Assistant")
    st.caption("Find food recommendations using your preferences.")

    # Sidebar filters
    st.sidebar.header("Food Preferences")

    top_k = st.sidebar.slider(
        "Number of recommendations to retrieve",
        min_value=1,
        max_value=10,
        value=3
    )

    use_cuisine = st.sidebar.checkbox("Filter by cuisine")
    cuisine = None

    if use_cuisine:
        cuisine = st.sidebar.text_input(
            "Choose your preferred cuisine",
            placeholder="e.g. Indian"
        ).strip() or None

    use_calories = st.sidebar.checkbox("Filter by max calories")
    max_calories = None

    if use_calories:
        max_calories = st.sidebar.number_input(
            "Maximum calories per serving",
            min_value=1,
            max_value=2000,
            value=500,
            step=50
        )

    use_dietary = st.sidebar.checkbox("Filter by dietary preference")
    dietary_type = None

    if use_dietary:
        dietary_type = st.sidebar.selectbox(
            "Choose dietary preference",
            ["vegetarian", "non_vegetarian"]
        )

    active_filters = []

    if cuisine:
        active_filters.append(f"Cuisine: {cuisine}")

    if max_calories is not None:
        active_filters.append(f"Max calories:{max_calories}")

    if dietary_type:
        active_filters.append(f"Dietary: {dietary_type}")

    if active_filters:
        st.caption("|".join(active_filters))
    else:
        st.caption("No additional food filters applied.")

    with st.expander("About nutritional information"):
        st.write(
            "Food details and nutritional values are based on the "
            "provided dataset. Actual nutritional values may vary "
            "depending on ingredients, portion sizes, and preparation.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Clear conversation
    if st.sidebar.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user query
    query = st.chat_input("What would you like to eat today?")

    if query:
        st.session_state.messages.append(
            {"role": "user", "content": query}
        )

        with st.chat_message("user"):
            st.markdown(query)

        # Generate recommendation
        with st.chat_message("assistant"):
            with st.spinner("Finding recommended foods..."):
                try:
                    answer = rag_pipeline(
                        query=query,
                        top_k=top_k,
                        cuisine=cuisine,
                        max_calories=max_calories,
                        dietary_type=dietary_type
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as error:
                    st.error(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()
