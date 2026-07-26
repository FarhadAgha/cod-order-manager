import streamlit as st
from database import (
    get_all_orders, update_status,
    save_ai_message, save_risk_assessment, delete_order
)
from ai_helper import generate_message_and_risk

def show_seller_view():
    st.title("🔐 Seller Dashboard")
    st.caption("COD Order Manager — Admin View")

    orders = get_all_orders()

    if not orders:
        st.info("No orders yet.")
        return

    status_options = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]

    for order in orders:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown(f"**ORD-{order['id']} — {order['customer_name']}** — {order['product']}")
                st.write(f"📞 {order['phone']}")
                st.write(f"📍 {order['address']}")
                st.write(f"💰 PKR {order['price']}")
                if order['notes']:
                    st.caption(f"Note: {order['notes']}")

            with col2:
                new_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(order['status']) if order['status'] in status_options else 0,
                    key=f"status_{order['id']}"
                )
                if new_status != order['status']:
                    update_status(order['id'], new_status)
                    st.rerun()

                if order['risk_level']:
                    risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(order['risk_level'], "⚪")
                    st.write(f"{risk_color} Risk: **{order['risk_level']}**")
                    st.caption(order['risk_reason'])

            with col3:
                if st.button("🤖 AI: Message + Risk", key=f"ai_{order['id']}"):
                    with st.spinner("Generating..."):
                        message, risk_level, risk_reason = generate_message_and_risk(
                            order['customer_name'], order['phone'], order['address'],
                            order['product'], order['price'], order['notes']
                        )
                        save_ai_message(order['id'], message)
                        save_risk_assessment(order['id'], risk_level, risk_reason)
                        st.rerun()

                if st.button("🗑️ Delete", key=f"delete_{order['id']}"):
                    delete_order(order['id'])
                    st.rerun()

            if order['ai_message']:
                st.text_area(
                    "WhatsApp Message (copy this)",
                    value=order['ai_message'],
                    height=100,
                    key=f"msg_{order['id']}"
                )