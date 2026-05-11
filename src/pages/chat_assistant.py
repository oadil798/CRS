from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.content.assistant_knowledge import answer_question
from src.ui.layout import page_header, card, section_title


def render(user: dict, language: str) -> None:
    page_header(t(language, "chat_title"), t(language, "chat_subtitle"), "chat", t(language, "built_in_guidance"))

    c1, c2, c3 = st.columns(3)
    with c1:
        card(t(language, "ask_inputs"), t(language, "ask_inputs_body"), "🧪")
    with c2:
        card(t(language, "ask_modes"), t(language, "ask_modes_body"), "🌤️")
    with c3:
        card(t(language, "ask_confidence"), t(language, "ask_confidence_body"), "📈")

    section_title(t(language, "assistant_chat"), t(language, "assistant_chat_subtitle"))
    if "chat_messages" not in st.session_state or st.session_state.get("chat_language") != language:
        st.session_state.chat_language = language
        st.session_state.chat_messages = [
            {"role": "assistant", "content": t(language, "assistant_greeting")}
        ]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input(t(language, "chat_placeholder"))
    if question:
        st.session_state.chat_messages.append({"role": "user", "content": question})
        answer = answer_question(question, language)
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})
        st.rerun()
