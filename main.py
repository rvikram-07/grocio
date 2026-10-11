"""Grocio — Smart Grocery Shopping, Made Simple.

Main execution file for the Grocio web application.
Configures page settings, global navigation, session state initialization,
and module routing across all 8 logical views.
"""

import os
import streamlit as st

# Set page config as the very first Streamlit call
st.set_page_config(
    page_title="Grocio | Grocery Booking System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the 6 functional modules
import home
import products
import categories
import cart
import checkout
import orders

LOGO_PATH = os.path.join("assets", "grocio_logo.jpg")


def init_session_state() -> None:
    """Initialize shared session-state variables safely."""
    defaults = {
        "current_page": "Home",
        "cart": {},
        "selected_category": "All",
        "search_query": "",
        "sort_option": "Popularity",
        "selected_product_id": None,
        "applied_coupon": None,
        "latest_order": None,
        "customer_name": "",
        "customer_mobile": "",
        "customer_hno": "",
        "customer_street": "",
        "customer_city": "Bengaluru",
        "customer_pincode": "",
        "sim_upi_vpa": "customer@okhdfcbank",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def render_sidebar_navigation() -> None:
    """Render consistent sidebar navigation with branding and live cart counter."""
    with st.sidebar:
        # Brand Logo display
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width="stretch")
        else:
            st.title("🛒 Grocio")
            st.caption("Smart Grocery Shopping, Made Simple.")

        st.divider()

        # Dynamic Cart Item Count
        cart_count = cart.get_cart_count()
        cart_label = f"🛍️ Cart ({cart_count})" if cart_count > 0 else "🛍️ Cart (0)"

        curr = st.session_state.get("current_page", "Home")

        st.subheader("Navigation")

        # Navigation buttons with active state highlighting
        if st.button("🏠 Home", key="nav_home", type="primary" if curr == "Home" else "secondary", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()

        if st.button("🛒 Shop", key="nav_shop", type="primary" if curr == "Shop" else "secondary", use_container_width=True):
            st.session_state.current_page = "Shop"
            st.session_state.selected_category = "All"
            st.session_state.search_query = ""
            st.rerun()

        if st.button("📂 Categories", key="nav_categories", type="primary" if curr == "Categories" else "secondary", use_container_width=True):
            st.session_state.current_page = "Categories"
            st.rerun()

        if st.button("🏷️ Offers", key="nav_offers", type="primary" if curr == "Offers" else "secondary", use_container_width=True):
            st.session_state.current_page = "Offers"
            st.rerun()

        if st.button(cart_label, key="nav_cart", type="primary" if curr == "Cart" else "secondary", use_container_width=True):
            st.session_state.current_page = "Cart"
            st.rerun()

        st.divider()

        # Live Cart Glance in Sidebar
        if cart_count > 0:
            with st.container(border=True):
                st.caption("🛒 **Active Cart Snapshot**")
                totals = cart.calculate_cart_totals()
                st.write(f"Items: **{cart_count} units**")
                st.write(f"Subtotal: **₹{totals['subtotal']:.2f}**")
                if st.button("Open Basket", key="sidebar_open_basket_btn", use_container_width=True):
                    st.session_state.current_page = "Cart"
                    st.rerun()
                if st.button("Instant Checkout", key="sidebar_instant_checkout_btn", type="primary", use_container_width=True):
                    st.session_state.current_page = "Checkout"
                    st.rerun()

        st.caption("⚡ **Express Delivery:** 15–25 Mins")
        st.caption("🚚 **Free Delivery** on orders ₹499+")
        st.caption("🔒 Verified Secure Simulated Booking")


def render_top_navigation_bar() -> None:
    """Render horizontal navigation header for seamless desktop & mobile access."""
    cart_count = cart.get_cart_count()
    cart_label = f"Cart ({cart_count})"
    curr = st.session_state.get("current_page", "Home")

    header_cols = st.columns([1.5, 0.9, 0.9, 1.1, 0.9, 1.1])

    with header_cols[0]:
        # Logo button returning directly to homepage
        if st.button("🛒 GROCIO", key="top_brand_logo_btn", help="Return to Homepage", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()

    with header_cols[1]:
        if st.button("Home", key="top_nav_home", type="primary" if curr == "Home" else "secondary", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()

    with header_cols[2]:
        if st.button("Shop", key="top_nav_shop", type="primary" if curr == "Shop" else "secondary", use_container_width=True):
            st.session_state.current_page = "Shop"
            st.session_state.selected_category = "All"
            st.session_state.search_query = ""
            st.rerun()

    with header_cols[3]:
        if st.button("Categories", key="top_nav_cats", type="primary" if curr == "Categories" else "secondary", use_container_width=True):
            st.session_state.current_page = "Categories"
            st.rerun()

    with header_cols[4]:
        if st.button("Offers", key="top_nav_offers", type="primary" if curr == "Offers" else "secondary", use_container_width=True):
            st.session_state.current_page = "Offers"
            st.rerun()

    with header_cols[5]:
        if st.button(cart_label, key="top_nav_cart", type="primary" if curr == "Cart" else "secondary", use_container_width=True):
            st.session_state.current_page = "Cart"
            st.rerun()

    st.divider()


def main() -> None:
    """Main application execution pipeline and page router."""
    init_session_state()
    render_sidebar_navigation()
    render_top_navigation_bar()

    # Logical View Dispatcher
    page = st.session_state.get("current_page", "Home")

    if page == "Home":
        home.render_home_page()
    elif page == "Shop":
        products.render_shop_page()
    elif page == "Categories":
        categories.render_categories_page()
    elif page == "Offers":
        products.render_offers_page()
    elif page == "Product Details":
        products.render_product_details_page()
    elif page == "Cart":
        cart.render_cart_page()
    elif page == "Checkout":
        checkout.render_checkout_page()
    elif page == "Order Confirmation":
        orders.render_order_confirmation_page()
    else:
        # Fallback to Home if unknown page state occurs
        home.render_home_page()


if __name__ == "__main__":
    main()
