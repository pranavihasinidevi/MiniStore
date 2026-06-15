"""
pages/1_Support_Chatbot.py
===========================
MiniStore AI Support Chatbot — powered by OpenAI GPT.
- Uses st.secrets["OPENAI_API_KEY"]
- System prompt includes full product catalogue
- Restricted to store-related topics only
- Chat history stored in st.session_state
"""

import streamlit as st
from openai import OpenAI

# ══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MiniStore — AI Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════
# PRODUCT CATALOGUE — must match homepage exactly
# ══════════════════════════════════════════════════════════════════════════
PRODUCTS = [
    {"name":"AirPods Pro Max",        "category":"Electronics",    "price":4999,  "old_price":6999,  "rating":4.8, "reviews":1240, "desc":"Premium noise-cancelling wireless headphones with 30-hour battery and Hi-Fi sound."},
    {"name":"Smart Watch Series X",   "category":"Electronics",    "price":3499,  "old_price":4299,  "rating":4.6, "reviews":890,  "desc":"Health monitoring, GPS tracking, 7-day battery life and AMOLED display."},
    {"name":"Running Shoes Pro",      "category":"Fashion",        "price":1299,  "old_price":1999,  "rating":4.5, "reviews":2103, "desc":"Lightweight mesh upper, cushioned sole, ideal for daily runs and gym workouts."},
    {"name":"Mechanical Keyboard RGB","category":"Electronics",    "price":2199,  "old_price":2799,  "rating":4.7, "reviews":567,  "desc":"Cherry MX Blue switches, full RGB backlight, aluminium frame and USB-C connection."},
    {"name":"Leather Backpack",       "category":"Fashion",        "price":899,   "old_price":1299,  "rating":4.4, "reviews":435,  "desc":"Genuine leather, padded laptop sleeve up to 15\", multiple compartments."},
    {"name":"Yoga Mat Premium",       "category":"Sports",         "price":599,   "old_price":799,   "rating":4.9, "reviews":3210, "desc":"6mm eco-friendly TPE foam, non-slip surface, carrying strap included."},
    {"name":"Coffee Maker Deluxe",    "category":"Home & Kitchen", "price":1799,  "old_price":2299,  "rating":4.6, "reviews":788,  "desc":"12-cup drip coffee maker with built-in grinder and programmable timer."},
    {"name":"Skincare Glow Set",      "category":"Beauty",         "price":1199,  "old_price":1699,  "rating":4.8, "reviews":1560, "desc":"5-piece vitamin C serum, moisturiser, eye cream, toner and face wash set."},
    {"name":"Wireless Charger Pad",   "category":"Electronics",    "price":499,   "old_price":799,   "rating":4.3, "reviews":302,  "desc":"15W fast Qi wireless charging pad for all smartphones and earbuds."},
    {"name":"Dumbbell Set 10kg",      "category":"Sports",         "price":1099,  "old_price":1499,  "rating":4.7, "reviews":921,  "desc":"Hex dumbbells, anti-roll design, rubber-coated for floor protection."},
    {"name":"Stainless Steel Bottle", "category":"Home & Kitchen", "price":349,   "old_price":499,   "rating":4.9, "reviews":4500, "desc":"1-litre vacuum insulated bottle — cold 24h, hot 12h."},
    {"name":"Perfume Noir Edition",   "category":"Beauty",         "price":2499,  "old_price":3299,  "rating":4.5, "reviews":678,  "desc":"100ml EDP with oud, sandalwood and amber notes. Luxury packaging."},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD PRODUCT CATALOGUE TEXT for the system prompt
# ══════════════════════════════════════════════════════════════════════════
def build_catalogue_text() -> str:
    """Convert product list into a readable text block for the system prompt."""
    lines = []
    for p in PRODUCTS:
        discount = round((1 - p["price"] / p["old_price"]) * 100)
        lines.append(
            f"• {p['name']} | Category: {p['category']} | "
            f"Price: ₹{p['price']:,} (was ₹{p['old_price']:,}, {discount}% off) | "
            f"Rating: {p['rating']}/5 ({p['reviews']:,} reviews) | "
            f"Description: {p['desc']}"
        )
    return "\n".join(lines)

CATALOGUE_TEXT = build_catalogue_text()

# ══════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT — defines Mia's personality, knowledge, and scope
# ══════════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = f"""
You are Mia, a professional and friendly AI customer support representative for MiniStore — 
an online e-commerce store based in India.

## YOUR ROLE
You help customers with:
- Product information, recommendations, comparisons, and availability
- Order placement, order status, and order cancellation
- Delivery timelines, tracking, express options, and pin code coverage
- Returns — policy, eligibility, process, and step-by-step instructions
- Refunds — timeline, methods, and status
- Payment methods — UPI, cards, COD, EMI, wallets, and security
- Offers, discounts, coupon codes, and promotions
- Warranty and damaged product claims
- General MiniStore policies and contact information

## SCOPE RESTRICTION — VERY IMPORTANT
You ONLY answer questions related to MiniStore and shopping.
If a user asks about ANYTHING unrelated to the store (e.g., general knowledge, 
politics, coding, recipes, sports, science, news, math, etc.), 
politely decline and redirect them. Example redirect:
"I'm Mia, MiniStore's support assistant! I can only help with shopping-related 
questions. Is there anything about our products, orders, or delivery I can help you with? 😊"

## TONE & STYLE
- Warm, professional, and concise
- Use emojis occasionally but not excessively
- Use bullet points for multi-step answers
- Always end with a helpful follow-up offer when appropriate
- Address the customer politely — use "you" not "the customer"

## STORE POLICIES
- Free delivery on orders above ₹999; standard delivery fee ₹49 below ₹999
- Standard delivery: 3–5 business days
- Express delivery: 1–2 business days (+₹99 extra)
- Same-day delivery available in Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune (+₹149)
- 30-day hassle-free returns from delivery date (item must be unused, original packaging)
- Free return pickup from doorstep
- Refunds processed within 5–7 business days (bank/card) or 24 hours (MiniStore Wallet)
- Payment methods: UPI (GPay, PhonePe, Paytm), Credit/Debit Cards, Net Banking, COD (up to ₹10,000, +₹25 fee), EMI (no-cost on orders above ₹1,999), MiniStore Wallet
- Warranty: Electronics 1 year, Fashion/Sports/Beauty 6 months, Home & Kitchen 1 year
- Support: 1800-123-MINI (toll-free, 24/7), support@ministore.in
- Coupon codes: MINI100 (₹100 off above ₹999), FIRST50 (50% off first order, max ₹200), UPIBACK (5% UPI cashback), WELCOME10 (10% off for new users)

## PRODUCT CATALOGUE
MiniStore currently sells 12 products across 5 categories 
(Electronics, Fashion, Sports, Home & Kitchen, Beauty):

{CATALOGUE_TEXT}

## RESPONSE FORMAT
- Keep answers concise but complete
- For product comparisons, use a simple table or bullet list
- For multi-step processes, use numbered steps
- Always mention prices in Indian Rupees (₹)
- If unsure about something not in your knowledge, say so honestly and 
  direct the customer to call 1800-123-MINI or email support@ministore.in
"""

# ══════════════════════════════════════════════════════════════════════════
# OPENAI CLIENT — reads key from st.secrets
# ══════════════════════════════════════════════════════════════════════════
@st.cache_resource
def get_openai_client():
    """
    Initialise OpenAI client once and cache it.
    API key is read from .streamlit/secrets.toml:
        [secrets]
        OPENAI_API_KEY = "sk-..."
    """
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
    except KeyError:
        st.error(
            "⚠️ **OpenAI API key not found.**\n\n"
            "Please add your key to `.streamlit/secrets.toml`:\n\n"
            "```toml\n[secrets]\nOPENAI_API_KEY = \"sk-your-key-here\"\n```\n\n"
            "Get your key at: https://platform.openai.com/api-keys"
        )
        st.stop()

client = get_openai_client()

# ══════════════════════════════════════════════════════════════════════════
# GET AI RESPONSE — sends history to OpenAI GPT
# ══════════════════════════════════════════════════════════════════════════
def get_ai_response(chat_history: list) -> str:
    """
    Send the full conversation history to OpenAI and return the assistant reply.
    The system prompt is always prepended as the first message.
    
    Args:
        chat_history: list of {"role": "user"|"assistant", "content": "..."}
    
    Returns:
        str: The assistant's reply text
    """
    # Build messages array: system prompt first, then conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",     # cost-effective, fast, great for support
            messages=messages,
            max_tokens=600,          # keep responses concise
            temperature=0.4,         # slightly creative but mostly factual
            stream=False,
        )
        return response.choices[0].message.content

    except Exception as e:
        error_str = str(e)
        # Handle common OpenAI errors with friendly messages
        if "insufficient_quota" in error_str or "billing" in error_str.lower():
            return (
                "⚠️ I'm temporarily unavailable due to API quota limits. "
                "Please contact us directly:\n\n"
                "📞 **1800-123-MINI** (toll-free)\n"
                "📧 **support@ministore.in**"
            )
        if "invalid_api_key" in error_str or "Incorrect API key" in error_str:
            return (
                "⚠️ There's an issue with my configuration. "
                "Please contact support:\n\n"
                "📞 **1800-123-MINI**\n"
                "📧 **support@ministore.in**"
            )
        if "rate_limit" in error_str:
            return (
                "⏳ I'm receiving too many requests right now. "
                "Please wait a moment and try again!"
            )
        # Generic fallback
        return (
            f"⚠️ I encountered an error: `{error_str[:120]}`\n\n"
            "Please try again or contact support at **1800-123-MINI**."
        )

# ══════════════════════════════════════════════════════════════════════════
# CSS — chatbot page styling
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
  .block-container { padding-top: 1rem !important; }
  #MainMenu, footer, header { visibility: hidden; }

  /* Header banner */
  .chat-header {
    background: linear-gradient(135deg,#6C5CE7 0%,#0984E3 100%);
    border-radius: 16px; padding: 24px 32px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 20px;
  }
  .bot-avatar {
    width: 64px; height: 64px; border-radius: 50%;
    background: rgba(255,255,255,0.20);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; flex-shrink: 0;
  }
  .chat-header-text h2 { color: #FFF; font-size: 22px; font-weight: 700; margin: 0 0 4px; }
  .chat-header-text p  { color: rgba(255,255,255,0.82); font-size: 13px; margin: 0; }
  .status-dot {
    display: inline-block; width: 8px; height: 8px;
    background: #00B894; border-radius: 50%; margin-right: 6px;
  }
  .openai-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.30);
    color: #FFF; font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px; margin-top: 6px;
  }

  /* Quick chips */
  .stButton > button {
    background: #F0EDFF !important; color: #6C5CE7 !important;
    border: 1.5px solid #DDD8FF !important; border-radius: 20px !important;
    font-size: 12px !important; font-weight: 600 !important;
    padding: 4px 12px !important;
    transition: all 0.15s !important;
  }
  .stButton > button:hover {
    background: #6C5CE7 !important; color: white !important;
  }

  /* Sidebar buttons override */
  section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg,#6C5CE7,#0984E3) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important;
  }

  /* Info cards in sidebar */
  .info-card {
    background: #F8F7FF; border-radius: 10px;
    padding: 12px 14px; margin-bottom: 10px;
    border-left: 3px solid #6C5CE7;
  }
  .info-card-title { font-size: 10px; font-weight: 700; color: #6C5CE7; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  .info-card-body  { font-size: 12px; color: #2D3436; line-height: 1.55; }

  /* Pricing tip box */
  .product-tip {
    background: #E1F5EE; border-radius: 10px;
    padding: 10px 14px; margin-bottom: 8px;
    border-left: 3px solid #00B894;
    font-size: 12px; color: #085041; line-height: 1.5;
  }

  /* Token counter */
  .token-info {
    font-size: 11px; color: #B2BEC3;
    text-align: center; padding: 4px 0;
  }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE — chat history & message counter
# ══════════════════════════════════════════════════════════════════════════
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # stores {"role":..., "content":...} dicts

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:8px 0 16px;'>
      <div style='font-size:40px; margin-bottom:4px;'>🛍️</div>
      <div style='font-size:20px; font-weight:800; color:#6C5CE7;'>MiniStore</div>
      <div style='font-size:11px; color:#636E72;'>AI Support Center</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Back to homepage
    if st.button("🏠 Back to Shop", use_container_width=True):
        st.switch_page("app.py")

    st.markdown("<br>", unsafe_allow_html=True)

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history  = []
        st.session_state.message_count = 0
        st.toast("Chat cleared!", icon="🗑️")
        st.rerun()

    st.markdown("---")

    # Message counter
    st.markdown(f"""
    <div class='token-info'>
      💬 {st.session_state.message_count} message(s) in this session
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Info cards
    st.markdown("""
    <div class='info-card'>
      <div class='info-card-title'>🤖 About Mia (AI)</div>
      <div class='info-card-body'>Powered by OpenAI GPT-4o Mini. Knows all 12 MiniStore products and store policies. Available 24/7.</div>
    </div>
    <div class='info-card'>
      <div class='info-card-title'>📞 Human Support</div>
      <div class='info-card-body'>1800-123-MINI (toll-free)<br>support@ministore.in<br>Mon–Sat, 9 AM – 9 PM IST</div>
    </div>
    <div class='info-card'>
      <div class='info-card-title'>🔒 Privacy</div>
      <div class='info-card-body'>Chat is not stored permanently. Session ends when you close the browser tab.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Product quick lookup
    st.markdown("**🔍 Quick Product Ask**")
    lookup = st.selectbox(
        "Product:",
        ["-- Select --"] + [p["name"] for p in PRODUCTS],
        label_visibility="collapsed",
    )
    if lookup != "-- Select --":
        if st.button("Ask about this product", use_container_width=True):
            question = f"Tell me about the {lookup} — price, features, and rating."
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Mia is typing…"):
                reply = get_ai_response(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.message_count += 1
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# MAIN CHAT AREA
# ══════════════════════════════════════════════════════════════════════════

# Chat header
st.markdown("""
<div class='chat-header'>
  <div class='bot-avatar'>🤖</div>
  <div class='chat-header-text'>
    <h2>Mia — MiniStore AI Support</h2>
    <p>
      <span class='status-dot'></span>Online · Powered by OpenAI · 
      Knows all 12 products & store policies
    </p>
    <span class='openai-badge'>✨ GPT-4o Mini</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Quick reply chips ─────────────────────────────────────────────────────
st.markdown("**💡 Quick Questions — click to ask:**")
QUICK_QUESTIONS = [
    ("📦 All Products",      "What products does MiniStore sell? List all categories."),
    ("🚚 Delivery Time",     "How long does standard delivery take and what are my options?"),
    ("🔄 Return Policy",     "What is MiniStore's return policy and how do I return something?"),
    ("💳 Payment Methods",   "What payment methods does MiniStore accept?"),
    ("💰 Refund Timeline",   "How long does a refund take after I return a product?"),
    ("🎉 Discount Codes",    "What discount codes or offers are currently available?"),
    ("⭐ Best Products",     "What are the top rated products at MiniStore?"),
    ("🛡️ Warranty Info",    "What warranty do products come with?"),
]

chip_cols = st.columns(4)
for i, (label, question) in enumerate(QUICK_QUESTIONS):
    with chip_cols[i % 4]:
        if st.button(label, key=f"chip_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Mia is typing…"):
                reply = get_ai_response(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.message_count += 1
            st.rerun()

st.markdown("---")

# ── Welcome message shown before any chat ────────────────────────────────
if not st.session_state.chat_history:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            "👋 Hi! I'm **Mia**, MiniStore's AI support assistant — powered by OpenAI!\n\n"
            "I can help you with:\n"
            "🛍️ **Products** — prices, features, comparisons, recommendations\n"
            "🚚 **Delivery** — timelines, tracking, express options\n"
            "🔄 **Returns** — policy, eligibility, step-by-step process\n"
            "💰 **Refunds** — timeline and methods\n"
            "💳 **Payments** — UPI, cards, COD, EMI, wallets\n"
            "📋 **Orders** — placement, tracking, cancellation\n"
            "🎉 **Offers** — discount codes and promotions\n\n"
            "What can I help you with today? 😊"
        )

# ── Render chat history ───────────────────────────────────────────────────
for message in st.session_state.chat_history:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ── Chat input ────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask Mia anything about MiniStore… 💬")

if user_input:
    # 1. Show user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # 2. Add to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # 3. Get AI response with spinner
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Mia is thinking…"):
            bot_reply = get_ai_response(st.session_state.chat_history)
        st.markdown(bot_reply)

    # 4. Save reply to history and increment counter
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.session_state.message_count += 1

    # 5. Rerun to refresh UI cleanly
    st.rerun()