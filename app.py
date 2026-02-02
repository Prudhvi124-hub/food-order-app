import streamlit as st
import pandas as pd
import random
import os

# 1. PAGE SETUP
st.set_page_config(page_title="DesiBites | Smart Menu", layout="wide")

# Initialize Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 2. LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv("data/menu_data.csv")

df_master = load_data()

# 3. SIDEBAR: Restaurant Selection & Persistent Cart
with st.sidebar:
    st.title("🛵 DesiBites")
    res_list = ["Biryani Bliss", "Masala Leaf", "Tandoor Bites", "Chulha Chauki", "Waffle Wagon", "Curry Flame"]
    selected_res = st.selectbox("Select Restaurant", res_list)
    
    st.divider()
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        for item in st.session_state.cart:
            st.write(f"✅ {item['name']} - ₹{item['price']}")
        
        if st.button("🗑️ Clear All"):
            st.session_state.cart = []
            st.rerun()

# 4. JUMBLING LOGIC
random.seed(selected_res) 
categories = list(df_master['category'].unique())

st.title(f"Welcome to {selected_res}")
st.caption(f"Showing jumbled menu for {selected_res}")

# 5. DISPLAY JUMBLED MENU IN TABS
tabs = st.tabs(categories)

for i, cat in enumerate(categories):
    with tabs[i]:
        cat_items = df_master[df_master['category'] == cat].to_dict('records')
        random.shuffle(cat_items)
        
        for item in cat_items:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{item['symbol']} {item['name']}**")
            with col2:
                st.write(f"₹{item['price']}")
            with col3:
                if st.button("ADD", key=f"{selected_res}_{item['name']}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']}!")
                    st.rerun()

# 6. BILLING & UPI PAYMENT SECTION
if st.session_state.cart:
    st.divider()
    st.header("🏁 Checkout & Payment")
    
    c1, c2 = st.columns(2)
    
    with c1:
        subtotal = sum(i['price'] for i in st.session_state.cart)
        gst = subtotal * 0.05
        delivery = 45
        # We round to 2 decimals so the UPI app accepts the number
        total = round(subtotal + gst + delivery, 2)
        
        st.write(f"Items Total: ₹{subtotal}")
        st.write(f"GST (5%): ₹{gst:.2f}")
        st.write(f"Delivery: ₹{delivery}")
        st.error(f"### Amount to Pay: ₹{total}")
    
    with c2:
        st.subheader("Payment Method")
        method = st.radio("Pay via:", ["UPI (PhonePe/GPay/Paytm)", "Cash on Delivery"])
        
        if method == "UPI (PhonePe/GPay/Paytm)":
            upi_id = "prudhvidaggumati@ybl" 
            
            # --- THE MAGIC LINK ---
            # am={total} sends the amount directly to the scanner
            upi_data = f"upi://pay?pa={upi_id}&pn=DesiBites&am={total}&cu=INR"
            
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={upi_data}"
            
            st.image(qr_url, caption=f"Scan to pay ₹{total} to {upi_id}")
        
        if st.button("CONFIRM ORDER", type="primary", use_container_width=True):
            st.balloons()
            st.success("Order Placed! Preparing your food...")
            st.session_state.cart = []