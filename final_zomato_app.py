import streamlit as st

# --- 1. SETTINGS & APP THEME ---
st.set_page_config(page_title="DesiBites | Multi-Restaurant", layout="wide")

# Custom Styling for "Page-wise" look
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 50px; }
    .stTabs [data-baseweb="tab"] { font-size: 20px; font-weight: bold; }
    .restaurant-card { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 5px solid #e03131; }
    .add-button { background-color: #e03131; color: white; border-radius: 5px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA: 20 RESTAURANTS & THEIR CATEGORIES ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

restaurants = [
    "Masala Leaf", "Biryani Bliss", "The Early Bird", "Gilded Fork", 
    "Chulha Chauki Da Dhaba", "Waffle Wagon", "Saffron Pot", "Curry Flame",
    "Tandoor Bites", "Olive Bistro", "Sunny Side Up", "Eggslut",
    "Kickstart Cafe", "The Griddle", "Clayful Cafe", "Folklore Cafe",
    "Mist Poolside", "Ivory Platter", "Radiant Table", "Luminous Ladle"
]

# Large Menu Dataset
menu_data = {
    "🟢 Veg Starters": [
        {"name": "Paneer Tikka", "price": 160, "sym": "🟢"},
        {"name": "Gobi Manchurian", "price": 120, "sym": "🟢"},
        {"name": "Hara Bhara Kabab", "price": 140, "sym": "🟢"}
    ],
    "🔴 Non-Veg Starters": [
        {"name": "Chicken 65", "price": 180, "sym": "🔴"},
        {"name": "Fish Fry", "price": 220, "sym": "🔴"},
        {"name": "Chicken Lollipop", "price": 190, "sym": "🔴"}
    ],
    "🍛 Main Course": [
        {"name": "Chicken Biryani", "price": 250, "sym": "🔴"},
        {"name": "Butter Chicken", "price": 280, "sym": "🔴"},
        {"name": "Paneer Butter Masala", "price": 220, "sym": "🟢"},
        {"name": "Dal Tadka", "price": 150, "sym": "🟢"}
    ],
    "🍞 Breads & Rice": [
        {"name": "Butter Naan", "price": 40, "sym": "🟢"},
        {"name": "Garlic Naan", "price": 50, "sym": "🟢"},
        {"name": "Jeera Rice", "price": 120, "sym": "🟢"}
    ],
    "🥤 Beverages": [
        {"name": "Masala Chai", "price": 30, "sym": "🟢"},
        {"name": "Cold Coffee", "price": 90, "sym": "🟢"},
        {"name": "Mango Lassi", "price": 70, "sym": "🟢"}
    ]
}

# --- 3. UI: SIDEBAR (Restaurant Selection & Bill) ---
with st.sidebar:
    st.title("🛵 DesiBites")
    selected_res = st.selectbox("Choose a Restaurant", restaurants)
    st.markdown(f"### Selected: **{selected_res}**")
    st.divider()
    
    st.header("🛒 Your Cart")
    if st.session_state.cart:
        subtotal = 0
        for item in st.session_state.cart:
            st.write(f"{item['sym']} {item['name']} - ₹{item['price']}")
            subtotal += item['price']
        
        gst = subtotal * 0.05
        total = subtotal + gst + 40 # 40 for delivery
        
        st.divider()
        st.write(f"Subtotal: ₹{subtotal}")
        st.write(f"GST (5%): ₹{gst:.2f}")
        st.write(f"Delivery: ₹40")
        st.error(f"## Total: ₹{total:.2f}")
        
        if st.button("Place Order"):
            st.success(f"Order sent to {selected_res}!")
            st.balloons()
            st.session_state.cart = []
    else:
        st.info("Your cart is empty")
    
    if st.button("Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- 4. MAIN CONTENT: PAGE-WISE CATEGORIES ---
st.markdown(f"<div class='restaurant-header'><h1>{selected_res}</h1></div>", unsafe_allow_html=True)
st.write("Browse our menu by category below:")

# Creating Page-wise Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Starters", "Main Course", "Breads", "Drinks", "Desserts"])

def display_items(category_name):
    items = menu_data.get(category_name, [])
    for item in items:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{item['sym']} {item['name']}**")
        with col2:
            st.write(f"₹{item['price']}")
        with col3:
            if st.button("Add", key=f"{selected_res}_{item['name']}"):
                st.session_state.cart.append(item)
                st.rerun()
        st.divider()

with tab1:
    st.header("🔥 Starters")
    display_items("🟢 Veg Starters")
    display_items("🔴 Non-Veg Starters")

with tab2:
    st.header("🍛 Hearty Mains")
    display_items("🍛 Main Course")

with tab3:
    st.header("🍞 Indian Breads")
    display_items("🍞 Breads & Rice")

with tab4:
    st.header("🥤 Coolers & Teas")
    display_items("🥤 Beverages")

with tab5:
    st.header("🍰 Sweet Cravings")
    st.write("Special Desserts coming soon to this restaurant!")