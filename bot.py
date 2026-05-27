import telebot
from telebot import types

TOKEN = "7956424976:AAH-nFiJfygrzkSBPFDUXX_L5HiBdeYemiQ"
MY_CHAT_ID = "761852272"

bot = telebot.TeleBot(TOKEN)
user_data = {}

bot.delete_webhook(drop_pending_updates=True)

INFO_TEXT = (
    "እንኳን ወደ ምዝገባው በደህና መጡ! 🎉\n\n"
    "📚 **የትምህርቱ ዝርዝር መረጃ፦**\n"
    "• **የኮርሱ ቆይታ፦** ለ3 ወራት ብቻ\n"
    "• **የሰዓት ክፍለ-ጊዜ፦** በቀን 2 ሰዓት ይሰጣል\n"
    "• **የእረፍት ቀናት፦** ቅዳሜ እና እሁድ ትምህርት የለም (እረፍት ነው)\n"
    "• ትምህርቱ በአንድ ግሩፕ 5 ሰው በመሆን በኢንተራክቲቭ መልኩ ይሰጣል።\n"
    "• የትምህርቱ መጀመርያ ጊዜ ተማሪዎች ተሟልተው ግሩፑ እንደተዘጋጀ ይጀምራል።\n"
    "• **የኮርሱ ክፍያ፦** **5,000 ብር** ብቻ።\n\n"
    "📖 **የሚሰጡ የኮርስ ዓይነቶች ዝርዝር፦**\n"
    "🔵 1/ ግብረ ዲቁና ቅዳሴ\n"
    "🟢 2/ ግብረ ቅስና ቅዳሴ\n"
    "🟡 3/ ግብረ ዲቁናና ቅስና ቅዳሴ\n"
    "🟠 4/ ተሰጥዎ ቅዳሴ\n"
    "🔴 5/ ሙሉ ሰአታት\n\n"
    "💳 **የባንክ አካውንት መረጃ፦**\n"
    "• የባንክ ስም፦ የኢትዮጵያ ንግድ ባንክ (CBE)\n"
    "• የስም ማረጋገጫ፦ **tsehaye alemu**\n"
    "• የአካውንት ቁጥር፦ `1000730489319`\n\n"
    "⚠️ *ማሳሰቢያ፦ እባክዎ ከላይ ካሉት የኮርስ ዝርዝሮች መማር የሚፈልጉት መኖሩን ያረጋግጡ፤ ከዚያም ክፍያውን ፈጽመው ደረሰኙን በእጅዎ ካደረጉ በኋላ ምዝገባውን ይጀምሩ።*\n\n"
    "ለመመዝገብ ከታች ያለውን **'🚀 ምዝገባ ጀምር'** የሚለውን ቁልፍ ይጫኑ።"
)

COURSES = {
    "1": {"name": "🔵 1/ ግብረ ዲቁና ቅዳሴ", "url": "https://t.me/+BZknMU3b5KU0YWU0"},
    "2": {"name": "🟢 2/ ግብረ ቅስና ቅዳሴ", "url": "https://t.me/+Xe2XsBD3clE5ZTdk"},
    "3": {"name": "🟡 3/ ግብረ ዲቁናና ቅስና ቅዳሴ", "url": "https://t.me/+NRbz0hKGf1liYmE0"},
    "4": {"name": "🟠 4/ ተሰጥዎ ቅዳሴ", "url": "https://t.me/+y2HRjv0OjWI3Zjdk"},
    "5": {"name": "🔴 5/ ሙሉ ሰአታት", "url": "https://t.me/+9-IkbvloovE1Yjg0"}
}

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'START'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("🚀 ምዝገባ ጀምር"))
    bot.send_message(chat_id, INFO_TEXT, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 ምዝገባ ጀምር")
def ask_name(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "በጣም ጥሩ! እባክዎ መጀመሪያ **ሙሉ ስምዎን** ያስገቡ፦", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    chat_id = message.chat.id
    if chat_id not in user_data: user_data[chat_id] = {}
    user_data[chat_id]['name'] = message.text
    bot.send_message(chat_id, "እባክዎ አሁን ደግሞ **ስልክ ቁጥርዎን** ያስገቡ፦", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    chat_id = message.chat.id
    user_data[chat_id]['phone'] = message.text
    bot.send_message(chat_id, "በመጨረሻም፤ የከፈሉበትን **የባንክ ደረሰኝ (የሂሳብ ማስተላለፊያ ፎቶ/Screenshot)** ይላኩልን፦", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_receipt)

def get_receipt(message):
    chat_id = message.chat.id
    if message.content_type != 'photo':
        bot.send_message(chat_id, "⚠️ እባክዎ በትክክል የደረሰኝ ፎቶ/Screenshot ይላኩ።")
        bot.register_next_step_handler(message, get_receipt)
        return

    file_id = message.photo[-1].file_id
    user_data[chat_id]['receipt_file_id'] = file_id
    
    bot.send_message(
        chat_id, 
        "✅ **የደረሰኝ ፎቶዎ ደርሶናል!**\n\n"
        "የክፍያ ደረሰኝዎ በአስተዳዳሪው ተረጋግጦ ሲፈቀድ የሊንክ ምርጫው ይላክሎታል። እባክዎ ለአፍታ በትዕግስት ይጠብቁ።", 
        parse_mode="Markdown"
    )
    
    markup = types.InlineKeyboardMarkup()
    approve_btn = types.InlineKeyboardButton("✅ ፍቀድ (Approve)", callback_data=f"approve_{chat_id}")
    reject_btn = types.InlineKeyboardButton("❌ ከልክል (Reject)", callback_data=f"reject_{chat_id}")
    markup.add(approve_btn, reject_btn)
    
    admin_text = (
        "🚨 **አዲስ የተመዘገበ ተማሪ እና የደረሰኝ ማረጋገጫ!**\n\n"
        f"👤 **ስም፦** {user_data[chat_id]['name']}\n"
        f"📞 **ስልክ፦** {user_data[chat_id]['phone']}\n"
        f"🆔 **Telegram ID፦** `{chat_id}`\n\n"
        "👉 እባክዎ የባንክ ሂሳብዎን ካረጋገጡ በኋላ አንዱን ይምረጡ፦"
    )
    bot.send_photo(MY_CHAT_ID, file_id, caption=admin_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data
    
    if data.startswith("approve_"):
        student_id = int(data.split("_")[1])
        bot.answer_callback_query(call.id, "ክፍያው ጸድቋል!")
        bot.edit_message_caption("✅ ይህ ተማሪ ክፍያው ተረጋግጦ ተፈቅዶለታል።", chat_id=MY_CHAT_ID, message_id=call.message.message_id)
        
        thanks_text = (
            "✅ **ምዝገባዎ በተሳካ ሁኔታ ተረጋግጧል!**\n\n"
            "እባክዎ ከታች ካሉት አማራጮች ሊማሩት የሚፈልጉትን **አንድ የኮርስ ክፍል ብቻ** ይምረጡ።\n"
            "⚠️ *ማሳሰቢያ፦ አንድ ጊዜ ከመረጡ በኋላ ወደ ሌላ መቀየር ወይም ሌላ ግሩፕ መምረጥ አይችሉም!*"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, value in COURSES.items():
            markup.add(types.InlineKeyboardButton(value["name"], callback_data=f"select_{key}_{student_id}"))
            
        bot.send_message(student_id, thanks_text, parse_mode="Markdown", reply_markup=markup)
        
    elif data.startswith("reject_"):
        student_id = int(data.split("_")[1])
        bot.answer_callback_query(call.id, "ክፍያው ውድቅ ተደርጓል!")
        bot.edit_message_caption("❌ ይህ ተማሪ ክፍያው ስላልተገኘ ውድቅ ተደርጓል።", chat_id=MY_CHAT_ID, message_id=call.message.message_id)
        
        bot.send_message(student_id, "❌ **ይቅርታ፣ የላኩት ደረሰኝ ትክክለኛ ሆኖ አልተገኘም።**\nእባክዎ በትክክል መክፈልዎን አረጋግጠው እንደገና በ /start ይጀምሩ።")

    elif data.startswith("select_"):
        parts = data.split("_")
        course_key = parts[1]
        student_id = int(parts[2])
        
        if call.from_user.id != student_id:
            bot.answer_callback_query(call.id, "ይህ ምርጫ የእርስዎ አይደለም!")
            return
            
        selected_course = COURSES[course_key]
        bot.answer_callback_query(call.id, "ምርጫዎ ተመዝግቧል!")
        
        bot.edit_message_text(
            f"🎯 **የመረጡት የኮርስ ክፍል፦** {selected_course['name']}\n\n"
            f"የተመረጠውን ግሩፕ ለመቀላቀል ከታች ያለውን ሰማያዊ ሊንክ ይጫኑ፦\n👇👇👇\n"
            f"{selected_course['url']}\n\n"
            f"**እንኳን በደህና መጡ! ትምህርቱ የሚጀመርበትን የጊዜ ሰሌዳ በግሩፑ ውስጥ እናሳውቃለን።**",
            chat_id=student_id,
            message_id=call.message.message_id
        )
        
        try:
            student_name = user_data[student_id].get('name', 'ያልታወቀ')
        except:
            student_name = "የቀድሞ ተማሪ"
            
        bot.send_message(MY_CHAT_ID, f"📢 **የተማሪ ምርጫ ማሳወቂያ፦**\n👤 ተማሪ፦ {student_name}\n🆔 ID፦ `{student_id}`\n🗂 የመረጠው ክፍል፦ {selected_course['name']}")

print("Run...")
bot.infinity_polling()
