"""Checkout Module for Grocio — Smart Grocery Booking System.

Handles delivery address collection, strict Indian contact validation,
delivery options, simulated payment modes, order submission, and handoff to orders.py.
"""

import re
import time
import streamlit as st
import cart
import orders

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi NCR", "Chandigarh"
]


def render_checkout_page() -> None:
    """Render the full Checkout workflow with validation and simulated payment."""
    totals = cart.calculate_cart_totals()

    # Verify that the cart is not empty
    if not totals["items"]:
        with st.container(border=True):
            st.warning("🛒 Your cart is currently empty. Please add items before checking out.")
            if st.button("Return to Shop", key="chk_empty_shop_btn", type="primary"):
                st.session_state.current_page = "Shop"
                st.rerun()
        return

    st.title("Checkout")
    st.caption("Provide your delivery address and choose a simulated payment method.")

    # Two-column layout: Form (left) and Order Summary (right)
    col_form, col_summary = st.columns([1.6, 1.2])

    with col_form:
        st.subheader("1. Delivery Information")
        with st.container(border=True):
            c_name, c_mobile = st.columns(2)
            with c_name:
                cust_name = st.text_input(
                    "Full Name *",
                    value=st.session_state.get("customer_name", ""),
                    placeholder="e.g. Rahul Sharma",
                    key="customer_name"
                )
            with c_mobile:
                cust_mobile = st.text_input(
                    "Mobile Number (10 Digits) *",
                    value=st.session_state.get("customer_mobile", ""),
                    placeholder="e.g. 9876543210",
                    max_chars=10,
                    key="customer_mobile"
                )

            c_hno, c_street = st.columns([1, 2])
            with c_hno:
                cust_hno = st.text_input(
                    "House / Flat No. *",
                    value=st.session_state.get("customer_hno", ""),
                    placeholder="e.g. Flat 402, Block B",
                    key="customer_hno"
                )
            with c_street:
                cust_street = st.text_input(
                    "Street / Area / Landmark *",
                    value=st.session_state.get("customer_street", ""),
                    placeholder="e.g. Green Glen Layout, Bellandur",
                    key="customer_street"
                )

            c_city, c_state, c_pin = st.columns([1.2, 1.2, 1])
            with c_city:
                cust_city = st.text_input(
                    "City *",
                    value=st.session_state.get("customer_city", "Bengaluru"),
                    placeholder="e.g. Bengaluru",
                    key="customer_city"
                )
            with c_state:
                default_state_idx = INDIAN_STATES.index("Karnataka") if "Karnataka" in INDIAN_STATES else 0
                cust_state = st.selectbox(
                    "State *",
                    INDIAN_STATES,
                    index=default_state_idx,
                    key="customer_state"
                )
            with c_pin:
                cust_pin = st.text_input(
                    "Pincode (6 Digits) *",
                    value=st.session_state.get("customer_pincode", ""),
                    placeholder="e.g. 560103",
                    max_chars=6,
                    key="customer_pincode"
                )

        st.write("")
        st.subheader("2. Delivery Options")
        with st.container(border=True):
            deliv_choice = st.radio(
                "Select preferred delivery speed:",
                options=[
                    "Express Delivery (Estimated: 15–25 minutes)",
                    "Standard Delivery (Estimated: 30–45 minutes)"
                ],
                index=0,
                key="delivery_option"
            )
            if "Express" in deliv_choice:
                st.caption("⚡ **Express Local Slot:** Priority dispatch from your nearest Grocio dark store.")
            else:
                st.caption("🚚 **Standard Green Slot:** Eco-friendly batched neighbourhood delivery.")

        st.write("")
        st.subheader("3. Payment Method (Simulated)")
        with st.container(border=True):
            pay_method = st.radio(
                "Select simulated payment mode:",
                options=["UPI", "Credit / Debit Card", "Cash on Delivery"],
                index=0,
                key="payment_method"
            )

            st.write("")
            # Dynamic fields for selected payment method
            upi_id_val = ""
            card_holder_val = ""
            card_number_val = ""
            
            if pay_method == "UPI":
                st.info("📲 **Simulated UPI Flow:** Enter any mock UPI VPA ID (e.g. name@upi or mobile@okhdfcbank).")
                upi_id_val = st.text_input(
                    "UPI Virtual Payment Address (VPA) *",
                    value=st.session_state.get("sim_upi_vpa", "customer@okhdfcbank"),
                    placeholder="username@okhdfcbank",
                    key="sim_upi_vpa"
                )
            
            elif pay_method == "Credit / Debit Card":
                st.info("💳 **Simulated Card Flow:** Enter dummy card details. No real charge is made.")
                c_cname, c_cnum = st.columns(2)
                with c_cname:
                    card_holder_val = st.text_input("Cardholder Name *", value=st.session_state.get("sim_card_holder", "Rahul Sharma"), placeholder="Name as on card", key="sim_card_holder")
                with c_cnum:
                    card_number_val = st.text_input("Card Number (16 Digits) *", value=st.session_state.get("sim_card_num", "4532 0150 0000 1234"), placeholder="4532 0150 0000 1234", max_chars=19, key="sim_card_num")
                
                c_exp, c_cvv = st.columns(2)
                with c_exp:
                    st.text_input("Expiry (MM/YY)", value=st.session_state.get("sim_card_exp", "12/28"), placeholder="12/28", max_chars=5, key="sim_card_exp")
                with c_cvv:
                    st.text_input("CVV", value=st.session_state.get("sim_card_cvv", "821"), placeholder="•••", max_chars=3, type="password", key="sim_card_cvv")

            elif pay_method == "Cash on Delivery":
                st.info("💵 **Cash / QR on Delivery:** Pay ₹{:.2f} using cash or UPI QR scanner when the delivery partner arrives.".format(totals["final_total"]))

            st.caption("⚠️ **Notice:** This application is for demonstration purposes. No real banking or payment gateways are accessed.")

    # Right column: Order Summary & Place Order Action
    with col_summary:
        with st.container(border=True):
            st.subheader("Order Summary")

            # Items breakdown list
            for item in totals["items"]:
                r_col1, r_col2 = st.columns([2.5, 1])
                with r_col1:
                    st.write(f"**{item['name']}** × {item['quantity']}")
                    st.caption(f"{item['unit']} • ₹{item['price']:.2f}")
                with r_col2:
                    st.write(f"₹{item['line_total']:.2f}")

            st.divider()

            # Totals
            b_l1, b_r1 = st.columns(2)
            with b_l1:
                st.write("Subtotal:")
            with b_r1:
                st.write(f"₹{totals['subtotal']:.2f}")

            if totals["discount"] > 0:
                b_l2, b_r2 = st.columns(2)
                with b_l2:
                    st.write("Coupon Discount:")
                with b_r2:
                    st.write(f"-₹{totals['discount']:.2f}")

            b_l3, b_r3 = st.columns(2)
            with b_l3:
                st.write("Delivery Charge:")
            with b_r3:
                st.write("FREE" if totals["delivery_charge"] == 0 else f"₹{totals['delivery_charge']:.2f}")

            st.divider()
            b_l4, b_r4 = st.columns(2)
            with b_l4:
                st.write("### Total Payable:")
            with b_r4:
                st.write(f"### ₹{totals['final_total']:.2f}")

            if totals["product_savings"] > 0:
                st.success(f"🌱 Total Savings: ₹{totals['product_savings']:.2f}")

            st.write("")
            st.write(f"**Delivery Mode:** {deliv_choice.split('(')[0].strip()}")
            st.write(f"**Payment:** {pay_method}")

            st.write("")
            place_order_clicked = st.button(
                "Place Order (Confirm Booking) →",
                key="place_order",
                type="primary",
                use_container_width=True
            )

            if st.button("← Modify Cart", key="chk_modify_cart_btn", use_container_width=True):
                st.session_state.current_page = "Cart"
                st.rerun()

            # Form submission and validation handling
            if place_order_clicked:
                # Validation checks
                errors = []

                if not cust_name.strip():
                    errors.append("Please enter your full name.")
                
                # Indian 10-digit mobile number validation
                clean_mobile = re.sub(r"\D", "", cust_mobile.strip())
                if not re.match(r"^[6-9]\d{9}$", clean_mobile):
                    errors.append("Please enter a valid 10-digit Indian mobile number (e.g. 9876543210).")

                if not cust_hno.strip():
                    errors.append("Please enter your house or flat number.")

                if not cust_street.strip():
                    errors.append("Please enter your street or area details.")

                if not cust_city.strip():
                    errors.append("Please enter your city.")

                # 6-digit Indian pincode validation
                clean_pin = cust_pin.strip()
                if not re.match(r"^\d{6}$", clean_pin):
                    errors.append("Please enter a valid 6-digit Indian pincode (e.g. 560103).")

                # Payment method validation
                if pay_method == "UPI":
                    if not upi_id_val.strip() or "@" not in upi_id_val:
                        errors.append("Please enter a valid simulated UPI ID (e.g. user@okhdfcbank).")
                elif pay_method == "Credit / Debit Card":
                    if not card_holder_val.strip():
                        errors.append("Please enter the cardholder name.")
                    clean_card = re.sub(r"\D", "", card_number_val)
                    if len(clean_card) < 15:
                        errors.append("Please enter a valid 16-digit simulated card number.")

                if errors:
                    for err in errors:
                        st.error(f"❌ {err}")
                else:
                    # Simulate order processing
                    with st.spinner("Processing simulated order and securing fresh items..."):
                        time.sleep(0.5)
                        
                        customer_data = {
                            "name": cust_name.strip(),
                            "mobile": clean_mobile,
                            "address": f"{cust_hno.strip()}, {cust_street.strip()}",
                            "city": cust_city.strip(),
                            "state": cust_state.strip(),
                            "pincode": clean_pin,
                        }

                        orders.create_order(
                            customer_info=customer_data,
                            items=totals["items"],
                            calculation_totals=totals,
                            delivery_option=deliv_choice,
                            payment_method=pay_method,
                        )

                        # Clear cart only after successful creation
                        cart.clear_cart()
                        st.session_state.applied_coupon = None

                        # Redirect to Order Confirmation
                        st.session_state.current_page = "Order Confirmation"
                        st.rerun()
