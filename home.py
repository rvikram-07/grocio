"""Homepage Module for Grocio — Smart Grocery Booking System.

Renders the Hero banner, official brand logo, featured categories,
popular groceries, promotional offers, Why Choose Grocio value props,
and the comprehensive website footer.
"""

import os
import streamlit as st
import products
import categories

LOGO_PATH = os.path.join("assets", "grocio_logo.jpg")


def render_home_page() -> None:
    """Render the full interactive Homepage view."""
    
    # 1. HERO SECTION
    hero_col_left, hero_col_right = st.columns([1.4, 1])

    with hero_col_left:
        # Display official Grocio brand logo
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=320)
        else:
            st.subheader("🛒 GROCIO")

        st.title("Fresh groceries. Simple shopping.")
        st.write(
            "Discover everyday essentials, explore fresh groceries, and prepare your order "
            "in just a few clicks. Sourced fresh daily from trusted local farms and packaged with care."
        )

        st.write("")
        # Primary Call to Action
        btn_c1, btn_c2 = st.columns([1, 1.2])
        with btn_c1:
            if st.button("Shop Now →", key="home_hero_shop_now", type="primary", use_container_width=True):
                st.session_state.current_page = "Shop"
                st.session_state.selected_category = "All"
                st.session_state.search_query = ""
                st.rerun()
        with btn_c2:
            if st.button("Browse Categories", key="home_hero_browse_cats", use_container_width=True):
                st.session_state.current_page = "Categories"
                st.rerun()

        st.write("")
        # Trust highlights row
        t1, t2, t3 = st.columns(3)
        with t1:
            st.caption("⚡ **15–25 Mins**\nExpress Delivery")
        with t2:
            st.caption("🌿 **100% Farm Fresh**\nQuality Guaranteed")
        with t3:
            st.caption("💰 **Best Value**\nAuthentic Local Prices")

    with hero_col_right:
        # Hero Feature Highlight Card
        with st.container(border=True):
            st.subheader("🌟 Today's Fresh Picks")
            st.caption("Hand-selected morning arrivals at peak freshness")
            
            p_mango = products.get_product_by_id("prod_frt_4")
            p_milk = products.get_product_by_id("prod_dry_1")
            
            if p_mango and os.path.exists(p_mango.get("image", "")):
                st.image(p_mango["image"], width="stretch")
                st.write(f"**{p_mango['name']}** • ₹{p_mango['price']:.2f}")
                st.caption(p_mango["description"][:90] + "...")
            
            st.divider()
            st.info("🚚 **Free Delivery** on all grocery baskets above ₹499!")

    st.write("")
    st.divider()

    # 2. FEATURED CATEGORIES
    categories.render_featured_categories_preview()

    st.write("")
    st.divider()

    # 3. POPULAR PRODUCTS (Curated Top Picks)
    st.header("Popular Groceries")
    st.caption("Top essentials chosen by happy families across the city.")

    popular_items = products.get_featured_products(limit=6)
    pop_cols = st.columns(3)
    for idx, prod in enumerate(popular_items):
        with pop_cols[idx % 3]:
            products.render_product_card(prod, key_prefix="home_popular")

    st.write("")
    center_col1, center_col2, center_col3 = st.columns([1, 1.2, 1])
    with center_col2:
        if st.button("View All Products →", key="home_view_all_prods_btn", type="primary", use_container_width=True):
            st.session_state.current_page = "Shop"
            st.session_state.selected_category = "All"
            st.session_state.search_query = ""
            st.rerun()

    st.write("")
    st.divider()

    # 4. PROMOTIONAL OFFERS
    st.header("Today's Grocery Offers")
    st.caption("Save more every single day with Grocio member discounts.")

    off_c1, off_c2 = st.columns(2)
    with off_c1:
        with st.container(border=True):
            st.subheader("🥦 Flat 20% OFF Farm Vegetables")
            st.write("Crisp spinach, vine tomatoes, and juicy cucumbers directly from rural growers.")
            st.caption("Discounted prices active in catalogue")
            if st.button("Claim Vegetable Savings", key="home_claim_veg", use_container_width=True):
                st.session_state.selected_category = "Vegetables"
                st.session_state.current_page = "Shop"
                st.rerun()

    with off_c2:
        with st.container(border=True):
            st.subheader("🏷️ Flat ₹50 OFF with Code GROCIO50")
            st.write("Special introductory grocery voucher applicable on any order of ₹499 or more.")
            st.caption("Enter coupon during checkout")
            if st.button("Explore Eligible Staples", key="home_claim_coupon", use_container_width=True):
                st.session_state.applied_coupon = "GROCIO50"
                st.session_state.current_page = "Offers"
                st.rerun()

    st.write("")
    st.divider()

    # 5. WHY CHOOSE GROCIO?
    st.header("Why Choose Grocio?")
    st.caption("Smart Grocery Shopping, Made Simple.")

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        with st.container(border=True):
            st.subheader("🛒 Everyday Essentials")
            st.write("Over 35+ hand-graded items spanning vegetables, fruits, dairy, bakery, snacks, and staples.")

    with w2:
        with st.container(border=True):
            st.subheader("⚡ 15–25m Express")
            st.write("Hyperlocal fulfillment centers dispatch your groceries within minutes of placing your booking.")

    with w3:
        with st.container(border=True):
            st.subheader("🚚 Flexible Delivery")
            st.write("Choose between blazing Express slots or economical Standard neighborhood batch delivery.")

    with w4:
        with st.container(border=True):
            st.subheader("💳 Convenient Checkout")
            st.write("Instant UPI simulation, simulated debit/credit cards, and traditional Cash on Delivery options.")

    st.write("")
    st.divider()

    # 6. FOOTER
    f_c1, f_c2, f_c3, f_c4 = st.columns([1.5, 1, 1, 1.2])

    with f_c1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=180)
        st.write("**GROCIO**")
        st.caption("Smart Grocery Shopping, Made Simple.")
        st.write(
            "Your friendly neighborhood online grocery partner delivering pure dairy, "
            "fresh farm vegetables, and daily staples right to your doorstep."
        )

    with f_c2:
        st.write("#### Quick Links")
        if st.button("Home", key="footer_nav_home"):
            st.session_state.current_page = "Home"
            st.rerun()
        if st.button("Shop All", key="footer_nav_shop"):
            st.session_state.current_page = "Shop"
            st.session_state.selected_category = "All"
            st.rerun()
        if st.button("Categories", key="footer_nav_categories"):
            st.session_state.current_page = "Categories"
            st.rerun()
        if st.button("Special Offers", key="footer_nav_offers"):
            st.session_state.current_page = "Offers"
            st.rerun()

    with f_c3:
        st.write("#### Categories")
        cats = ["Vegetables", "Fruits", "Dairy", "Bakery", "Staples"]
        for c in cats:
            if st.button(c, key=f"footer_cat_{c.lower()}"):
                st.session_state.selected_category = c
                st.session_state.current_page = "Shop"
                st.rerun()

    with f_c4:
        st.write("#### Help & Support")
        st.write("📞 **Helpline:** 1800-GROCIO-HELP")
        st.write("📧 **Email:** support@grocio.local")
        st.write("⏰ **Operational Hours:** 6:00 AM – 11:00 PM Daily")
        st.caption("Demo application for academic & software evaluation.")

    st.divider()
    st.caption("© 2026 Grocio — Smart Grocery Shopping, Made Simple. All rights reserved.")
