import telebot
from telebot import types
import csv
import os
import random

TOKEN = "7956424976:AAH-nFiJfygrzkSBPFDUXX_L5HiBdeYemiQ"
MY_CHAT_ID = "7618522772"

ADMIN_USERNAME = "@Azaryas_debre_abay"
ADMIN_PHONE = "+251979043780"
CSV_FILE = "students_database.csv"

bot = telebot.TeleBot(TOKEN)
user_data = {}

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["የምዝገባ ቁጥር", "የቴሌግራም ID", "ሙሉ ስም", "ስልክ ቁጥር", "የመረጠው ክፍል"])

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
    "⚠️ *ማሳሰቢያ፦ እባክዎ ከላይ ካሉት የኮርስ ዝርዝሮች መማር የሚፈልጉት መኖሩን ያረጋግጡ፤ ከዚያም ክፍያውን ፈጽመው ደረሰኙን በእጅዎ ካደረጉ በኋላ ምዝገባውን ይጀምሩ።*\n"
    "👉 **ክፍያ ሲፈጽሙ በባንክ ማስተላለፊያ ማስታወሻ (Reason/Remark) ላይ ሙሉ ስምዎን መጻፍዎን አይርሱ!**\n\n"
    "ለመመዝገብ ከታች ያለውን **'🚀 ምዝገባ ጀምር'** የሚለውን ቁልፍ ይጫኑ።"
)

TERMS_TEXT = (
    "📜 **የውል እና ደንብ ስምምነት (Terms & Conditions)**\n\n"
    "ምዝገባውን ከመጀመርዎ በፊት እባክዎ የሚከተሉትን ህጋዊ ደንቦች በጥንቃቄ ያንብቡ፦\n\n"
    "1️⃣ ትምህርቱ ሙሉ በሙሉ **በኦንላይን (Online)** የሚሰጥ ነው።\n"
    "2️⃣ የትምህርቱ ክፍያ ከተፈጸመ በኋላ **በምንም መልኩ ተመላሽ አይደረግም**።\n"
    "3️⃣ ምዝገባው ተጠናቆ አንዴ የኮርስ ክፍል ከተመረጠ በኋላ **ክፍል መቀየር በፍጹም አይቻልም**።\n\n"
    "ከላይ በተጠቀሱት ውሎች ከተስማሙ ከታች ያለውን **'🤝 ተስማምቻለሁ'** የሚለውን ቁልፍ በመጫን ምዝገባውን ይቀጥሉ።"
)

COURSES = {
    "1": {"name": "🔵 1/ ግብረ ዲቁና ቅዳሴ", "url": "https://t.me/+BZknMU3b5KU0YWU0"},
    "2": {"name": "🟢 2/ ግብረ ቅስና ቅዳሴ", "url": "https://t.me/+Xe2XsBD3clE5ZTdk"},
    "3": {"name": "🟡 3/ ግብረ ዲቁናና ቅስና ቅዳሴ", "url": "https://t.me/+y2HRjv0OjWI3Zjdk"},
    "4": {"name": "🟠 4/ ተሰጥዎ ቅዳሴ", "url": "https://t.me/+NRbz0hKGf1liYmE0"},
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
def show_terms(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("🤝 ተስማምቻለሁ"))
    bot.send_message(chat_id, TERMS_TEXT, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🤝 ተስማምቻለሁ")
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
        f"✅ **የደረሰኝ ፎቶዎ ደርሶናል!**\n\n"
        f"የክፍያ ደረሰኝዎ በአስተዳዳሪው ተረጋግጦ ሲፈቀድ የሊንክ ምርጫው ይላክሎታል። እባክዎ ለአፍታ በትዕግስት ይጠብቁ。\n\n"
        f"📞 መዘግየት ካለ ለአስተዳዳሪው መልእክት መላክ ይችላሉ፦\n"
        f"ቴሌግራም፦ {ADMIN_USERNAME}\n"
        f"ስልክ፦ {ADMIN_PHONE}", 
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
        
        reg_number = f"REG-{random.randint(1000, 9999)}"
        user_data[student_id]['reg_number'] = reg_number
        
        bot.answer_callback_query(call.id, "ክፍያው ጸድቋል!")
        bot.edit_message_caption(f"✅ ይህ ተማሪ ክፍያው ተረጋግጦ ተፈቅዶለታል።\n🆔 የምዝገባ ቁጥር፦ `{reg_number}`", chat_id=MY_CHAT_ID, message_id=call.message.message_id)
        
        thanks_text = (
            "🧾 **ዲጂታል የክፍያ ደረሰኝ ማረጋገጫ**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **የምዝገባ ማረጋገጫ ቁጥር፦** `{reg_number}`\n"
            f"👤 **የተማሪ ስም፦** {user_data[student_id]['name']}\n"
            f"📞 **ስልክ ቁጥር፦** {user_data[student_id]['phone']}\n"
            "状态 **የክፍያ ሁኔታ፦** በስኬት ጸድቋል (Paid) ✅\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🎉 **ምዝገባዎ በተሳካ ሁኔታ ተጠናቋል!**\n"
            "እባክዎ ከታች ካሉት አማራጮች ሊማሩት የሚፈልጉትን **አንድ የኮርስ ክፍል ብቻ** ይምረጡ。\n"
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
        
        bot.send_message(
            student_id, 
            f"❌ **ይቅርታ፣ የላኩት ደረሰኝ ወይም ክፍያ በትክክል ሆኖ አልተገኘም።**\n\n"
            f"እባክዎ በትክክል መክፈልዎን አረጋግጠው እንደገና በ /start ይጀምሩ። ጥያቄ ካለዎት በአስተዳዳሪው አድራሻ ይጠይቁ፦\n"
            f"ቴሌግራም፦ {ADMIN_USERNAME}\n"
            f"ስልክ፦ {ADMIN_PHONE}"
        )

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
            student_phone = user_data[student_id].get('phone', 'ያልታወቀ')
            reg_num = user_data[student_id].get('reg_number', 'ያልታወቀ')
        except:
            student_name = "የቀድሞ ተማሪ"
            student_phone = "ያልታወቀ"
            reg_num = "ያልታወቀ"
            
        try:
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([reg_num, student_id, student_name, student_phone, selected_course['name']])
        except Exception as e:
            print(e)
            
        bot.send_message(
            MY_CHAT_ID, 
            f"📢 **የተማሪ ምርጫ ማሳወቂያ እና ምዝገባ ሥርዓት፦**\n"
            f"📝 መረጃው በ Excel (CSV) ላይ ሰፍሯል!\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **የምዝገባ ቁጥር፦** `{reg_num}`\n"
            f"👤 **ተማሪ፦** {student_name}\n"
            f"📞 **ስልክ፦** {student_phone}\n"
            f"🗂 **የመረጠው ክፍል፦** {selected_course['name']}"
        )

print("Run...")
bot.infinity_polling()
