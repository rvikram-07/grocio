"""Order Management Module for Grocio — Smart Grocery Booking System.

Handles order ID generation, order creation, order persistence to local JSON,
retrieval, and rendering of the Order Confirmation view.
"""

import os
import json
import random
import time
from datetime import datetime
import streamlit as st

ORDERS_DATA_FILE = os.path.join("data", "orders.json")
LOGO_PATH = os.path.join("assets", "grocio_logo.jpg")


def _ensure_data_dir() -> None:
    """Ensure data directory exists."""
    os.makedirs(os.path.dirname(ORDERS_DATA_FILE), exist_ok=True)


def generate_order_id() -> str:
    """Generate a unique, human-friendly order identifier.
    
    Format: GRC-<5-digit number>
    """
    random_num = random.randint(10000, 99999)
    return f"GRC-{random_num}"


def get_all_orders() -> list:
    """Safely load all completed orders from the local JSON file."""
    _ensure_data_dir()
    if not os.path.exists(ORDERS_DATA_FILE):
        return []
    try:
        with open(ORDERS_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def get_order_by_id(order_id: str) -> dict | None:
    """Retrieve an order record by its unique ID."""
    orders = get_all_orders()
    for o in orders:
        if o.get("order_id") == order_id:
            return o
    return None


def create_order(
    customer_info: dict,
    items: list,
    calculation_totals: dict,
    delivery_option: str,
    payment_method: str,
) -> dict:
    """Create and persist a new order record into local JSON storage.
    
    Never stores sensitive payment details.
    """
    _ensure_data_dir()
    order_id = generate_order_id()
    
    # Delivery estimate calculation
    is_express = "Express" in delivery_option
    est_time = "15–25 minutes" if is_express else "30–45 minutes"
    
    # Simulated payment status
    if "Cash" in payment_method:
        pay_status = "Due on Delivery (Cash / UPI)"
    else:
        pay_status = "Paid (Simulated Online)"

    order_record = {
        "order_id": order_id,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "epoch_time": int(time.time()),
        "customer": {
            "name": customer_info.get("name", "").strip(),
            "mobile": customer_info.get("mobile", "").strip(),
            "address": customer_info.get("address", "").strip(),
            "city": customer_info.get("city", "").strip(),
            "state": customer_info.get("state", "").strip(),
            "pincode": customer_info.get("pincode", "").strip(),
        },
        "delivery_option": delivery_option,
        "estimated_delivery": est_time,
        "payment_method": payment_method,
        "payment_status": pay_status,
        "order_status": "Confirmed",
        "items": items,
        "subtotal": float(calculation_totals.get("subtotal", 0.0)),
        "discount": float(calculation_totals.get("discount", 0.0)),
        "product_savings": float(calculation_totals.get("product_savings", 0.0)),
        "delivery_charge": float(calculation_totals.get("delivery_charge", 0.0)),
        "final_total": float(calculation_totals.get("final_total", 0.0)),
    }

    # Persist safely
    existing_orders = get_all_orders()
    existing_orders.insert(0, order_record)
    
    try:
        with open(ORDERS_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_orders, f, indent=2, ensure_ascii=False)
    except OSError as e:
        st.error(f"Error saving order record: {e}")

    # Save to session state as active latest order
    st.session_state.latest_order = order_record
    return order_record


def render_order_confirmation_page() -> None:
    """Render the polished order confirmation screen."""
    latest = st.session_state.get("latest_order")
    
    if not latest:
        with st.container(border=True):
            st.warning("No recent order found in this session.")
            st.write("You can browse groceries and place a new order anytime.")
            if st.button("Browse Shop", key="conf_goto_shop_empty", type="primary"):
                st.session_state.current_page = "Shop"
                st.rerun()
        return

    # Header with Grocio logo if available
    col_logo, col_heading = st.columns([1, 4])
    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width="stretch")
        else:
            st.write("🛒 **GROCIO**")
    with col_heading:
        st.title("ORDER CONFIRMED")
        st.caption("Your grocery booking has been placed and scheduled for delivery!")

    st.success("🎉 **Success!** Your grocery basket has been packed and handed over to our delivery partner.")

    # Top summary metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Order ID", value=latest["order_id"])
    with m2:
        st.metric(label="Estimated Delivery", value=latest["estimated_delivery"])
    with m3:
        st.metric(label="Payment Status", value=latest["payment_method"].split()[0])
    with m4:
        st.metric(label="Total Amount", value=f"₹{latest['final_total']:.2f}")

    st.divider()

    # Two column layout: Delivery & Payment Details / Ordered Items
    left_col, right_col = st.columns([1.1, 1.4])

    with left_col:
        with st.container(border=True):
            st.subheader("📍 Delivery Details")
            st.write(f"**Customer Name:** {latest['customer']['name']}")
            st.write(f"**Mobile Contact:** +91 {latest['customer']['mobile']}")
            st.write(f"**Delivery Address:** {latest['customer']['address']}")
            st.write(f"**City & State:** {latest['customer']['city']}, {latest['customer']['state']}")
            st.write(f"**Pincode:** {latest['customer']['pincode']}")

        with st.container(border=True):
            st.subheader("💳 Payment & Logistics")
            st.write(f"**Selected Mode:** {latest['delivery_option']}")
            st.write(f"**Payment Method:** {latest['payment_method']}")
            st.write(f"**Status:** {latest['payment_status']}")
            st.write(f"**Order Placed At:** {latest['timestamp']}")
            
            if "Cash" in latest["payment_method"]:
                st.info("💵 Please keep exact cash or UPI QR scanner ready upon delivery.")
            else:
                st.info("🔒 Simulated online transaction completed successfully.")

    with right_col:
        with st.container(border=True):
            st.subheader("🛍️ Ordered Items")
            
            items = latest.get("items", [])
            for idx, item in enumerate(items):
                i_col1, i_col2, i_col3 = st.columns([3, 1, 1.5])
                with i_col1:
                    st.write(f"**{item.get('name', 'Product')}**")
                    st.caption(f"{item.get('unit', '')} • ₹{item.get('price', 0):.2f} each")
                with i_col2:
                    st.write(f"Qty: **{item.get('quantity', 1)}**")
                with i_col3:
                    st.write(f"₹{item.get('line_total', 0.0):.2f}")
                if idx < len(items) - 1:
                    st.divider()

            st.divider()
            
            # Bill Breakdown
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.write("Item Subtotal:")
                if latest.get("discount", 0) > 0:
                    st.write("Special Discount:")
                st.write("Delivery Fee:")
                st.write("### Total Paid:")
            with s_col2:
                st.write(f"₹{latest.get('subtotal', 0.0):.2f}")
                if latest.get("discount", 0) > 0:
                    st.write(f"-₹{latest.get('discount', 0.0):.2f}")
                del_charge = latest.get("delivery_charge", 0.0)
                st.write("FREE" if del_charge == 0 else f"₹{del_charge:.2f}")
                st.write(f"### ₹{latest.get('final_total', 0.0):.2f}")

            if latest.get("product_savings", 0) > 0:
                st.success(f"🌱 You saved a total of ₹{latest['product_savings']:.2f} on this order!")

    st.write("")
    
    # Navigation after checkout
    b1, b2 = st.columns([1, 3])
    with b1:
        if st.button("Continue Shopping", key="continue_shopping", type="primary", use_container_width=True):
            st.session_state.current_page = "Shop"
            st.session_state.selected_category = "All"
            st.rerun()
    with b2:
        if st.button("Return to Homepage", key="conf_return_home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
