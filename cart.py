"""Shopping Cart Module for Grocio — Smart Grocery Booking System.

Manages cart session state, item quantities, single source of truth
financial calculations, delivery charge rules, and the Cart view.
"""

import os
import streamlit as st
import products


def _init_cart() -> None:
    """Ensure cart dictionary exists in session state."""
    if "cart" not in st.session_state or not isinstance(st.session_state.cart, dict):
        st.session_state.cart = {}


def get_cart() -> dict:
    """Retrieve active session cart dictionary {product_id: quantity}."""
    _init_cart()
    return st.session_state.cart


def add_to_cart(product_id: str, quantity: int = 1) -> None:
    """Add item or increment quantity of existing item in the cart."""
    _init_cart()
    prod = products.get_product_by_id(product_id)
    if not prod:
        st.error("Cannot add: Product not found.")
        return

    if prod.get("stock") != "Available":
        st.error(f"Sorry, {prod['name']} is currently out of stock.")
        return

    current_qty = st.session_state.cart.get(product_id, 0)
    st.session_state.cart[product_id] = current_qty + quantity
    st.toast(f"🛒 Added {quantity}x {prod['name']} to cart!")


def update_cart_quantity(product_id: str, new_quantity: int) -> None:
    """Update item quantity in cart. Remove if quantity <= 0."""
    _init_cart()
    if new_quantity <= 0:
        remove_from_cart(product_id)
    else:
        st.session_state.cart[product_id] = new_quantity


def remove_from_cart(product_id: str) -> None:
    """Remove item completely from cart."""
    _init_cart()
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]
        st.toast("Item removed from cart.")


def clear_cart() -> None:
    """Empty all contents of active shopping cart."""
    st.session_state.cart = {}


def get_cart_count() -> int:
    """Calculate total units of all items in cart.
    
    Example: 2 units milk + 1 loaf bread = 3.
    """
    cart = get_cart()
    return sum(cart.values())


def calculate_cart_totals(cart_dict: dict = None, coupon_code: str = None) -> dict:
    """Single source of truth for all cart, checkout, and order calculations.
    
    Subtotal = Sum of (Product Price * Quantity)
    Product Savings = Sum of ((Original Price - Price) * Quantity)
    Delivery = FREE if Subtotal >= ₹499 else ₹20 (₹0 if cart is empty)
    Discount = ₹50 if coupon 'GROCIO50' applied and Subtotal >= ₹499
    Final Total = Subtotal - Discount + Delivery
    """
    if cart_dict is None:
        cart_dict = get_cart()

    if coupon_code is None:
        coupon_code = st.session_state.get("applied_coupon", "")

    items_list = []
    subtotal = 0.0
    product_savings = 0.0

    for pid, qty in cart_dict.items():
        if qty <= 0:
            continue
        prod = products.get_product_by_id(pid)
        if not prod:
            continue

        p_curr = float(prod.get("price", 0.0))
        p_orig = float(prod.get("original_price", p_curr))
        line_total = p_curr * qty
        line_saving = max(0.0, (p_orig - p_curr) * qty)

        subtotal += line_total
        product_savings += line_saving

        items_list.append({
            "id": pid,
            "name": prod.get("name", "Grocery Item"),
            "category": prod.get("category", "General"),
            "unit": prod.get("unit", ""),
            "price": p_curr,
            "original_price": p_orig,
            "quantity": qty,
            "line_total": line_total,
            "image": prod.get("image", ""),
        })

    # Delivery Charge Policy
    free_delivery_threshold = 499.0
    if subtotal == 0.0:
        delivery_charge = 0.0
    elif subtotal >= free_delivery_threshold:
        delivery_charge = 0.0
    else:
        delivery_charge = 20.0

    # Coupon Discount Policy
    coupon_discount = 0.0
    if coupon_code and coupon_code.strip().upper() == "GROCIO50":
        if subtotal >= free_delivery_threshold:
            coupon_discount = 50.0
        else:
            coupon_discount = 0.0

    final_total = max(0.0, subtotal - coupon_discount + delivery_charge)

    return {
        "items": items_list,
        "item_count": sum(i["quantity"] for i in items_list),
        "subtotal": subtotal,
        "product_savings": product_savings,
        "discount": coupon_discount,
        "delivery_charge": delivery_charge,
        "final_total": final_total,
        "free_delivery_threshold": free_delivery_threshold,
        "is_free_delivery": (subtotal >= free_delivery_threshold),
        "amount_for_free_delivery": max(0.0, free_delivery_threshold - subtotal),
    }


def render_cart_page() -> None:
    """Render the full interactive Shopping Cart page."""
    _init_cart()
    totals = calculate_cart_totals()

    st.title("Shopping Cart")
    st.caption("Review your grocery selections, manage quantities, and proceed to checkout.")

    # Empty cart state
    if not totals["items"]:
        with st.container(border=True):
            st.subheader("Your cart is empty.")
            st.write("Add some fresh groceries to get started.")
            if st.button("Start Shopping", key="cart_start_shopping_btn", type="primary"):
                st.session_state.current_page = "Shop"
                st.session_state.selected_category = "All"
                st.rerun()
        return

    # Two column layout: Cart Items & Order Summary
    col_items, col_summary = st.columns([1.6, 1.1])

    # Left: Cart items list
    with col_items:
        st.subheader(f"Items in Basket ({totals['item_count']} units)")

        for item in totals["items"]:
            with st.container(border=True):
                c_img, c_info, c_qty, c_sub = st.columns([1, 2.2, 1.8, 1.2])

                with c_img:
                    img_path = item.get("image", "")
                    if img_path and os.path.exists(img_path):
                        st.image(img_path, width="stretch")
                    else:
                        st.write("🧺")

                with c_info:
                    st.write(f"**{item['name']}**")
                    st.caption(f"{item['unit']} • ₹{item['price']:.2f} each")

                with c_qty:
                    # Quantity buttons
                    q_minus, q_disp, q_plus = st.columns([1, 1.2, 1])
                    with q_minus:
                        if st.button("➖", key=f"cart_minus_{item['id']}", use_container_width=True):
                            update_cart_quantity(item["id"], item["quantity"] - 1)
                            st.rerun()
                    with q_disp:
                        st.write(f"**{item['quantity']}**")
                    with q_plus:
                        if st.button("➕", key=f"cart_plus_{item['id']}", use_container_width=True):
                            update_cart_quantity(item["id"], item["quantity"] + 1)
                            st.rerun()

                with c_sub:
                    st.write(f"**₹{item['line_total']:.2f}**")
                    if st.button("Remove", key=f"remove_from_cart_{item['id']}", use_container_width=True):
                        remove_from_cart(item["id"])
                        st.rerun()

        # Clear Cart Action
        st.write("")
        c_act1, c_act2 = st.columns([1, 2])
        with c_act1:
            if st.button("Clear Entire Cart", key="cart_clear_all_btn"):
                clear_cart()
                st.rerun()
        with c_act2:
            if st.button("← Add More Items", key="cart_continue_btn"):
                st.session_state.current_page = "Shop"
                st.rerun()

    # Right: Order Summary & Coupon
    with col_summary:
        with st.container(border=True):
            st.subheader("Order Summary")

            # Free delivery banner
            if totals["is_free_delivery"]:
                st.success("🎉 **FREE Delivery Unlocked!** (Orders above ₹499)")
            else:
                rem = totals["amount_for_free_delivery"]
                st.info(f"🚚 Add **₹{rem:.2f}** more to get **FREE Delivery**!")

            st.divider()

            # Coupon section
            st.write("##### Promotional Coupon")
            applied_coupon = st.session_state.get("applied_coupon", "")
            
            cp_col1, cp_col2 = st.columns([2, 1])
            with cp_col1:
                entered_code = st.text_input(
                    "Coupon Code",
                    value=applied_coupon or "",
                    placeholder="e.g. GROCIO50",
                    label_visibility="collapsed",
                    key="cart_coupon_input"
                )
            with cp_col2:
                if st.button("Apply", key="cart_apply_coupon_btn", use_container_width=True):
                    if entered_code.strip().upper() == "GROCIO50":
                        st.session_state.applied_coupon = "GROCIO50"
                        if totals["subtotal"] >= totals["free_delivery_threshold"]:
                            st.toast("Coupon GROCIO50 applied! ₹50 OFF saved.")
                        else:
                            st.toast("GROCIO50 requires minimum ₹499 subtotal.")
                        st.rerun()
                    elif entered_code.strip() == "":
                        st.session_state.applied_coupon = None
                        st.rerun()
                    else:
                        st.error("Invalid coupon code.")

            if applied_coupon == "GROCIO50":
                if totals["subtotal"] >= totals["free_delivery_threshold"]:
                    st.caption("✅ **GROCIO50 applied:** ₹50 discount included!")
                else:
                    st.caption("⚠️ **GROCIO50** requires min. order of ₹499 to activate.")

            st.divider()

            # Bill breakdown
            r1_l, r1_r = st.columns(2)
            with r1_l:
                st.write("Item Subtotal:")
            with r1_r:
                st.write(f"₹{totals['subtotal']:.2f}")

            if totals["discount"] > 0:
                r2_l, r2_r = st.columns(2)
                with r2_l:
                    st.write("Coupon Discount:")
                with r2_r:
                    st.write(f"-₹{totals['discount']:.2f}")

            r3_l, r3_r = st.columns(2)
            with r3_l:
                st.write("Delivery Charge:")
            with r3_r:
                if totals["delivery_charge"] == 0:
                    st.write("FREE")
                else:
                    st.write(f"₹{totals['delivery_charge']:.2f}")

            st.divider()

            # Final Total
            r4_l, r4_r = st.columns(2)
            with r4_l:
                st.write("### Total Amount:")
            with r4_r:
                st.write(f"### ₹{totals['final_total']:.2f}")

            if totals["product_savings"] > 0:
                st.success(f"🌱 You are saving ₹{totals['product_savings']:.2f} on catalogue MRP!")

            st.write("")
            
            # Checkout button
            if st.button("Proceed to Checkout →", key="checkout_button", type="primary", use_container_width=True):
                st.session_state.current_page = "Checkout"
                st.rerun()
