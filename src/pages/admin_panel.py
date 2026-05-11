from __future__ import annotations
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth.password_utils import create_password_hash
from src.content.translations import t
from src.database.users_repo import (
    admin_update_user,
    count_admins,
    count_users,
    delete_user,
    get_user_by_id,
    list_users,
    update_password,
)
from src.database.predictions_repo import (
    delete_prediction,
    delete_user_predictions,
    get_all_predictions,
    get_stats,
    to_dataframe,
)
from src.database.notifications_repo import add_broadcast_notification, add_notification
from src.ui.layout import page_header, metric_card, section_title, card
from src.utils.formatting import title_crop


def _admin_only(user: dict, language: str = "English") -> bool:
    if user["role"] != "admin":
        page_header("Access Restricted", "This page is only available to administrator accounts.", "admin", "Admin security")
        st.error("Admin access only.")
        return False
    return True


def render(user: dict, language: str) -> None:
    render_overview(user, language)


def render_overview(user: dict, language: str) -> None:
    if not _admin_only(user, language):
        return

    page_header(t(language, "admin_title"), t(language, "admin_subtitle"), "admin", t(language, "admin_workspace"))

    stats = get_stats()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(t(language, "total_users"), str(count_users()), "👥")
    with c2:
        metric_card(t(language, "total_predictions"), str(stats["total"]), "🌾")
    with c3:
        metric_card(t(language, "active_users"), str(stats.get("active_users", 0)), "🧑‍🌾")
    with c4:
        metric_card(t(language, "avg_confidence"), f"{stats['average_confidence'] * 100:.2f}%", "📈")

    section_title(t(language, "system_overview"), t(language, "system_overview_subtitle"))
    left, right = st.columns([1, 1])
    with left:
        if stats["top_crops"]:
            crop_df = pd.DataFrame(stats["top_crops"])
            crop_df["recommended_crop"] = crop_df["recommended_crop"].map(title_crop)
            st.plotly_chart(
                px.bar(crop_df, x="recommended_crop", y="count", title="Most Recommended Crops"),
                use_container_width=True,
            )
        else:
            card(t(language, "no_crop_trend"), t(language, "no_crop_trend_body"), "📊")
    with right:
        if stats["mode_usage"]:
            mode_df = pd.DataFrame(stats["mode_usage"])
            st.plotly_chart(
                px.pie(mode_df, names="mode", values="count", title="Basic vs Advanced Mode Usage"),
                use_container_width=True,
            )
        else:
            card(t(language, "no_mode_usage"), t(language, "no_mode_usage_body"), "🧪")

    section_title(t(language, "admin_notice"), t(language, "admin_notice_subtitle"))
    with st.form("admin_broadcast_form"):
        title = st.text_input(t(language, "notice_title"), placeholder="Example: Use Advanced Mode for more reliable predictions")
        message = st.text_area(t(language, "notice_message"), placeholder="Write a short announcement or reminder for users.")
        ntype = st.selectbox(t(language, "type"), ["info", "success", "warning", "error"])
        submitted = st.form_submit_button(t(language, "send_broadcast"), type="primary", use_container_width=True)
    if submitted:
        if title.strip() and message.strip():
            total = add_broadcast_notification(title, message, ntype)
            st.success(f"Broadcast notice created for {total} user(s).")
        else:
            st.error("Please enter both title and message.")


def render_user_management(user: dict, language: str) -> None:
    if not _admin_only(user, language):
        return

    page_header(t(language, "user_management_title"), t(language, "user_management_subtitle"), "users", "Admin control")

    users = list_users()
    if not users:
        st.markdown("<div class='empty-state'>No users found.</div>", unsafe_allow_html=True)
        return

    display = pd.DataFrame(users)
    st.dataframe(display, use_container_width=True, hide_index=True)

    section_title("Edit User", "Update account details or reset a user password. Password hashes are never shown to the admin.")
    user_options = {f"{u['username']} — {u['email']} (ID {u['id']})": u["id"] for u in users}
    selected_label = st.selectbox(t(language, "select_user"), list(user_options.keys()), key="admin_edit_user_select")
    selected_id = user_options[selected_label]
    selected_user = get_user_by_id(selected_id)

    if selected_user:
        with st.form("admin_edit_user_form"):
            full_name = st.text_input(t(language, "full_name"), value=selected_user["full_name"])
            username = st.text_input(t(language, "username"), value=selected_user["username"])
            email = st.text_input(t(language, "email"), value=selected_user["email"])
            role_index = 1 if selected_user["role"] == "admin" else 0
            role = st.selectbox(t(language, "role"), ["user", "admin"], index=role_index)
            preferred_language = st.selectbox(
                t(language, "preferred_language"),
                ["English", "Bahasa Melayu"],
                index=0 if selected_user.get("preferred_language") == "English" else 1,
            )
            new_password = st.text_input("Admin Password Reset (optional)", type="password", placeholder="Leave blank to keep current password")
            submitted = st.form_submit_button("Save User Changes", type="primary", use_container_width=True)

        if submitted:
            if selected_user["id"] == user["id"] and role != "admin":
                st.error("You cannot remove your own admin role while logged in.")
            elif selected_user["role"] == "admin" and role != "admin" and count_admins() <= 1:
                st.error("At least one admin account must remain in the system.")
            else:
                try:
                    admin_update_user(selected_user["id"], full_name, username, email, role, preferred_language)
                    if new_password:
                        if len(new_password) < 6:
                            st.error("New password must be at least 6 characters long.")
                            return
                        pw_hash, salt = create_password_hash(new_password)
                        update_password(selected_user["id"], pw_hash, salt)
                    add_notification(selected_user["id"], "Account updated", "An administrator updated your account details.", "info")
                    st.success("User account updated successfully.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(t(language, "username_email_exists"))

    section_title("Delete User", "Deleting a user also removes their prediction history because the database uses cascade delete.")
    delete_label = st.selectbox(t(language, "select_user_delete"), list(user_options.keys()), key="admin_delete_user_select")
    delete_id = user_options[delete_label]
    delete_target = get_user_by_id(delete_id)
    if delete_target:
        if delete_id == user["id"]:
            st.markdown(f"<div class='empty-state'>{t(language, 'cannot_delete_own_admin')}</div>", unsafe_allow_html=True)
        elif delete_target["role"] == "admin" and count_admins() <= 1:
            st.warning("This is the only admin account, so it cannot be deleted.")
        else:
            st.warning(f"You are about to delete: {delete_target['username']} ({delete_target['email']}).")
            confirm = st.text_input("Type the username to confirm deletion", key="confirm_delete_user")
            if st.button("Delete Selected User", type="primary", use_container_width=True):
                if confirm.strip().lower() == delete_target["username"].lower():
                    delete_user(delete_id)
                    st.success("User deleted successfully.")
                    st.rerun()
                else:
                    st.error("Confirmation username does not match.")


def render_prediction_logs(user: dict, language: str) -> None:
    if not _admin_only(user, language):
        return

    page_header(t(language, "prediction_logs_title"), t(language, "prediction_logs_subtitle"), "logs", "Privacy-controlled records")

    rows = get_all_predictions()
    if not rows:
        st.markdown(f"<div class='empty-state'>{t(language, 'no_prediction_logs')}</div>", unsafe_allow_html=True)
        return

    df = to_dataframe(rows)
    df["recommended_crop_title"] = df["recommended_crop"].map(title_crop)

    c1, c2, c3 = st.columns(3)
    usernames = ["All"] + sorted(df["username"].dropna().unique().tolist())
    modes = ["All"] + sorted(df["mode"].dropna().unique().tolist())
    crops = ["All"] + sorted(df["recommended_crop_title"].dropna().unique().tolist())
    selected_user = c1.selectbox("Filter by User", usernames)
    selected_mode = c2.selectbox("Filter by Mode", modes)
    selected_crop = c3.selectbox("Filter by Crop", crops)

    filtered = df.copy()
    if selected_user != "All":
        filtered = filtered[filtered["username"] == selected_user]
    if selected_mode != "All":
        filtered = filtered[filtered["mode"] == selected_mode]
    if selected_crop != "All":
        filtered = filtered[filtered["recommended_crop_title"] == selected_crop]

    view_cols = [
        "id", "created_at", "username", "email", "mode", "recommended_crop_title",
        "confidence_level", "confidence_percent", "N", "P", "K", "temperature", "humidity", "ph", "rainfall",
    ]
    st.dataframe(
        filtered[view_cols].rename(
            columns={
                "id": "Log ID", "created_at": "Date/Time", "username": "Username", "email": "Email",
                "mode": "Mode", "recommended_crop_title": "Recommended Crop", "confidence_level": "Confidence Level",
                "confidence_percent": "Confidence (%)", "temperature": "Temperature", "humidity": "Humidity",
                "ph": "pH", "rainfall": "Rainfall",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Logs CSV", csv, "admin_prediction_logs.csv", "text/csv", use_container_width=True)

    section_title("Delete Prediction Log", "Use this only for incorrect demo records or testing cleanup.")
    log_ids = filtered["id"].astype(int).tolist()
    if log_ids:
        selected_log_id = st.selectbox("Select Log ID", log_ids)
        confirm = st.checkbox("I understand this will permanently delete this prediction record.")
        if st.button("Delete Selected Prediction Log", type="primary", use_container_width=True):
            if confirm:
                delete_prediction(int(selected_log_id))
                st.success("Prediction log deleted.")
                st.rerun()
            else:
                st.error("Please tick the confirmation checkbox first.")

    section_title("Clear User Prediction History", "This removes all saved prediction records for one selected user without deleting the account.")
    users = list_users()
    user_options = {f"{u['username']} — {u['email']} (ID {u['id']})": u["id"] for u in users}
    selected_user_label = st.selectbox(t(language, "select_user"), list(user_options.keys()), key="clear_history_user_select")
    clear_user_id = user_options[selected_user_label]
    clear_confirm = st.checkbox("I understand this will delete all prediction history for the selected user.", key="clear_user_history_confirm")
    if st.button("Clear Selected User History", use_container_width=True):
        if clear_confirm:
            delete_user_predictions(clear_user_id)
            st.success("Selected user's prediction history was cleared.")
            st.rerun()
        else:
            st.error("Please tick the confirmation checkbox first.")
