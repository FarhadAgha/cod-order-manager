import streamlit as st
from database import add_order, get_order_by_id_and_phone

def show_customer_view():
    st.title("📦 Place Your Order")
    st.caption("Leather Wallets — Cash on Delivery")

    tab1, tab2 = st.tabs(["🛒 Place an Order", "🔍 Check My Order Status"])

    # ---------------- Place an Order ----------------
    with tab1:
        with st.form("customer_order_form", clear_on_submit=True):
            customer_name = st.text_input("Your Name")
            phone = st.text_input("Phone Number")
            address = st.text_area("Delivery Address")
            product = st.text_input("Which wallet would you like?")
            price = st.number_input("Price (PKR)", min_value=0.0, step=50.0)
            notes = st.text_area("Any notes? (optional)")

            submitted = st.form_submit_button("Place Order")

            if submitted:
                if customer_name and phone and address and product:
                    new_id = add_order(customer_name, phone, address, product, price, notes)
                    st.success(f"✅ Order placed! Your Order ID is: **ORD-{new_id}**")
                    st.info("Please save this Order ID and your phone number — you'll need both to check your order status later.")
                else:
                    st.error("Please fill in all required fields (Name, Phone, Address, Product).")

    # ---------------- Check Order Status ----------------
    with tab2:
        st.write("Enter your Order ID and phone number to check your order status.")

        order_id_input = st.text_input("Order ID (e.g. ORD-1023)", key="check_order_id")
        phone_input = st.text_input("Phone Number used when ordering", key="check_phone")

        if st.button("Check Status"):
            try:
                clean_id = order_id_input.upper().replace("ORD-", "").strip()
                order_id = int(clean_id)
                order = get_order_by_id_and_phone(order_id, phone_input.strip())

                if order:
                    st.success(f"Order found!")
                    st.write(f"**Product:** {order['product']}")
                    st.write(f"**Price:** PKR {order['price']}")
                    st.write(f"**Status:** {order['status']}")

                    status_steps = ["Pending", "Confirmed", "Shipped", "Delivered"]
                    if order['status'] in status_steps:
                        st.progress(
                            (status_steps.index(order['status']) + 1) / len(status_steps)
                        )
                else:
                    st.error("No matching order found. Please check your Order ID and phone number.")
            except ValueError:
                st.error("Please enter a valid Order ID (e.g. ORD-1023).")