import telebot
from telebot import types
from pymongo import MongoClient
import uuid
from datetime import datetime, timezone
from dateutil import parser
import math


bot = telebot.TeleBot("7118718415:AAEuafQPWFS7geKADfdNxOU3fUolJoN1G84", parse_mode=None)
uri = 'mongodb+srv://ihyea:2nrYJLeLmhxpiNOH@cluster0.cltw0.mongodb.net/calc?retryWrites=true&w=majority'
client = MongoClient(uri)

db = client['calc']
collection = db['users']


uri2 = 'mongodb+srv://ihyea:2nrYJLeLmhxpiNOH@cluster0.cltw0.mongodb.net/important?retryWrites=true&w=majority'
client2 = MongoClient(uri2)

db2 = client2['important']
day_message_collection = db2['day_message']

def now():
    return datetime.now()


CHANNEL_USERNAME = '-1002289574179'

# دالة للتحقق من اشتراك المستخدم
def check_user_subscription(user_id):
    try:
        # استخدام get_chat_member للتحقق من حالة المستخدم في القناة
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        # التحقق مما إذا كان المستخدم عضوًا أو مسؤولًا أو مشرفًا
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        # في حال حدوث خطأ (على سبيل المثال إذا كانت القناة خاصة)
        print(f"Error checking subscription: {str(e)}")
        return False



@bot.message_handler(commands=['id'])
def userid(message):
    userid = message.from_user.id
    bot.reply_to(message, f'أيدي حسابك هو: <code>{userid}</code>', parse_mode='HTML')


def get_day_message():
    day_message = day_message_collection.find_one({"day": 1})
    if day_message:
            message = day_message.get("message", "لا توجد رسالة")
            description = day_message.get("description", "لا توجد وصف")
            tafsir = day_message.get("explain", "لا يوجد تفسير")
            return message, description, tafsir
    else:
            return "لا توجد رسالة", "لا يوجد وصف" , "لا يوجد تفسير"


def check_and_notify_user(user_id):
    today = datetime.now(timezone.utc).date()  # استخدم الوقت بالتوقيت العالمي المنسق

    user = collection.find_one({"user_id": user_id})

    if user:
        last_usage = user.get("last_usage")
        if last_usage:
            last_usage_date = last_usage.date()
            if last_usage_date < today:

                return True
        else:
            return True
    else:
        return True 
    
    return False




def send_day_message(user_id):
    if check_and_notify_user(user_id):
        day_message = day_message_collection.find_one({"day": 1})
        if day_message:
            msg = day_message.get("message", "لا توجد رسالة")
            tafsir = day_message.get("explain", "لا يوجد تفسير")
            
            # إرسال رسالة اليوم للمستخدم
            bot.send_message(user_id, f'''
­
رسالة اليوم 

{msg}

{tafsir}
­
''')
        else:
            bot.send_message(user_id, "لا توجد رسالة، وصف، أو تفسير لليوم.")




userdash = types.InlineKeyboardMarkup(row_width=2)
writecalc = types.InlineKeyboardButton('كتابية', callback_data='writecalc')
simplecalc = types.InlineKeyboardButton('تفاعلية', callback_data="simplecalc")
infostu = types.InlineKeyboardButton('عائمة', switch_inline_query_current_chat="")
userdash.add(writecalc,simplecalc,infostu)






def evaluate_expression(expression):
    try:
        # دعم الدوال الرياضية
        expression = expression.replace("sin", "math.sin")  # الجيب
        expression = expression.replace("cos", "math.cos")  # جيب التمام
        expression = expression.replace("tan", "math.tan")  # الظل
        expression = expression.replace("log", "math.log")  # اللوغاريتم الطبيعي
        expression = expression.replace("log10", "math.log10")  # لوغاريتم الأساس 10
        expression = expression.replace("sqrt", "math.sqrt")  # الجذر التربيعي
        expression = expression.replace("e", "math.e")  # العدد النيبيري
        expression = expression.replace("pi", "math.pi")  # العدد π
        expression = expression.replace("pow", "math.pow")  # رفع العدد للأس
        expression = expression.replace("exp", "math.exp")  # e^x
        expression = expression.replace("factorial", "math.factorial")  # العاملية (factorial)
        expression = expression.replace("abs", "math.fabs")  # القيمة المطلقة
        expression = expression.replace("degrees", "math.degrees")  # التحويل إلى درجات
        expression = expression.replace("radians", "math.radians")  # التحويل إلى راديان
        expression = expression.replace("sinh", "math.sinh")  # دالة الجيب الزائدي
        expression = expression.replace("cosh", "math.cosh")  
        expression = expression.replace("tanh", "math.tanh")  
        expression = expression.replace("asin", "math.asin")  
        expression = expression.replace("acos", "math.acos")  
        expression = expression.replace("atan", "math.atan")  
        expression = expression.replace("atan2", "math.atan2")  
        expression = expression.replace("hypot", "math.hypot")  
        expression = expression.replace("ceil", "math.ceil")  
        expression = expression.replace("floor", "math.floor")  
        expression = expression.replace("trunc", "math.trunc") 
        expression = expression.replace("gcd", "math.gcd") 
        expression = expression.replace("lcm", "math.lcm")  
        expression = expression.replace("comb", "math.comb")  
        expression = expression.replace("perm", "math.perm")  
        expression = expression.replace("isqrt", "math.isqrt")  
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        # تقييم العملية الحسابية
        result = eval(expression, {"math": math})
        return result
    except:
        return f"حدث خطأ ما تأكد من إرسال العملية الحسابية بشكل صحيح"







# دالة لمعالجة الاستعلامات المضمنة
@bot.inline_handler(func=lambda query: True)
def handle_inline_query(query):
    search_query = query.query
    result = evaluate_expression(search_query)
    message, description, tafsir = get_day_message()
    results = [
        types.InlineQueryResultArticle(
            id=str(uuid.uuid4()),  # استخدم UUID لتوليد معرف فريد
            title= f"الناتج = {result}", 
            
            input_message_content=types.InputTextMessageContent(
                message_text=f'''
الناتج = {result}

@atharbots
'''
        )
            ),
        types.InlineQueryResultArticle(
            id=str(uuid.uuid4()),  # استخدم UUID لتوليد معرف فريد
            title= message,
            description= description,
            input_message_content=types.InputTextMessageContent(
                message_text=f'''
­
رسالة اليوم

{message}

{tafsir}
­
'''
            )
        )
    ]
    bot.answer_inline_query(query.id, results, cache_time=1)
    return






simplecalc = types.InlineKeyboardMarkup(row_width=4)
sims1 = types.InlineKeyboardButton('%', callback_data='sim_%')
sims2 = types.InlineKeyboardButton('(', callback_data='sim_(')
sims3 = types.InlineKeyboardButton(')', callback_data='sim_)')
simclr = types.InlineKeyboardButton('C', callback_data='clrsim')
sims4 = types.InlineKeyboardButton('÷', callback_data='sim_/')
sims5 = types.InlineKeyboardButton('×', callback_data='sim_*')
sims6 = types.InlineKeyboardButton('+', callback_data='sim_+')
sims7 = types.InlineKeyboardButton('-', callback_data='sim_-')
sims8 = types.InlineKeyboardButton('log', callback_data='sim_log(')
sims9 = types.InlineKeyboardButton('sin', callback_data='sim_sin(')
sims10 = types.InlineKeyboardButton('cos', callback_data='sim_cos(')
sims11 = types.InlineKeyboardButton('tan', callback_data='sim_tan(')
sims12 = types.InlineKeyboardButton('e', callback_data='sim_e')
sims13 = types.InlineKeyboardButton('➥', callback_data='home')
sims14 = types.InlineKeyboardButton('Xⁿ', callback_data='sim_^')
sims15 = types.InlineKeyboardButton('√', callback_data='sim_sqrt(')

sims_ = types.InlineKeyboardButton('.', callback_data='sim_.')
sim7 = types.InlineKeyboardButton('7', callback_data='sim_7')
sim8 = types.InlineKeyboardButton('8', callback_data='sim_8')
sim9 = types.InlineKeyboardButton('9', callback_data='sim_9')
sim4 = types.InlineKeyboardButton('4', callback_data='sim_4')
sim5 = types.InlineKeyboardButton('5', callback_data='sim_5')
sim6 = types.InlineKeyboardButton('6', callback_data='sim_6')
sim1 = types.InlineKeyboardButton('1', callback_data='sim_1')
sim2 = types.InlineKeyboardButton('2', callback_data='sim_2')
sim3 = types.InlineKeyboardButton('3', callback_data='sim_3')
sim0 = types.InlineKeyboardButton('0', callback_data='sim_0')
simres = types.InlineKeyboardButton('=', callback_data='ressim')


simplecalc.add(sims2,sims3,sims8,simclr,sims9,sims10,sims11,sims13,sims1,sims14,sims15,sims12,sim7,sim8,sim9,sims4,sim4,sim5,sim6,sims5,sim1,sim2,sim3,sims7,sim0,sims_,simres,sims6)









home = types.InlineKeyboardMarkup()
backbtn = types.InlineKeyboardButton('رجوع', callback_data='home')
home.add(backbtn)


pro = types.InlineKeyboardMarkup(row_width=1)
probtn = types.InlineKeyboardButton('الإشتراك بالخطة المدفوعة', callback_data='pro')
backbtn = types.InlineKeyboardButton('رجوع', callback_data='home')
pro.add(probtn,backbtn)


from datetime import datetime

def now():
    return datetime.now()

def add_user(user_id, referred_by=None):
    # تحقق مما إذا كان المستخدم مسجل بالفعل
    if not collection.find_one({"user_id": user_id}):
        user_data = {
            "user_id": user_id,
            "oper": "",
            "daily_using": 0,
            "points": 0,
            "last_usage": now(),
            "referred_by": referred_by
        }

        collection.insert_one(user_data)
        return True  # تم إضافة المستخدم الجديد
    return False  # المستخدم مسجل مسبقًا


def generate_referral_link(user_id):
    base_link = "https://t.me/atharcalcbot?start="
    referral_link = base_link + str(user_id)
    return referral_link


def update_points(user_id):
    # قم بتحديث نقاط المستخدم في قاعدة البيانات
    user = collection.find_one({"user_id": user_id})
    if user:
        new_points = user["points"] + 1
        collection.update_one({"user_id": user_id}, {"$set": {"points": new_points}})
        return True  # تم تحديث النقاط بنجاح
    return False  # لم يتم العثور على المستخدم


@bot.message_handler(commands=['start'])
def start(message):
    referral_code = message.text.split()[1] if len(message.text.split()) > 1 else None
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if referral_code:
        if add_user(user_id, referred_by=int(referral_code)):
            if not check_user_subscription(user_id):
                # إذا لم يكن مشتركًا، إرسال رسالة تطلب منه الاشتراك
                checksub = types.InlineKeyboardMarkup()
                subscribe_button = types.InlineKeyboardButton('اضغط للاشتراك', url="https://t.me/+ih9i67Vw0lJhYmU0")
                checksub.add(subscribe_button)

                bot.send_message(user_id, "لا يمكنك استخدام البوت إلا بعد الاشتراك في هذه القناة.", reply_markup=checksub)
            else:
                bot.send_message(user_id, text=f'''
                ­                
حياك الله {first_name}

اختر ما تريد من القائمة التالية:
­
                ''', reply_markup=userdash)
            
            # يمكنك هنا إضافة نقاط أو مكافأة للمحيل
            if update_points(int(referral_code)):
                bot.send_message(int(referral_code), "لقد حصلت على نقطة إضافية بسبب إحالتك!")
        else:
            bot.send_message(user_id, text=f'''
            ­                
حياك الله {first_name}

اختر ما تريد من القائمة التالية:
            ­
            ''', reply_markup=userdash)
    else:
        if not check_user_subscription(user_id):
            # إذا لم يكن مشتركًا، إرسال رسالة تطلب منه الاشتراك
            checksub = types.InlineKeyboardMarkup()
            subscribe_button = types.InlineKeyboardButton('اضغط للاشتراك', url="https://t.me/+ih9i67Vw0lJhYmU0")
            checksub.add(subscribe_button)

            bot.send_message(user_id, "لا يمكنك استخدام البوت إلا بعد الاشتراك في هذه القناة.", reply_markup=checksub)
        else:
            if add_user(user_id):
                bot.send_message(user_id, text=f'''
                ­                
حياك الله {first_name}

اختر ما تريد من القائمة التالية:
                ­
                ''', reply_markup=userdash)
            else:
                bot.send_message(user_id, text=f'''
                ­                
حياك الله {first_name}

اختر ما تريد من القائمة التالية:
                ­
                ''', reply_markup=userdash)

                     
@bot.message_handler(commands=['dashboard'])
def dashboard(message):
    chat_id = message.from_user.id
    user = collection.find_one({"user_id": chat_id})
    if user:
        points = user["points"]
        daily_using = user["daily_using"]
        iso_date = f"{user['last_usage']}"
        parsed_date = parser.parse(iso_date)
        last_usage = parsed_date.strftime("%H:%M %Y-%m-%d")

        
    bot.send_message(message.from_user.id, text= f'''
    ­                
معلومات حسابك:

عدد إحالاتك: {points}
استخداماتك اليوم: {daily_using}
آخر استخدام لك: {last_usage}

رابط الإحالة الخاص بك:
{generate_referral_link(message.from_user.id)}
    ­
    ''', reply_markup=pro)
                     
                     
                     


        
        
 
 
 
 
@bot.callback_query_handler(func=lambda call: call.data.startswith("sim_"))
def handle_sh_selection(call):
    bot.answer_callback_query(callback_query_id=call.id)
    num = call.data.split("_")[1]

    try:
        # الحصول على قيمة oper القديمة
        user = collection.find_one({"user_id": call.message.chat.id})
        if user and "oper" in user:
            old_value = user["oper"]
        else:
            old_value = ""

        # إلحاق القيمة الجديدة بالنص القديم
        new_value = old_value + num if old_value else num

        # تحديث الحقل oper
        result = collection.update_one(
            {"user_id": call.message.chat.id},
            {"$set": {"oper": new_value}}
        )
        user = collection.find_one({"user_id": call.message.chat.id})
        bot.edit_message_text(chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              text=
f'''
البوتات الأثرية

{user['oper']}


­
''' , reply_markup=simplecalc)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"حدث خطأ: {str(e)}")







@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    first_name = call.from_user.first_name
    user_id = call.message.chat.id
    if not check_user_subscription(user_id):
            # إذا لم يكن مشتركًا، إرسال رسالة تطلب منه الاشتراك
            checksub = types.InlineKeyboardMarkup()
            subscribe_button = types.InlineKeyboardButton('اضغط للاشتراك', url="https://t.me/+ih9i67Vw0lJhYmU0")
            checksub.add(subscribe_button)

            bot.send_message(user_id, "لا يمكنك استخدام البوت إلا بعد الاشتراك في هذه القناة.", reply_markup=checksub)
    else:
        if call.data == 'home' :
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f'''
        ­                
حياك الله {first_name}

اختر ما تريد من القائمة التالية:
        ­
        ''', reply_markup=userdash)
            
        if call.data == 'writecalc':
            user = collection.find_one({"user_id": call.message.chat.id})
            value = ""
            # تحديث الحقل oper
            result = collection.update_one(
                {"user_id": call.message.chat.id},
                {"$set": {"oper": value}}
            )
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=
    '''
    ­
    أرسل لي العملية الحسابية حتى آتيك بالنتيجة
    ­
    ''' , reply_markup=home)
            
        if call.data == 'simplecalc':
            user = collection.find_one({"user_id": call.message.chat.id})
            value = ""
            # تحديث الحقل oper
            result = collection.update_one(
                {"user_id": call.message.chat.id},
                {"$set": {"oper": value}}
            )
            user = collection.find_one({"user_id": call.message.chat.id})
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=
    f'''
    البوتات الأثرية

    {user['oper']}

    ­
    ''' , reply_markup=simplecalc)
            
        if call.data == 'clrsim':
            user = collection.find_one({"user_id": call.message.chat.id})
            value = ""
            # تحديث الحقل oper
            result = collection.update_one(
                {"user_id": call.message.chat.id},
                {"$set": {"oper": value}}
            )
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=
    f'''
    البوتات الأثرية



    ­
    ''' , reply_markup=simplecalc)

        if call.data == 'ressim':
                user = collection.find_one({"user_id": call.message.chat.id})
                oper = user['oper']
                result = evaluate_expression(oper)
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                    message_id=call.message.message_id, 
                                    text=
        f'''
        البوتات الأثرية

        {user['oper']}

    الناتج: {result}

    ­
        ''' , reply_markup=simplecalc)
                daily_using = user["daily_using"] + 1
                collection.update_one({"user_id": call.message.chat.id}, {"$set": {"daily_using": daily_using}})
                send_day_message(call.message.chat.id)
                collection.update_one(
            {"user_id": call.message.chat.id},
            {"$set": {"last_usage": datetime.now(timezone.utc)}},
            upsert=True
        )
        
        if call.data == 'pro':
            proo = types.InlineKeyboardMarkup(row_width=1)
            refbtn = types.InlineKeyboardButton('مشاركة رابط دعوتك', url = f'https://t.me/share/url?url=t.me/atharcalcbot?start={call.from_user.id}')
            proobtn = types.InlineKeyboardButton('الإشتراك بجميع خدماتنا', url='https://t.me/+ytMQvdd7DlAwNmM0')
            backbtn = types.InlineKeyboardButton('رجوع', callback_data='homepro')
            proo.add(refbtn,proobtn,backbtn)
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=
    f'''
    ­
    يمكنك الاشتراك بالخطة المدفوعة بإحدي طريقين:

    الإشتراك مجانا مدي الحياة: بدعوة 10 أشخاص للبوت عن طريق رابط دعوتك

    الاشتراك مقابل 50 نجمة شهريا: يمكنك بهذا الاشتراك الاستمتاع بجميع خدماتنا بلا حدود يومية وليس هذا البوت فقط
    ­
    ''' , reply_markup=proo)
            
        if call.data == 'homepro': 
            chat_id = call.from_user.id
            user = collection.find_one({"user_id": chat_id})
            if user:
                points = user["points"]
                daily_using = user["daily_using"]
                iso_date = f"{user['last_usage']}"
                parsed_date = parser.parse(iso_date)
                last_usage = parsed_date.strftime("%H:%M %Y-%m-%d")
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, text= f'''
                ­                
    معلومات حسابك:

    عدد إحالاتك: {points}
    استخداماتك اليوم: {daily_using}
    آخر استخدام لك: {last_usage}

    رابط الإحالة الخاص بك:
    {generate_referral_link(call.from_user.id)}
        ­
        ''', reply_markup=pro)

            
     
     
@bot.message_handler(func=lambda message: not message.via_bot and message.text)
def handle_message(message):
    user_id = message.from_user.id
    if not check_user_subscription(user_id):
         # إذا لم يكن مشتركًا، إرسال رسالة تطلب منه الاشتراك
        checksub = types.InlineKeyboardMarkup()
        subscribe_button = types.InlineKeyboardButton('اضغط للاشترك', url= "https://t.me/+ih9i67Vw0lJhYmU0")
        checksub.add(subscribe_button)
        
        bot.send_message(user_id, "لا يمكنك استخدام البوت إلا بعد الاشتراك في هذه القناة.", reply_markup=checksub)
    else:
        expression = message.text
        result = evaluate_expression(expression)
        bot.reply_to(message, f"الناتج = {result}")
        send_day_message(user_id)
        # تحديث آخر استخدام للبوت
        collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_usage": datetime.now(timezone.utc)}},
            upsert=True
        )
        user = collection.find_one({"user_id": user_id})
        daily_using = user["daily_using"] + 1
        collection.update_one({"user_id": user_id}, {"$set": {"daily_using": daily_using}})
                    
     
     
     
bot.polling()