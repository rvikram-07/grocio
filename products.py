"""Product Catalogue Module for Grocio — Smart Grocery Booking System.

Stores the 35 grocery products, product details, search, filtering,
sorting, card rendering, and the Shop, Product Details, and Offers pages.
"""

import os
import streamlit as st

# Comprehensive grocery dataset with 35 realistic products
PRODUCTS_DATA = [
    # 1. VEGETABLES (7 items)
    {
        "id": "prod_veg_1",
        "name": "Fresh Tomatoes (Hybrid)",
        "category": "Vegetables",
        "price": 40.0,
        "original_price": 50.0,
        "discount": 20,
        "unit": "500 g",
        "image": os.path.join("assets", "products", "prod_veg_1.png"),
        "description": "Farm-fresh ripe hybrid tomatoes. Perfect for everyday curries, rich gravies, and fresh salads.",
        "rating": 4.6,
        "stock": "Available",
        "popularity": 95,
    },
    {
        "id": "prod_veg_2",
        "name": "Farm Fresh Potatoes",
        "category": "Vegetables",
        "price": 30.0,
        "original_price": 35.0,
        "discount": 14,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_veg_2.png"),
        "description": "Naturally grown unwashed potatoes with firm skin and rich starch content. Versatile kitchen staple.",
        "rating": 4.5,
        "stock": "Available",
        "popularity": 90,
    },
    {
        "id": "prod_veg_3",
        "name": "Nashik Red Onions",
        "category": "Vegetables",
        "price": 45.0,
        "original_price": 55.0,
        "discount": 18,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_veg_3.png"),
        "description": "Crisp, pungent red onions sourced directly from Nashik farms. Essential for tadkas and biryanis.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 96,
    },
    {
        "id": "prod_veg_4",
        "name": "Fresh Orange Carrots",
        "category": "Vegetables",
        "price": 35.0,
        "original_price": 45.0,
        "discount": 22,
        "unit": "500 g",
        "image": os.path.join("assets", "products", "prod_veg_4.png"),
        "description": "Sweet, crunchy orange carrots packed with beta-carotene. Ideal for snacking, salads, and fresh juice.",
        "rating": 4.4,
        "stock": "Available",
        "popularity": 82,
    },
    {
        "id": "prod_veg_5",
        "name": "Crisp Green Cucumbers",
        "category": "Vegetables",
        "price": 25.0,
        "original_price": 30.0,
        "discount": 17,
        "unit": "500 g",
        "image": os.path.join("assets", "products", "prod_veg_5.png"),
        "description": "Cooling, crunchy green cucumbers with thin skin and tender seeds. Refreshing salad essential.",
        "rating": 4.3,
        "stock": "Available",
        "popularity": 78,
    },
    {
        "id": "prod_veg_6",
        "name": "Fresh Organic Spinach (Palak)",
        "category": "Vegetables",
        "price": 28.0,
        "original_price": 35.0,
        "discount": 20,
        "unit": "250 g",
        "image": os.path.join("assets", "products", "prod_veg_6.png"),
        "description": "Tender and pesticide-free hydroponic spinach leaves. Rich in iron, dietary fibre, and vitamins.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 85,
    },
    {
        "id": "prod_veg_7",
        "name": "Crisp Green Capsicum",
        "category": "Vegetables",
        "price": 38.0,
        "original_price": 45.0,
        "discount": 16,
        "unit": "500 g",
        "image": os.path.join("assets", "products", "prod_veg_7.png"),
        "description": "Glossy green bell peppers with a crisp crunch and mild sweetness. Great for stir-fries and pizza toppings.",
        "rating": 4.5,
        "stock": "Available",
        "popularity": 80,
    },

    # 2. FRUITS (6 items)
    {
        "id": "prod_frt_1",
        "name": "Shimla Royal Apples",
        "category": "Fruits",
        "price": 150.0,
        "original_price": 180.0,
        "discount": 17,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_frt_1.png"),
        "description": "Crisp and aromatic Royal Delicious apples harvested from the orchards of Shimla. Naturally sweet.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 94,
    },
    {
        "id": "prod_frt_2",
        "name": "Fresh Robusta Bananas",
        "category": "Fruits",
        "price": 45.0,
        "original_price": 55.0,
        "discount": 18,
        "unit": "1 kg (6-8 pcs)",
        "image": os.path.join("assets", "products", "prod_frt_2.png"),
        "description": "Naturally sweetened robusta bananas, rich in potassium and energy. Daily breakfast essential.",
        "rating": 4.6,
        "stock": "Available",
        "popularity": 92,
    },
    {
        "id": "prod_frt_3",
        "name": "Nagpur Sweet Oranges",
        "category": "Fruits",
        "price": 75.0,
        "original_price": 90.0,
        "discount": 17,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_frt_3.png"),
        "description": "Juicy and citrus-rich Nagpur santras. Bursting with natural vitamin C and invigorating flavor.",
        "rating": 4.5,
        "stock": "Available",
        "popularity": 84,
    },
    {
        "id": "prod_frt_4",
        "name": "Premium Alphonso Mangoes",
        "category": "Fruits",
        "price": 280.0,
        "original_price": 350.0,
        "discount": 20,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_frt_4.png"),
        "description": "King of fruits! Ratnagiri Alphonso mangoes featuring heavenly aroma, rich saffron pulp, and smooth texture.",
        "rating": 4.9,
        "stock": "Available",
        "popularity": 99,
    },
    {
        "id": "prod_frt_5",
        "name": "Seedless Green Grapes",
        "category": "Fruits",
        "price": 85.0,
        "original_price": 100.0,
        "discount": 15,
        "unit": "500 g",
        "image": os.path.join("assets", "products", "prod_frt_5.png"),
        "description": "Crisp and sweet Sonaka seedless green grapes. Perfect refreshing snack for kids and adults.",
        "rating": 4.4,
        "stock": "Available",
        "popularity": 81,
    },
    {
        "id": "prod_frt_6",
        "name": "Ruby Red Kesar Pomegranates",
        "category": "Fruits",
        "price": 140.0,
        "original_price": 170.0,
        "discount": 18,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_frt_6.png"),
        "description": "Plump and juicy ruby-red arils packed with antioxidants. Excellent for boosting immunity and hemoglobin.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 87,
    },

    # 3. DAIRY (5 items)
    {
        "id": "prod_dry_1",
        "name": "Full Cream Fresh Milk",
        "category": "Dairy",
        "price": 33.0,
        "original_price": 35.0,
        "discount": 6,
        "unit": "500 ml",
        "image": os.path.join("assets", "products", "prod_dry_1.png"),
        "description": "Pasteurized homogenized full-cream cow milk with 6.0% fat. Rich taste for chai, coffee, and sweets.",
        "rating": 4.9,
        "stock": "Available",
        "popularity": 98,
    },
    {
        "id": "prod_dry_2",
        "name": "Farm Fresh Dahi (Curd)",
        "category": "Dairy",
        "price": 40.0,
        "original_price": 45.0,
        "discount": 11,
        "unit": "400 g",
        "image": os.path.join("assets", "products", "prod_dry_2.png"),
        "description": "Thick, creamy set curd prepared from pure milk. Rich in natural probiotics for gut wellness.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 89,
    },
    {
        "id": "prod_dry_3",
        "name": "Salted Table Butter",
        "category": "Dairy",
        "price": 58.0,
        "original_price": 62.0,
        "discount": 6,
        "unit": "100 g",
        "image": os.path.join("assets", "products", "prod_dry_3.png"),
        "description": "Classic creamy salted butter made from pure milk fat. Melts smoothly over warm toast and parathas.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 91,
    },
    {
        "id": "prod_dry_4",
        "name": "Processed Cheese Slices",
        "category": "Dairy",
        "price": 135.0,
        "original_price": 155.0,
        "discount": 13,
        "unit": "200 g (10 pcs)",
        "image": os.path.join("assets", "products", "prod_dry_4.png"),
        "description": "Individually wrapped cheese slices with superior meltability. Ideal for breakfast sandwiches and burgers.",
        "rating": 4.6,
        "stock": "Available",
        "popularity": 86,
    },
    {
        "id": "prod_dry_5",
        "name": "Fresh Soft Malai Paneer",
        "category": "Dairy",
        "price": 95.0,
        "original_price": 110.0,
        "discount": 14,
        "unit": "200 g",
        "image": os.path.join("assets", "products", "prod_dry_5.png"),
        "description": "Ultra-soft and fresh cottage cheese blocks. Tender texture absorbs curry spices quickly.",
        "rating": 4.9,
        "stock": "Available",
        "popularity": 97,
    },

    # 4. BAKERY (4 items)
    {
        "id": "prod_bky_1",
        "name": "Whole Wheat Brown Bread",
        "category": "Bakery",
        "price": 45.0,
        "original_price": 50.0,
        "discount": 10,
        "unit": "400 g",
        "image": os.path.join("assets", "products", "prod_bky_1.png"),
        "description": "Daily baked 100% whole wheat sliced bread. No added palm oil, enriched with natural dietary fibre.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 93,
    },
    {
        "id": "prod_bky_2",
        "name": "Soft Sesame Burger Buns",
        "category": "Bakery",
        "price": 35.0,
        "original_price": 40.0,
        "discount": 12,
        "unit": "Pack of 4",
        "image": os.path.join("assets", "products", "prod_bky_2.png"),
        "description": "Pillowy-soft bakery buns topped with roasted white sesame seeds. Great for homemade sliders.",
        "rating": 4.4,
        "stock": "Available",
        "popularity": 75,
    },
    {
        "id": "prod_bky_3",
        "name": "Butter Choco-Chip Cookies",
        "category": "Bakery",
        "price": 80.0,
        "original_price": 100.0,
        "discount": 20,
        "unit": "150 g",
        "image": os.path.join("assets", "products", "prod_bky_3.png"),
        "description": "Crunchy golden butter cookies loaded with melted Belgian chocolate chips. Perfect evening treat.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 88,
    },
    {
        "id": "prod_bky_4",
        "name": "French Butter Croissants",
        "category": "Bakery",
        "price": 110.0,
        "original_price": 130.0,
        "discount": 15,
        "unit": "Pack of 2",
        "image": os.path.join("assets", "products", "prod_bky_4.png"),
        "description": "Artisan laminated dough croissants baked to golden perfection. Flaky layers with pure French butter aroma.",
        "rating": 4.5,
        "stock": "Out of Stock",
        "popularity": 79,
    },

    # 5. SNACKS (4 items)
    {
        "id": "prod_snk_1",
        "name": "Classic Salted Potato Chips",
        "category": "Snacks",
        "price": 20.0,
        "original_price": 20.0,
        "discount": 0,
        "unit": "52 g",
        "image": os.path.join("assets", "products", "prod_snk_1.png"),
        "description": "Thin, crispy sliced potatoes lightly sprinkled with sea salt. The timeless tea-time crunch.",
        "rating": 4.6,
        "stock": "Available",
        "popularity": 92,
    },
    {
        "id": "prod_snk_2",
        "name": "Digestive Multigrain Biscuits",
        "category": "Snacks",
        "price": 40.0,
        "original_price": 45.0,
        "discount": 11,
        "unit": "250 g",
        "image": os.path.join("assets", "products", "prod_snk_2.png"),
        "description": "Fibre-loaded crunchy biscuits baked with oats, whole wheat, and malt. Delicious partner for hot tea.",
        "rating": 4.5,
        "stock": "Available",
        "popularity": 83,
    },
    {
        "id": "prod_snk_3",
        "name": "70% Dark Chocolate Bar",
        "category": "Snacks",
        "price": 99.0,
        "original_price": 125.0,
        "discount": 21,
        "unit": "100 g",
        "image": os.path.join("assets", "products", "prod_snk_3.png"),
        "description": "Rich artisanal dark chocolate made from single-origin cocoa beans. Velvety texture and balanced bitterness.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 89,
    },
    {
        "id": "prod_snk_4",
        "name": "Crispy Spicy Aloo Bhujia",
        "category": "Snacks",
        "price": 55.0,
        "original_price": 65.0,
        "discount": 15,
        "unit": "200 g",
        "image": os.path.join("assets", "products", "prod_snk_4.png"),
        "description": "Famous spicy potato and gram flour sev seasoned with traditional Indian spices and mint.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 90,
    },

    # 6. BEVERAGES (4 items)
    {
        "id": "prod_bev_1",
        "name": "100% Orange Fruit Juice",
        "category": "Beverages",
        "price": 110.0,
        "original_price": 135.0,
        "discount": 19,
        "unit": "1 Litre",
        "image": os.path.join("assets", "products", "prod_bev_1.png"),
        "description": "Pure pressed orange juice with no added sugar or preservatives. Packed with real fruit pulp.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 88,
    },
    {
        "id": "prod_bev_2",
        "name": "Assam Premium CTC Tea",
        "category": "Beverages",
        "price": 160.0,
        "original_price": 190.0,
        "discount": 16,
        "unit": "500 g",
        "image": os.path.join("assets", "products", "prod_bev_2.png"),
        "description": "Strong, full-bodied CTC tea granules with long leaf blend. Gives an invigorating brisk brew and amber color.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 95,
    },
    {
        "id": "prod_bev_3",
        "name": "Filter Coffee Roast Blend",
        "category": "Beverages",
        "price": 145.0,
        "original_price": 175.0,
        "discount": 17,
        "unit": "200 g",
        "image": os.path.join("assets", "products", "prod_bev_3.png"),
        "description": "Traditional 80:20 plantation coffee and chicory blend. Deep aroma, creamy froth, and bold flavor.",
        "rating": 4.9,
        "stock": "Available",
        "popularity": 91,
    },
    {
        "id": "prod_bev_4",
        "name": "Natural Spring Mineral Water",
        "category": "Beverages",
        "price": 20.0,
        "original_price": 20.0,
        "discount": 0,
        "unit": "1 Litre",
        "image": os.path.join("assets", "products", "prod_bev_4.png"),
        "description": "Pure packaged drinking water treated with multi-barrier filtration and enriched with minerals.",
        "rating": 4.5,
        "stock": "Available",
        "popularity": 85,
    },

    # 7. STAPLES (5 items)
    {
        "id": "prod_stp_1",
        "name": "Premium Basmati Rice",
        "category": "Staples",
        "price": 130.0,
        "original_price": 160.0,
        "discount": 19,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_stp_1.png"),
        "description": "Long-grain aged Basmati rice. Cooked grains expand up to 2.5 times with distinct pearly aroma.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 96,
    },
    {
        "id": "prod_stp_2",
        "name": "Chakki Fresh Sharbati Atta",
        "category": "Staples",
        "price": 230.0,
        "original_price": 260.0,
        "discount": 12,
        "unit": "5 kg",
        "image": os.path.join("assets", "products", "prod_stp_2.png"),
        "description": "100% whole wheat stone-ground flour from Sehore Sharbati grains. Makes rotis soft and fluffy for hours.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 97,
    },
    {
        "id": "prod_stp_3",
        "name": "Pure Sulphurless Sugar",
        "category": "Staples",
        "price": 48.0,
        "original_price": 55.0,
        "discount": 13,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_stp_3.png"),
        "description": "Sparkling white refined sugar produced using sulphur-free refining. Free flowing, pure sweetness.",
        "rating": 4.6,
        "stock": "Available",
        "popularity": 89,
    },
    {
        "id": "prod_stp_4",
        "name": "Iodized Crystal Salt",
        "category": "Staples",
        "price": 24.0,
        "original_price": 28.0,
        "discount": 14,
        "unit": "1 kg",
        "image": os.path.join("assets", "products", "prod_stp_4.png"),
        "description": "Vacuum-evaporated pure iodized cooking salt. Ensures uniform taste and fulfills daily iodine need.",
        "rating": 4.7,
        "stock": "Available",
        "popularity": 88,
    },
    {
        "id": "prod_stp_5",
        "name": "Cold-Pressed Cooking Oil",
        "category": "Staples",
        "price": 175.0,
        "original_price": 210.0,
        "discount": 17,
        "unit": "1 Litre",
        "image": os.path.join("assets", "products", "prod_stp_5.png"),
        "description": "Unrefined healthy blended cooking oil with high smoke point and natural omega fatty acids.",
        "rating": 4.8,
        "stock": "Available",
        "popularity": 94,
    },
]


def get_all_products() -> list:
    """Return all products in catalogue."""
    return PRODUCTS_DATA


def get_product_by_id(product_id: str) -> dict | None:
    """Retrieve single product by id."""
    for p in PRODUCTS_DATA:
        if p["id"] == product_id:
            return p
    return None


def get_featured_products(limit: int = 6) -> list:
    """Get top products sorted by popularity for homepage display."""
    sorted_prods = sorted(PRODUCTS_DATA, key=lambda x: x.get("popularity", 0), reverse=True)
    return sorted_prods[:limit]


def get_products_by_category(category: str) -> list:
    """Filter products by category name."""
    if not category or category == "All":
        return PRODUCTS_DATA
    return [p for p in PRODUCTS_DATA if p.get("category", "").lower() == category.lower()]


def get_categories_list() -> list:
    """Return list of categories including 'All'."""
    return ["All", "Vegetables", "Fruits", "Dairy", "Bakery", "Snacks", "Beverages", "Staples"]


def render_product_card(product: dict, key_prefix: str = "shop") -> None:
    """Render a single product card using Streamlit native components."""
    with st.container(border=True):
        # Image display with fallback
        img_path = product.get("image", "")
        if img_path and os.path.exists(img_path):
            st.image(img_path, width="stretch")
        else:
            st.info(f"🧺 {product['category']}")

        # Product Title
        st.subheader(product["name"])
        
        # Meta: Unit & Rating
        st.caption(f"⭐ **{product['rating']}** / 5.0 • {product['unit']}")

        # Price, Original Price, and Discount
        p_curr = product["price"]
        p_orig = product["original_price"]
        disc = product["discount"]

        price_col, disc_col = st.columns([1.5, 1])
        with price_col:
            if disc > 0 and p_orig > p_curr:
                st.write(f"### ₹{p_curr:.2f}")
                st.caption(f"MRP: ~~₹{p_orig:.2f}~~")
            else:
                st.write(f"### ₹{p_curr:.2f}")
        with disc_col:
            if disc > 0:
                st.success(f"{disc}% OFF")

        # Stock status
        is_in_stock = product.get("stock") == "Available"
        if is_in_stock:
            st.caption("🟢 In Stock")
        else:
            st.caption("🔴 Out of Stock")

        # Action buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            details_key = f"view_product_{product['id']}_{key_prefix}"
            if st.button("Details", key=details_key, use_container_width=True):
                st.session_state.selected_product_id = product["id"]
                st.session_state.current_page = "Product Details"
                st.rerun()

        with btn_col2:
            add_key = f"add_to_cart_{product['id']}_{key_prefix}"
            if st.button("Add to Cart", key=add_key, type="primary", disabled=not is_in_stock, use_container_width=True):
                import cart
                cart.add_to_cart(product["id"], 1)
                st.rerun()


def render_shop_page() -> None:
    """Render the full dedicated Shop catalogue page."""
    st.title("Shop Groceries")
    st.caption("Browse daily essentials, search across products, and filter by your favorite categories.")

    # 1. Filter and Search Controls Bar
    c_search, c_cat, c_sort, c_clear = st.columns([3, 2, 2, 1])

    with c_search:
        # User search input
        curr_search = st.session_state.get("search_query", "")
        search_input = st.text_input(
            "Search Products",
            value=curr_search,
            key="shop_search",
            placeholder="Search by name, category, or keyword..."
        )
        if search_input != curr_search:
            st.session_state.search_query = search_input

    with c_cat:
        cat_options = get_categories_list()
        selected_cat = st.session_state.get("selected_category", "All")
        # Ensure selected_cat is in options
        if selected_cat not in cat_options:
            selected_cat = "All"
        cat_idx = cat_options.index(selected_cat)
        new_cat = st.selectbox("Category Filter", cat_options, index=cat_idx, key="category_filter")
        if new_cat != selected_cat:
            st.session_state.selected_category = new_cat

    with c_sort:
        sort_options = ["Popularity", "Price: Low to High", "Price: High to Low", "Rating"]
        curr_sort = st.session_state.get("sort_option", "Popularity")
        sort_idx = sort_options.index(curr_sort) if curr_sort in sort_options else 0
        new_sort = st.selectbox("Sort Order", sort_options, index=sort_idx, key="sort_option")
        if new_sort != curr_sort:
            st.session_state.sort_option = new_sort

    with c_clear:
        st.write("")  # Alignment spacer
        st.write("")
        if st.button("Clear", key="shop_clear_filters_btn", use_container_width=True):
            st.session_state.search_query = ""
            st.session_state.selected_category = "All"
            st.session_state.sort_option = "Popularity"
            st.rerun()

    # 2. Filter data logic
    filtered = list(PRODUCTS_DATA)
    active_search = st.session_state.get("search_query", "").strip().lower()
    active_category = st.session_state.get("selected_category", "All")
    active_sort = st.session_state.get("sort_option", "Popularity")

    # Category filter
    if active_category and active_category != "All":
        filtered = [p for p in filtered if p["category"].lower() == active_category.lower()]

    # Search filter
    if active_search:
        filtered = [
            p for p in filtered
            if active_search in p["name"].lower()
            or active_search in p["category"].lower()
            or active_search in p["description"].lower()
        ]

    # Sorting
    if active_sort == "Price: Low to High":
        filtered.sort(key=lambda x: x["price"])
    elif active_sort == "Price: High to Low":
        filtered.sort(key=lambda x: x["price"], reverse=True)
    elif active_sort == "Rating":
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    elif active_sort == "Popularity":
        filtered.sort(key=lambda x: x.get("popularity", 0), reverse=True)

    # 3. Product Count and Active State Feedback
    active_details = []
    if active_category != "All":
        active_details.append(f"Category: **{active_category}**")
    if active_search:
        active_details.append(f"Search: **'{active_search}'**")

    status_col1, status_col2 = st.columns([3, 1])
    with status_col1:
        details_txt = f" ({', '.join(active_details)})" if active_details else ""
        st.write(f"Showing **{len(filtered)}** products{details_txt}")
    with status_col2:
        st.caption(f"Sorted by: {active_sort}")

    st.divider()

    # 4. Render Grid or Empty state
    if not filtered:
        with st.container(border=True):
            st.warning("🔍 **No products found.**")
            st.write("Try another search term or clear your filters to explore our full grocery catalogue.")
            if st.button("Reset All Filters", key="reset_filters_empty_state", type="primary"):
                st.session_state.search_query = ""
                st.session_state.selected_category = "All"
                st.session_state.sort_option = "Popularity"
                st.rerun()
    else:
        # Multi-column grid (3 columns for optimal balance on desktop and mobile)
        cols = st.columns(3)
        for idx, prod in enumerate(filtered):
            with cols[idx % 3]:
                render_product_card(prod, key_prefix="shop_grid")


def render_product_details_page() -> None:
    """Render the comprehensive single product details view."""
    prod_id = st.session_state.get("selected_product_id")
    product = get_product_by_id(prod_id) if prod_id else None

    if not product:
        with st.container(border=True):
            st.warning("Product not found or selection expired.")
            if st.button("← Back to Shop", key="details_fallback_back_btn", type="primary"):
                st.session_state.current_page = "Shop"
                st.rerun()
        return

    # Back navigation button
    if st.button("← Back to Shop", key="details_back_btn"):
        st.session_state.current_page = "Shop"
        st.rerun()

    st.write("")
    left_col, right_col = st.columns([1.2, 1.8])

    with left_col:
        with st.container(border=True):
            img_path = product.get("image", "")
            if img_path and os.path.exists(img_path):
                st.image(img_path, width="stretch")
            else:
                st.info(f"🧺 {product['name']}")

    with right_col:
        with st.container(border=True):
            st.caption(f"Category: **{product['category']}** • ID: `{product['id']}`")
            st.title(product["name"])
            
            # Rating and Unit
            st.write(f"⭐ **{product['rating']} / 5.0** • Net Quantity: **{product['unit']}**")

            st.divider()

            # Pricing
            p_curr = product["price"]
            p_orig = product["original_price"]
            disc = product["discount"]

            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.write(f"## ₹{p_curr:.2f}")
                if disc > 0 and p_orig > p_curr:
                    st.caption(f"MRP: ~~₹{p_orig:.2f}~~ (You save ₹{p_orig - p_curr:.2f})")
            with p_col2:
                if disc > 0:
                    st.success(f"🎉 **{disc}% DISCOUNT APPLIED**")

            st.divider()

            # Description
            st.write("### Product Description")
            st.write(product["description"])

            # Stock status
            is_in_stock = product.get("stock") == "Available"
            if is_in_stock:
                st.success("✅ **In Stock:** Ready for 15–45 min local delivery")
            else:
                st.error("❌ **Currently Out of Stock:** Check back tomorrow!")

            st.write("")

            # Quantity Selector and Add to Cart
            if is_in_stock:
                q_col, a_col = st.columns([1, 2])
                with q_col:
                    qty = st.number_input(
                        "Select Quantity",
                        min_value=1,
                        max_value=20,
                        value=1,
                        step=1,
                        key="details_qty_selector"
                    )
                with a_col:
                    st.write("")  # Vertical alignment
                    st.write("")
                    if st.button("Add to Cart", key="details_add_to_cart_btn", type="primary", use_container_width=True):
                        import cart
                        cart.add_to_cart(product["id"], int(qty))
                        st.rerun()
            else:
                st.button("Item Unavailable", disabled=True, use_container_width=True)


def render_offers_page() -> None:
    """Render the active Offers and promotional deals page."""
    st.title("Special Offers & Deals")
    st.caption("Maximize your daily grocery savings with verified store discounts and promotional coupons.")

    # Coupon Banner Card
    with st.container(border=True):
        c_left, c_right = st.columns([3, 1.2])
        with c_left:
            st.subheader("🏷️ Flat ₹50 OFF On Orders Above ₹499")
            st.write("Stock up on kitchen essentials and get an instant ₹50 discount at checkout.")
            st.caption("Applicable once per order on all categories • Code: **GROCIO50**")
        with c_right:
            st.write("")
            applied_code = st.session_state.get("applied_coupon")
            if applied_code == "GROCIO50":
                st.success("✅ Coupon Applied!")
            else:
                if st.button("Apply Coupon", key="offers_apply_grocio50", type="primary", use_container_width=True):
                    st.session_state.applied_coupon = "GROCIO50"
                    st.toast("Coupon GROCIO50 activated for checkout!")
                    st.rerun()

    st.write("")
    st.subheader("Active Category Offers")

    # Category Offer Cards
    off_col1, off_col2 = st.columns(2)

    with off_col1:
        with st.container(border=True):
            st.subheader("🥦 20% OFF Farm Fresh Vegetables")
            st.write("Direct harvest tomatoes, crisp cucumbers, and organic spinach with up to 20% savings.")
            st.caption("Prices already discounted in catalogue.")
            if st.button("Shop Vegetables Offer", key="offer_shop_veg", use_container_width=True):
                st.session_state.selected_category = "Vegetables"
                st.session_state.search_query = ""
                st.session_state.current_page = "Shop"
                st.rerun()

    with off_col2:
        with st.container(border=True):
            st.subheader("🥛 Up to 15% OFF Pure Dairy & Butter")
            st.write("Full-cream milk, fresh malai paneer, and rich table butter for your morning breakfast.")
            st.caption("Prices already discounted in catalogue.")
            if st.button("Shop Dairy Offer", key="offer_shop_dairy", use_container_width=True):
                st.session_state.selected_category = "Dairy"
                st.session_state.search_query = ""
                st.session_state.current_page = "Shop"
                st.rerun()

    off_col3, off_col4 = st.columns(2)

    with off_col3:
        with st.container(border=True):
            st.subheader("🍪 20% OFF Artisan Cookies & Bakes")
            st.write("Freshly baked chocolate-chip butter cookies and whole wheat breads at unbeatable rates.")
            if st.button("Shop Bakery Deals", key="offer_shop_bakery", use_container_width=True):
                st.session_state.selected_category = "Bakery"
                st.session_state.search_query = ""
                st.session_state.current_page = "Shop"
                st.rerun()

    with off_col4:
        with st.container(border=True):
            st.subheader("🍚 Big Pantry Savings on Staples")
            st.write("Aged Basmati rice and cold-pressed cooking oil with up to ₹35 direct savings per unit.")
            if st.button("Shop Staples Deals", key="offer_shop_staples", use_container_width=True):
                st.session_state.selected_category = "Staples"
                st.session_state.search_query = ""
                st.session_state.current_page = "Shop"
                st.rerun()
