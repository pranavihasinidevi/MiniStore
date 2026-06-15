"""
MiniStore v3 — Multipage E-Commerce App
========================================
Main homepage — products, cart, categories.
Run with: streamlit run app.py
"""

import streamlit as st

# ══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MiniStore — Shop Smart",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════
# PRODUCT CATALOGUE — shared with chatbot via session_state
# ══════════════════════════════════════════════════════════════════════════
PRODUCTS = [
    {"id":1,  "name":"AirPods Pro Max",        "category":"Electronics",   "emoji":"🎧", "price":4999,  "old_price":6999,  "desc":"Premium noise-cancelling wireless headphones with 30-hour battery and Hi-Fi sound.", "rating":4.8,"reviews":1240,"tag":"Best Seller","tag_color":"#6C5CE7","bg":"#F0EDFF"},
    {"id":2,  "name":"Smart Watch Series X",   "category":"Electronics",   "emoji":"⌚", "price":3499,  "old_price":4299,  "desc":"Health monitoring, GPS tracking, 7-day battery life and AMOLED display.",            "rating":4.6,"reviews":890, "tag":"New",         "tag_color":"#00B894","bg":"#E1F5EE"},
    {"id":3,  "name":"Running Shoes Pro",       "category":"Fashion",       "emoji":"👟", "price":1299,  "old_price":1999,  "desc":"Lightweight mesh upper, cushioned sole, ideal for daily runs and gym workouts.",       "rating":4.5,"reviews":2103,"tag":"35% Off",     "tag_color":"#D63031","bg":"#FFF5F5"},
    {"id":4,  "name":"Mechanical Keyboard RGB", "category":"Electronics",   "emoji":"⌨️","price":2199,  "old_price":2799,  "desc":"Cherry MX Blue switches, full RGB backlight, aluminium frame and USB-C.",              "rating":4.7,"reviews":567, "tag":"Top Rated",   "tag_color":"#0984E3","bg":"#E8F4FD"},
    {"id":5,  "name":"Leather Backpack",        "category":"Fashion",       "emoji":"🎒", "price":899,   "old_price":1299,  "desc":"Genuine leather, padded laptop sleeve up to 15\", multiple compartments.",            "rating":4.4,"reviews":435, "tag":"Trending",    "tag_color":"#E17055","bg":"#FFF3EE"},
    {"id":6,  "name":"Yoga Mat Premium",        "category":"Sports",        "emoji":"🧘", "price":599,   "old_price":799,   "desc":"6mm eco-friendly TPE foam, non-slip surface, carrying strap included.",               "rating":4.9,"reviews":3210,"tag":"Eco-Friendly","tag_color":"#00B894","bg":"#E1F5EE"},
    {"id":7,  "name":"Coffee Maker Deluxe",     "category":"Home & Kitchen","emoji":"☕", "price":1799,  "old_price":2299,  "desc":"12-cup drip coffee maker with built-in grinder and programmable timer.",              "rating":4.6,"reviews":788, "tag":"Popular",     "tag_color":"#FDCB6E","bg":"#FFFBEA"},
    {"id":8,  "name":"Skincare Glow Set",       "category":"Beauty",        "emoji":"✨", "price":1199,  "old_price":1699,  "desc":"5-piece vitamin C serum, moisturiser, eye cream, toner and face wash set.",          "rating":4.8,"reviews":1560,"tag":"Gift Set",    "tag_color":"#FD79A8","bg":"#FFF0F6"},
    {"id":9,  "name":"Wireless Charger Pad",    "category":"Electronics",   "emoji":"🔋", "price":499,   "old_price":799,   "desc":"15W fast Qi wireless charging pad for smartphones and earbuds.",                     "rating":4.3,"reviews":302, "tag":"Under ₹500",  "tag_color":"#6C5CE7","bg":"#F0EDFF"},
    {"id":10, "name":"Dumbbell Set 10kg",        "category":"Sports",        "emoji":"🏋️","price":1099,  "old_price":1499,  "desc":"Adjustable hex dumbbells, rubber-coated for floor protection.",                       "rating":4.7,"reviews":921, "tag":"Gym Essential","tag_color":"#E17055","bg":"#FFF3EE"},
    {"id":11, "name":"Stainless Steel Bottle",  "category":"Home & Kitchen","emoji":"💧", "price":349,   "old_price":499,   "desc":"1-litre vacuum insulated — keeps drinks cold 24h or hot 12h.",                       "rating":4.9,"reviews":4500,"tag":"#1 Rated",    "tag_color":"#00B894","bg":"#E1F5EE"},
    {"id":12, "name":"Perfume Noir Edition",    "category":"Beauty",        "emoji":"🌸", "price":2499,  "old_price":3299,  "desc":"100ml EDP with oud, sandalwood and amber notes. Luxury packaging.",                  "rating":4.5,"reviews":678, "tag":"Luxury",      "tag_color":"#FD79A8","bg":"#FFF0F6"},
]

ALL_CATEGORIES = ["All"] + sorted(set(p["category"] for p in PRODUCTS))

# Store products in session_state so chatbot page can access them
if "products" not in st.session_state:
    st.session_state.products = PRODUCTS

# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"

# ══════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
  .block-container { padding-top: 1rem !important; }
  #MainMenu, footer, header { visibility: hidden; }

  .hero {
    background: linear-gradient(135deg, #6C5CE7 0%, #0984E3 50%, #00B894 100%);
    border-radius: 16px; padding: 48px 40px; margin-bottom: 32px; text-align: center;
  }
  .hero h1 { font-size: 48px; font-weight: 800; color: #FFF; margin: 0 0 8px; }
  .hero p  { font-size: 18px; color: rgba(255,255,255,0.88); margin: 0 0 24px; }
  .hero-badge {
    display: inline-block; background: rgba(255,255,255,0.20);
    border: 1px solid rgba(255,255,255,0.35); color: #FFF;
    font-size: 13px; font-weight: 600; padding: 6px 18px;
    border-radius: 30px; margin: 0 6px 8px;
  }
  .stat-box { background:#F8F7FF; border-radius:12px; padding:16px; text-align:center; }
  .stat-num { font-size:28px; font-weight:800; color:#6C5CE7; margin:0; }
  .stat-label { font-size:12px; color:#636E72; margin:2px 0 0; }
  .section-header { font-size:24px; font-weight:700; color:#1a1a2e; margin:8px 0 4px; }
  .section-sub { font-size:14px; color:#636E72; margin:0 0 20px; }
  .product-card {
    background:#FFF; border:1px solid #E8E8F0; border-radius:14px;
    margin-bottom:20px; overflow:hidden;
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .product-card:hover { box-shadow:0 8px 32px rgba(108,92,231,0.15); transform:translateY(-3px); }
  .product-emoji-box {
    width:100%; height:160px;
    display:flex; align-items:center; justify-content:center; font-size:72px;
  }
  .product-body { padding:0 16px; }
  .product-category { font-size:10px; font-weight:600; letter-spacing:0.8px; text-transform:uppercase; color:#6C5CE7; margin-bottom:4px; }
  .product-name { font-size:15px; font-weight:700; color:#1a1a2e; margin:0 0 6px; line-height:1.3; }
  .product-desc { font-size:12.5px; color:#636E72; line-height:1.5; margin-bottom:12px; min-height:48px; }
  .product-footer { display:flex; align-items:center; justify-content:space-between; padding:0 16px 16px; }
  .product-price { font-size:20px; font-weight:800; color:#00B894; }
  .product-price-old { font-size:12px; color:#B2BEC3; text-decoration:line-through; margin-left:4px; }
  .product-rating { font-size:12px; color:#FDCB6E; }
  .stButton > button {
    background: linear-gradient(135deg,#6C5CE7,#0984E3) !important;
    color:white !important; border:none !important;
    border-radius:8px !important; font-weight:600 !important;
    font-size:13px !important; width:100% !important;
  }
  .cart-item {
    background:#F8F7FF; border-radius:10px;
    padding:10px 14px; margin-bottom:8px;
    display:flex; justify-content:space-between; align-items:center;
  }
  .cart-item-name  { font-size:13px; font-weight:600; color:#1a1a2e; }
  .cart-item-price { font-size:13px; font-weight:700; color:#6C5CE7; }
  .cart-total {
    background: linear-gradient(135deg,#6C5CE7,#0984E3);
    color:white; border-radius:10px; padding:14px;
    text-align:center; font-size:16px; font-weight:700; margin-top:12px;
  }
  .cart-empty { text-align:center; color:#B2BEC3; font-size:13px; padding:20px 0; }
  .newsletter {
    background:#1a1a2e; border-radius:14px;
    padding:32px 40px; text-align:center; margin-top:32px;
  }
  .newsletter h3 { color:#FFF; font-size:22px; font-weight:700; margin:0 0 6px; }
  .newsletter p  { color:#B2BEC3; font-size:14px; margin:0 0 18px; }

  /* ── Floating chat button ── */
  .float-chat-btn {
    position:fixed; bottom:28px; right:28px; z-index:9999;
    background: linear-gradient(135deg,#6C5CE7,#0984E3);
    color:white; border:none; border-radius:50px;
    padding:14px 22px; font-size:15px; font-weight:700;
    cursor:pointer; display:flex; align-items:center; gap:8px;
    box-shadow:0 6px 24px rgba(108,92,231,0.45);
    text-decoration:none;
    animation: float-pulse 2.5s ease-in-out infinite;
  }
  .float-chat-btn:hover {
    transform:translateY(-3px) scale(1.04);
    box-shadow:0 10px 32px rgba(108,92,231,0.65);
    color:white; text-decoration:none;
  }
  @keyframes float-pulse {
    0%,100% { box-shadow:0 6px 24px rgba(108,92,231,0.45); }
    50%      { box-shadow:0 8px 32px rgba(108,92,231,0.70); }
  }
  .chat-badge {
    background:#D63031; color:white; font-size:10px; font-weight:800;
    border-radius:50%; width:18px; height:18px;
    display:flex; align-items:center; justify-content:center;
  }
  /* Hide the nav trigger button completely */
  div[data-testid="stButton"]:has(button[kind="secondary"]#chat-nav-trigger) { display:none; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:8px 0 20px;'>
      <div style='font-size:40px; margin-bottom:4px;'>🛍️</div>
      <div style='font-size:22px; font-weight:800; color:#6C5CE7;'>MiniStore</div>
      <div style='font-size:12px; color:#636E72;'>Shop Smart. Live Better.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🗂️ Browse Categories**")
    for cat in ALL_CATEGORIES:
        active = st.session_state.selected_category == cat
        label  = f"{'✅ ' if active else ''}{cat}"
        if st.button(label, key=f"cat_{cat}", use_container_width=True):
            st.session_state.selected_category = cat
            st.rerun()
    st.markdown("---")
    st.markdown("**🛒 Shopping Cart**")
    if not st.session_state.cart:
        st.markdown("<div class='cart-empty'>🛒<br>Your cart is empty.</div>", unsafe_allow_html=True)
    else:
        total = 0
        for item in st.session_state.cart:
            st.markdown(f"""
            <div class='cart-item'>
              <div>
                <div class='cart-item-name'>{item['emoji']} {item['name']}</div>
                <div style='font-size:11px;color:#636E72;'>{item['category']}</div>
              </div>
              <div class='cart-item-price'>₹{item['price']:,}</div>
            </div>""", unsafe_allow_html=True)
            total += item["price"]
        st.markdown(f"""
        <div class='cart-total'>
          🛍️ Total: ₹{total:,}<br>
          <span style='font-size:11px;font-weight:400;opacity:0.85;'>{len(st.session_state.cart)} item(s)</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            if st.button("✅ Checkout", use_container_width=True):
                st.success("Order placed! 🎉")
                st.session_state.cart = []
                st.rerun()
        with cb:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px;color:#636E72;line-height:1.8;'>
      🚚 <b>Free delivery</b> above ₹999<br>
      🔄 <b>Easy returns</b> within 30 days<br>
      🔒 <b>Secure payments</b> guaranteed<br>
      ⭐ <b>4.8★</b> average customer rating
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**💬 Need Help?**")
    st.markdown("""
    <div style='font-size:12px;color:#636E72;margin-bottom:10px;'>
      Chat with Mia — our AI support assistant powered by OpenAI.
    </div>""", unsafe_allow_html=True)

    # ── Sidebar chat button — uses plain ASCII page name ──
    if st.button("🤖 Open AI Support Chat", use_container_width=True):
        st.switch_page("pages/1_Support_Chatbot.py")   # ← NO emoji in path

# ══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='hero'>
  <h1>🛍️ Welcome to MiniStore</h1>
  <p>Discover amazing products at unbeatable prices — curated just for you.</p>
  <span class='hero-badge'>🚚 Free Delivery</span>
  <span class='hero-badge'>🔄 Easy Returns</span>
  <span class='hero-badge'>🔒 Secure Checkout</span>
  <span class='hero-badge'>⭐ Top Brands</span>
</div>""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
for col, num, label in zip([s1,s2,s3,s4],
    ["500+","50K+","4.8★","30-Day"],
    ["Products","Happy Customers","Avg Rating","Easy Returns"]):
    with col:
        st.markdown(f"""
        <div class='stat-box'>
          <p class='stat-num'>{num}</p>
          <p class='stat-label'>{label}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

active_cat = st.session_state.selected_category
filtered   = [p for p in PRODUCTS if active_cat == "All" or p["category"] == active_cat]
heading    = "🔥 All Products" if active_cat == "All" else f"🏷️ {active_cat}"

st.markdown(f"""
<div class='section-header'>{heading}</div>
<div class='section-sub'>{len(filtered)} products found</div>""", unsafe_allow_html=True)

for row_start in range(0, len(filtered), 3):
    row_products = filtered[row_start:row_start+3]
    cols = st.columns(3)
    for col, product in zip(cols, row_products):
        with col:
            st.markdown(f"""
            <div class='product-card'>
              <div class='product-emoji-box' style='background:{product["bg"]};'>{product["emoji"]}</div>
              <div class='product-body'>
                <div style='margin:12px 0 4px;'>
                  <span style='background:{product["tag_color"]}18;color:{product["tag_color"]};
                    font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;
                    border:1px solid {product["tag_color"]}33;'>{product["tag"]}</span>
                </div>
                <div class='product-category'>{product["category"]}</div>
                <div class='product-name'>{product["name"]}</div>
                <div class='product-desc'>{product["desc"]}</div>
              </div>
              <div class='product-footer'>
                <div>
                  <span class='product-price'>₹{product["price"]:,}</span>
                  <span class='product-price-old'>₹{product["old_price"]:,}</span>
                </div>
                <div class='product-rating'>⭐ {product["rating"]} ({product["reviews"]:,})</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button("🛒 Add to Cart", key=f"add_{product['id']}"):
                st.session_state.cart.append(product)
                st.toast(f"✅ {product['name']} added!", icon="🛍️")
                st.rerun()

st.markdown("""
<div class='newsletter'>
  <h3>📬 Get Exclusive Deals in Your Inbox</h3>
  <p>Subscribe and never miss a sale or new arrival.</p>
</div>""", unsafe_allow_html=True)

n1, n2, n3 = st.columns([1,2,1])
with n2:
    email = st.text_input("", placeholder="✉️  Enter your email address…", label_visibility="collapsed")
    if st.button("Subscribe Now 🚀", use_container_width=True):
        if email and "@" in email:
            st.success(f"🎉 Subscribed! Watch your inbox at {email}")
        else:
            st.error("Please enter a valid email address.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:20px 0;border-top:1px solid #E8E8F0;'>
  <div style='font-size:24px;margin-bottom:6px;'>🛍️</div>
  <div style='font-size:18px;font-weight:800;color:#6C5CE7;margin-bottom:4px;'>MiniStore</div>
  <div style='font-size:12px;color:#B2BEC3;'>© 2026 MiniStore · Built with Streamlit & OpenAI · Prices in INR (₹)</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# FLOATING CHAT BUTTON — navigates to chatbot page (plain ASCII filename)
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div id='float-btn-container'>
  <button class='float-chat-btn'
          onclick="document.getElementById('hidden-chat-btn').click()">
    💬 AI Support
    <span class='chat-badge'>AI</span>
  </button>
</div>
""", unsafe_allow_html=True)

# Hidden Streamlit button triggered by JS above
col_h = st.columns([1])[0]
with col_h:
    if st.button("go_to_chat", key="hidden-chat-btn"):
        st.switch_page("pages/1_Support_Chatbot.py")   # ← plain ASCII, no emoji