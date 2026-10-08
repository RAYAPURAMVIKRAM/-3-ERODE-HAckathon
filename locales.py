TRANSLATIONS = {
    "English": {
        "lang_name": "English",
        "app_title": "STARK-X | Autonomous Agriculture",
        "chat_page": "Agri Chat",
        "vision_page": "Crop Vision",
        "opt_page": "Optimizer",
        "market_page": "Direct Market",
        "chat_title": "🌱 STARK-X Agri Advisor",
        "chat_status": "🟢 Online | Multilingual Farming Desk",
        "chat_welcome": "Vanakkam! I am your STARK-X advisor. Ask me anything about soil, crops, water, or pests in your language.",
        "chat_placeholder": "Ask your crop question here...",
        "vision_title": "📸 Crop Vision Studio",
        "vision_desc": "Upload a crop photo to detect diseases and get treatment advice.",
        "vision_btn": "🔍 Analyze Crop Health",
        "opt_title": "🌾 STARK-X Crop Optimizer",
        "opt_tab1": "🎯 Recommend Crop",
        "opt_tab2": "🔍 Evaluate My Crop",
        "soil_label": "Soil Type",
        "water_label": "Water Availability",
        "opt_btn": "🚀 Run STARK-X Algorithm",
        "market_title": "🛒 Direct Farmer Marketplace",
        "market_sub": "Bypass middlemen. Sell directly to buyers via WhatsApp.",
        "post_btn": "➕ Post Your Harvest",
        "wa_btn": "💬 Buy via WhatsApp"
    },
    "Tamil (தமிழ்)": {
        "lang_name": "Tamil",
        "app_title": "STARK-X | நவீன விவசாய தளம்",
        "chat_page": "விவசாய அரட்டை",
        "vision_page": "பயிர் பார்வை",
        "opt_page": "பயிர் தேர்வு",
        "market_page": "நேரடி சந்தை",
        "chat_title": "🌱 STARK-X விவசாய ஆலோசகர்",
        "chat_status": "🟢 நேரலையில் | பலமொழி வேளாண் மையம்",
        "chat_welcome": "வணக்கம்! நான் உங்கள் STARK-X விவசாய ஆலோசகர். மண், பயிர், நீர் மற்றும் பூச்சி மேலாண்மை பற்றி உங்கள் மொழியில் கேளுங்கள்.",
        "chat_placeholder": "உங்கள் விவசாய கேள்வியை இங்கே கேட்கவும்...",
        "vision_title": "📸 பயிர் நோய் கண்டறியும் மையம்",
        "vision_desc": "நோய்களைக் கண்டறிந்து தீர்வு பெற பயிர் இலையின் புகைப்படத்தை பதிவேற்றவும்.",
        "vision_btn": "🔍 பயிரை ஆய்வு செய்",
        "opt_title": "🌾 STARK-X பயிர் தேர்வு வழிகாட்டி",
        "opt_tab1": "🎯 சிறந்த பயிரைத் தேர்ந்தெடு",
        "opt_tab2": "🔍 எனது பயிரை சரிபார்",
        "soil_label": "மண் வகை",
        "water_label": "நீர் ஆதாரம்",
        "opt_btn": "🚀 பொருத்தத்தை கணக்கிடு",
        "market_title": "🛒 நேரடி உழவர் சந்தை",
        "market_sub": "தரகர்கள் இன்றி நேரடியாக வாட்ஸ்அப் மூலம் நுகர்வோருக்கு விற்கவும்.",
        "post_btn": "➕ உங்கள் விளைச்சலை பதிவிடவும்",
        "wa_btn": "💬 வாட்ஸ்அப் மூலம் வாங்க"
    },
    "Telugu (తెలుగు)": {
        "lang_name": "Telugu",
        "app_title": "STARK-X | ఆధునిక వ్యవసాయ వేదిక",
        "chat_page": "రైతు సలహా",
        "vision_page": "పంట పరీక్ష",
        "opt_page": "పంట ఎంపిక",
        "market_page": "రైతు మార్కెట్",
        "chat_title": "🌱 STARK-X రైతు సలహాదారు",
        "chat_status": "🟢 ఆన్లైన్ | బహుభాషా వ్యవసాయ కేంద్రం",
        "chat_welcome": "నమస్కారం! నేను మీ STARK-X వ్యవసాయ సలహాదారుని. నేల, పంట, నీరు లేదా తెగుళ్ల గురించి మీ భాషలోనే అడగండి.",
        "chat_placeholder": "మీ పంట సందేహాన్ని ఇక్కడ టైప్ చేయండి...",
        "vision_title": "📸 పంట వ్యాధి నిర్ధారణ విభాగం",
        "vision_desc": "వ్యాధులను గుర్తించడానికి పంట ఆకు ఫోటోను అప్లోడ్ చేయండి.",
        "vision_btn": "🔍 పంటను పరీక్షించండి",
        "opt_title": "🌾 STARK-X పంట ఆప్టిమైజర్",
        "opt_tab1": "🎯 సరైన పంట సిఫార్సు",
        "opt_tab2": "🔍 నా పంటను పరీక్షించు",
        "soil_label": "నేల రకం",
        "water_label": "నీటి వసతి",
        "opt_btn": "🚀 అనుకూలతను లెక్కించండి",
        "market_title": "🛒 రైతు ప్రత్యక్ష మార్కెట్",
        "market_sub": "దళారులు లేకుండా నేరుగా వాట్సాప్ ద్వారా విక్రయించండి.",
        "post_btn": "➕ మీ పంటను నమోదు చేయండి",
        "wa_btn": "💬 వాట్సాప్ ద్వారా కొనండి"
    }
}

def t(key, lang=None):
    """Returns localized string from dictionary using session state or explicit lang."""
    if lang is None:
        try:
            import streamlit as st
            lang = st.session_state.get("selected_lang", "English")
        except Exception:
            lang = "English"
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)
