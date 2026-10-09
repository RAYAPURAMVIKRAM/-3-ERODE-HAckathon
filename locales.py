import streamlit as st

__all__ = ["LANGUAGE_COLORS", "TRANSLATIONS", "resolve_lang", "t", "get_lang_color"]

LANGUAGE_COLORS = {
    "English": "#2563eb",         # Royal Blue
    "Tamil (தமிழ்)": "#16a34a",   # Agricultural Emerald Green
    "Telugu (తెలుగు)": "#ea580c"   # Warm Harvest Amber/Orange
}

TRANSLATIONS = {
    "English": {
        "lang_name": "English",
        "lang_code": "en",
        "lang_badge": "🇬🇧 English",
        "lang_color": "#2563eb",
        "app_title": "STARK-X | Autonomous Agriculture",
        "app_subtitle": "The Ultimate Autonomous Farming Ecosystem",
        "select_tool_msg": "Select a tool below to get started:",
        "welcome_farmer": "Vanakkam, **{name}** ({village})! Your farmer profile is connected.",
        "chat_page": "Agri Chat",
        "chat_page_desc": "Talk to our AI about your farm (WhatsApp style)",
        "vision_page": "Crop Vision",
        "vision_page_desc": "Upload photos for instant health checks",
        "opt_page": "Optimizer",
        "opt_page_desc": "Find out exactly what to grow based on soil and water",
        "market_sos_page": "Market & SOS",
        "market_sos_desc": "Check live prices and request community help",
        "market_page": "Direct Market",
        "market_page_desc": "Direct harvest sales & mobile farming reels",
        
        # Agri Chat
        "chat_title": "🌱 STARK-X Agri Advisor",
        "chat_status": "🟢 Online | Multilingual Farming Desk",
        "chat_welcome": "Vanakkam! I am your STARK-X advisor. Ask me anything about soil, crops, water, or pests in your language.",
        "chat_placeholder": "Ask your crop question here...",
        "thinking_msg": "STARK-X is analyzing your crop question...",
        "select_language": "Choose Language",
        
        # Crop Vision
        "vision_title": "📸 Crop Vision Studio",
        "vision_desc": "Upload a crop photo to detect diseases and get treatment advice.",
        "vision_upload_label": "Choose a crop photo...",
        "vision_btn": "🔍 Analyze Crop Health",
        "scanning_msg": "STARK-X is scanning the crop...",
        "report_title": "📋 Agronomy Report",
        "analysis_complete": "Analysis Complete!",
        
        # Crop Optimizer
        "opt_title": "🌾 STARK-X Crop Optimizer",
        "opt_subtitle": "Data-driven precision agronomy engine with real-time climate grounding.",
        "opt_tab1": "🎯 Recommend Crop for My Farm",
        "opt_tab2": "🔍 Evaluate Specific Crop Match",
        "soil_label": "Soil Type",
        "water_label": "Water Availability",
        "opt_btn": "🚀 Run STARK-X Algorithm",
        "opt_eval_btn": "🔍 Check Compatibility",
        "gps_banner_title": "📡 Live Satellite GPS & Agrometeorology",
        "auto_inferred_soil": "🌱 Auto-Inferred",
        "farm_params_title": "Farm Soil, Water & Climate Parameters",
        
        # Direct Market & Reels
        "market_title": "🛒 Direct Farmer Marketplace",
        "market_sub": "Bypass middlemen. Sell directly to buyers via WhatsApp.",
        "market_tab1": "🛒 Direct Marketplace",
        "market_tab2": "📱 Agri Reels",
        "post_harvest_title": "Post Your Harvest for Direct Sale",
        "post_btn": "➕ Post Your Harvest",
        "wa_btn": "💬 Buy via WhatsApp",
        "farmer_name_label": "Farmer Name",
        "crop_name_label": "Crop Name",
        "location_label": "Village / Location",
        "phone_label": "WhatsApp Number",
        "qty_label": "Available Quantity (kg)",
        "price_label": "Expected Price per kg (₹)",
        "active_listings_title": "🌾 Active Harvest Listings (Direct from Farmers)"
    },
    "Tamil (தமிழ்)": {
        "lang_name": "Tamil",
        "lang_code": "ta",
        "lang_badge": "🌾 தமிழ்",
        "lang_color": "#16a34a",
        "app_title": "STARK-X | நவீன விவசாய தளம்",
        "app_subtitle": "முழுமையான தன்னியக்க நவீன வேளாண் சுற்றுச்சூழல்",
        "select_tool_msg": "தொடங்குவதற்கு கீழே உள்ள ஒரு கருவியைத் தேர்ந்தெடுக்கவும்:",
        "welcome_farmer": "வணக்கம், **{name}** ({village})! உங்கள் உழவர் சுயவிவரம் இணைக்கப்பட்டுள்ளது.",
        "chat_page": "விவசாய அரட்டை",
        "chat_page_desc": "உங்கள் பண்ணை பற்றி AI-யுடன் உரையாடுங்கள் (வாட்ஸ்அப் பாணி)",
        "vision_page": "பயிர் பார்வை",
        "vision_page_desc": "உடனடி பயிர் மருத்துவ சோதனைக்கு புகைப்படங்களை பதிவேற்றவும்",
        "opt_page": "பயிர் தேர்வு",
        "opt_page_desc": "மண் மற்றும் நீரின் அடிப்படையில் சிறந்த பயிரை கண்டறியவும்",
        "market_sos_page": "சந்தை & அவசர உதவி",
        "market_sos_desc": "நேரலை மண்டி விலைகள் மற்றும் சமூக உதவி",
        "market_page": "நேரடி சந்தை",
        "market_page_desc": "நேரடி அறுவடை விற்பனை & மொபைல் விவசாய ரீல்ஸ்",
        
        # Agri Chat
        "chat_title": "🌱 STARK-X விவசாய ஆலோசகர்",
        "chat_status": "🟢 நேரலையில் | பலமொழி வேளாண் மையம்",
        "chat_welcome": "வணக்கம்! நான் உங்கள் STARK-X விவசாய ஆலோசகர். மண், பயிர், நீர் மற்றும் பூச்சி மேலாண்மை பற்றி உங்கள் மொழியில் கேளுங்கள்.",
        "chat_placeholder": "உங்கள் விவசாய கேள்வியை இங்கே கேட்கவும்...",
        "thinking_msg": "STARK-X உங்கள் பயிர் கேள்வியை ஆய்வு செய்கிறது...",
        "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        
        # Crop Vision
        "vision_title": "📸 பயிர் நோய் கண்டறியும் மையம்",
        "vision_desc": "நோய்களைக் கண்டறிந்து தீர்வு பெற பயிர் இலையின் புகைப்படத்தை பதிவேற்றவும்.",
        "vision_upload_label": "பயிர் புகைப்படத்தை தேர்வு செய்யவும்...",
        "vision_btn": "🔍 பயிரை ஆய்வு செய்",
        "scanning_msg": "STARK-X பயிரை ஸ்கேன் செய்கிறது...",
        "report_title": "📋 பயிர் மருத்துவ அறிக்கை",
        "analysis_complete": "ஆய்வு முடிந்தது!",
        
        # Crop Optimizer
        "opt_title": "🌾 STARK-X பயிர் தேர்வு வழிகாட்டி",
        "opt_subtitle": "நேரலை தட்பவெப்ப நிலை அடிப்படையிலான துல்லிய வேளாண் எஞ்சின்.",
        "opt_tab1": "🎯 எனது பண்ணைக்கு சிறந்த பயிர்",
        "opt_tab2": "🔍 குறிப்பிட்ட பயிர் பொருத்தத்தை சரிபார்",
        "soil_label": "மண் வகை",
        "water_label": "நீர் ஆதாரம்",
        "opt_btn": "🚀 பொருத்தத்தை கணக்கிடு",
        "opt_eval_btn": "🔍 பொருத்தத்தை சரிபார்",
        "gps_banner_title": "📡 நேரலை செயற்கைக்கோள் ஜிபிஎஸ் & வானிலை",
        "auto_inferred_soil": "🌱 தானாக கண்டறியப்பட்ட மண்",
        "farm_params_title": "பண்ணை மண், நீர் மற்றும் காலநிலை அளவீடுகள்",
        
        # Direct Market & Reels
        "market_title": "🛒 நேரடி உழவர் சந்தை",
        "market_sub": "தரகர்கள் இன்றி நேரடியாக வாட்ஸ்அப் மூலம் நுகர்வோருக்கு விற்கவும்.",
        "market_tab1": "🛒 நேரடி சந்தை",
        "market_tab2": "📱 விவசாய ரீல்ஸ்",
        "post_harvest_title": "நேரடி விற்பனைக்கு உங்கள் விளைச்சலை பதிவிடவும்",
        "post_btn": "➕ உங்கள் விளைச்சலை பதிவிடவும்",
        "wa_btn": "💬 வாட்ஸ்அப் மூலம் வாங்க",
        "farmer_name_label": "விவசாயி பெயர்",
        "crop_name_label": "பயிர் பெயர்",
        "location_label": "கிராமம் / இடம்",
        "phone_label": "வாட்ஸ்அப் எண்",
        "qty_label": "கிடைக்கும் அளவு (கிலோ)",
        "price_label": "எதிர்பார்க்கும் விலை / கிலோ (₹)",
        "active_listings_title": "🌾 நேரடி விவசாய விளைச்சல் பட்டியல்கள்"
    },
    "Telugu (తెలుగు)": {
        "lang_name": "Telugu",
        "lang_code": "te",
        "lang_badge": "☀️ తెలుగు",
        "lang_color": "#ea580c",
        "app_title": "STARK-X | ఆధునిక వ్యవసాయ వేదిక",
        "app_subtitle": "అత్యుత్తమ స్వయంప్రతిపత్తి వ్యవసాయ వేదిక",
        "select_tool_msg": "ప్రారంభించడానికి క్రింది ఒక సాధనాన్ని ఎంచుకోండి:",
        "welcome_farmer": "నమస్కారం, **{name}** ({village})! మీ రైతు ప్రొఫైల్ అనుసంధానించబడింది.",
        "chat_page": "రైతు సలహా",
        "chat_page_desc": "మీ వ్యవసాయం గురించి AI తో మాట్లాడండి (వాట్సాప్ శైలి)",
        "vision_page": "పంట పరీక్ష",
        "vision_page_desc": "తక్షణ ఆరోగ్య తనిఖీ కోసం పంట ఫోటోలను అప్‌లోడ్ చేయండి",
        "opt_page": "పంట ఎంపిక",
        "opt_page_desc": "నేల మరియు నీటి ఆధారంగా ఏ పంట వేయాలో తెలుసుకోండి",
        "market_sos_page": "మార్కెట్ & సహాయం",
        "market_sos_desc": "లైవ్ మండి ధరలు మరియు సమాజ అత్యవసర సహాయం",
        "market_page": "రైతు మార్కెట్",
        "market_page_desc": "రైతు ప్రత్యక్ష పంట అమ్మకాలు & వ్యవసాయ రీల్స్",
        
        # Agri Chat
        "chat_title": "🌱 STARK-X రైతు సలహాదారు",
        "chat_status": "🟢 ఆన్లైన్ | బహుభాషా వ్యవసాయ కేంద్రం",
        "chat_welcome": "నమస్కారం! నేను మీ STARK-X వ్యవసాయ సలహాదారుని. నేల, పంట, నీరు లేదా తెగుళ్ల గురించి మీ భాషలోనే అడగండి.",
        "chat_placeholder": "మీ పంట సందేహాన్ని ఇక్కడ టైప్ చేయండి...",
        "thinking_msg": "STARK-X మీ పంట సందేహాన్ని విశ్లేషిస్తోంది...",
        "select_language": "భాషను ఎంచుకోండి",
        
        # Crop Vision
        "vision_title": "📸 పంట వ్యాధి నిర్ధారణ విభాగం",
        "vision_desc": "వ్యాధులను గుర్తించడానికి పంట ఆకు ఫోటోను అప్లోడ్ చేయండి.",
        "vision_upload_label": "పంట ఫోటోను ఎంచుకోండి...",
        "vision_btn": "🔍 పంటను పరీక్షించండి",
        "scanning_msg": "STARK-X పంటను స్కాన్ చేస్తోంది...",
        "report_title": "📋 వ్యవసాయ నివేదిక",
        "analysis_complete": "విశ్లేషణ పూర్తయింది!",
        
        # Crop Optimizer
        "opt_title": "🌾 STARK-X పంట ఆప్టిమైజర్",
        "opt_subtitle": "ప్రత్యక్ష వాతావరణ ఆధారిత ఖచ్చితమైన వ్యవసాయ వ్యవస్థ.",
        "opt_tab1": "🎯 నా పొలానికి సరైన పంట సిఫార్సు",
        "opt_tab2": "🔍 పంట అనుకూలతను పరీక్షించు",
        "soil_label": "నేల రకం",
        "water_label": "నీటి వసతి",
        "opt_btn": "🚀 అనుకూలతను లెక్కించండి",
        "opt_eval_btn": "🔍 అనుకూలతను తనిఖీ చేయండి",
        "gps_banner_title": "📡 ప్రత్యక్ష శాటిలైట్ జీపీఎస్ & వ్యవసాయ వాతావరణం",
        "auto_inferred_soil": "🌱 స్వయంచాలకంగా గుర్తించిన నేల",
        "farm_params_title": "వ్యవసాయ నేల, నీరు & వాతావరణ పారామితులు",
        
        # Direct Market & Reels
        "market_title": "🛒 రైతు ప్రత్యక్ష మార్కెట్",
        "market_sub": "దళారులు లేకుండా నేరుగా వాట్సాప్ ద్వారా విక్రయించండి.",
        "market_tab1": "🛒 రైతు మార్కెట్",
        "market_tab2": "📱 వ్యవసాయ రీల్స్",
        "post_harvest_title": "ప్రత్యక్ష అమ్మకం కోసం మీ పంటను నమోదు చేయండి",
        "post_btn": "➕ మీ పంటను నమోదు చేయండి",
        "wa_btn": "💬 వాట్సాప్ ద్వారా కొనండి",
        "farmer_name_label": "రైతు పేరు",
        "crop_name_label": "పంట పేరు",
        "location_label": "గ్రామం / ప్రాంతం",
        "phone_label": "వాట్సాప్ నంబర్",
        "qty_label": "అందుబాటులో ఉన్న పరిమాణం (కేజీ)",
        "price_label": "ఆశించే ధర కేజీకి (₹)",
        "active_listings_title": "🌾 రైతు ప్రత్యక్ష పంటల జాబితా"
    }
}

def resolve_lang(lang=None):
    """Normalizes any language string to valid key in TRANSLATIONS."""
    if not lang:
        try:
            lang = st.session_state.get("lang") or st.session_state.get("selected_lang", "English")
        except Exception:
            lang = "English"
    lang_str = str(lang).lower().strip()
    if "tamil" in lang_str or "தமிழ்" in lang_str:
        return "Tamil (தமிழ்)"
    elif "telugu" in lang_str or "తెలుగు" in lang_str:
        return "Telugu (తెలుగు)"
    return "English"

def t(key, lang=None):
    """
    Multilingual helper function returning the localized string for a given key.
    Supports both t(key, lang) and t(key).
    Defaults to st.session_state['lang'].
    """
    resolved = resolve_lang(lang)
    lang_dict = TRANSLATIONS.get(resolved, TRANSLATIONS["English"])
    return lang_dict.get(key, TRANSLATIONS["English"].get(key, key))

def get_lang_color(lang=None):
    """Returns the highlight text color associated with the given language."""
    resolved = resolve_lang(lang)
    return LANGUAGE_COLORS.get(resolved, "#2563eb")
