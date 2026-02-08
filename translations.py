# Multi-language translations for the bot

TRANSLATIONS = {
    'en': {
        # Commands
        'start': """👋 Welcome to USDT Exchange Bot!

Exchange USDT (TRC20) to Cambodian Riel (KHR) instantly.

Supported languages: 🇬🇧 🇰🇭 🇨🇳

Use /language to change language.""",
        'help': """📚 Help Center

1. Send USDT to: `{wallet}`
2. Get transaction hash (TxID) or screenshot
3. Fill in your bank details
4. Wait for admin approval
5. Receive KHR in your bank account

Commands:
/start - Start the bot
/language - Change language
/rate - Check current exchange rate
/status - Check your order status
/help - Show this help message""",
        'rate': """💱 Current Exchange Rate

1 USD = {rate} KHR
Fee: {fee}%""",
        'language_select': "🌐 Select your language:",
        
        # Order process
        'enter_amount': "💵 Enter the amount of USDT you sent:",
        'enter_txid': "🔗 Enter the Transaction ID (TxID):",
        'upload_screenshot': "📎 Upload a screenshot of your transaction (or skip with /skip):",
        'enter_bank': "🏦 Enter your bank name:",
        'enter_account_number': "🔢 Enter your account number:",
        'enter_account_name': "👤 Enter your account holder name:",
        
        # Order confirmation
        'order_confirm': """✅ Order Summary

USDT Amount: {amount} USDT
Exchange Rate: {rate} KHR
Fee ({fee}%): {fee_amount} USDT
Received Amount: {received} KHR

Bank: {bank}
Account: {account}
Account Name: {name}

Reply /confirm to submit or /cancel to cancel.""",
        'order_submitted': "✅ Your order has been submitted! Order ID: #{order_id}\n\nWaiting for admin approval.",
        
        # Status
        'status_pending': "⏳ Your order #{order_id} is pending. Please wait for admin approval.",
        'status_approved': "✅ Your order #{order_id} has been approved! KHR will be transferred soon.",
        'status_rejected': "❌ Your order #{order_id} has been rejected. Contact admin for details.",
        
        # Admin
        'admin_new_order': """🆕 New Order #{order_id}

User: @{username} (ID: {user_id})
Amount: {amount} USDT
Received: {received} KHR
Bank: {bank}
Account: {account}

{tx_info}""",
        'admin_approve': "✅ Approve",
        'admin_reject': "❌ Reject",
        'order_approved_user': "✅ Your order #{order_id} has been approved! Payment will be processed shortly.",
        'order_rejected_user': "❌ Your order #{order_id} has been rejected. Reason: {reason}",
        
        # Errors
        'invalid_amount': "❌ Invalid amount. Please enter a valid number.",
        'invalid_txid': "❌ Invalid TxID format. Please check and try again.",
        'skip_screenshot': "⏭️ Screenshot skipped.",
        'order_not_found': "❌ Order not found.",
        'not_admin': "❌ You are not authorized to use this command.",
        
        # Keyboard
        'cancel': "Cancel",
        'skip': "Skip",
        'confirm': "Confirm",
        'back': "Back"
    },
    
    'km': {
        # Commands
        'start': """👋 សូមស្វាគមន៍មកកាន់ USDT Exchange Bot!

ប្តូរ USDT (TRC20) ទៅជារីលាក់កម្ពុជា (KHR) ភ្លាមៗ។

ភាសាដែលគាំទ្រ: 🇬🇧 🇰🇭 🇨🇳

ប្រើ /language ដើម្បីផ្លាស់ភាសា។""",
        'help': """📚 មជ្ឈមណ្ឌលជំនួយ

1. ផ្ញើ USDT ទៅ: `{wallet}`
2. ទទួល Transaction hash (TxID) ឬ រូបភាព
3.បំពេញព័ត៌មានធនាគាររបស់អ្នក
4. រង់ចាំការអនុញ្ញាតពីអ្នកគ្រប់គ្រង
5. ទទួល KHR ក្នុងគណនីធនាគាររបស់អ្នក

ពាក្យបញ្ជា:
/start - ចាប់ផ្តើម bot
/language - ផ្លាស់ភាសា
/rate - ពិនិត្យអត្រាប្តូរប្រាក់
/status - ពិនិត្យស្ថានភាពការបញ្ជា
/help - បង្ហាញជំនួយ""",
        'rate': """💱 អត្រាប្តូរប្រាក់បច្ចុប្បន្ន

1 USD = {rate} KHR
ថ្លៃសេវា: {fee}%""",
        'language_select': "🌐 ជ្រើសភាសា:",
        
        # Order process
        'enter_amount': "💵 បញ្ចូលចំនួន USDT ដែលអ្នកផ្ញើ:",
        'enter_txid': "🔗 បញ្ចូល Transaction ID (TxID):",
        'upload_screenshot': "📎 ផ្ទុកឡើងរូបភាពប្រតិបត្តិការ (ឬ រំល�់ជាមួយ /skip):",
        'enter_bank': "🏦 បញ្ចូលឈ្មោះធនាគារ:",
        'enter_account_number': "🔢 បញ្ចូលលេខគណនី:",
        'enter_account_name': "👤 បញ្ចូលឈ្មោះម្ចាស់គណនី:",
        
        # Order confirmation
        'order_confirm': """✅ សេចក្តីសង្ខេបការបញ្ជា

ចំនួន USDT: {amount} USDT
អត្រាប្តូរ: {rate} KHR
ថ្លៃសេវា ({fee}%): {fee_amount} USDT
ទទួលបាន: {received} KHR

ធនាគារ: {bank}
គណនី: {account}
ឈ្មោះ: {name}

ឆ្លើយតប /confirm ដើម្បីដាក់ពាក្យ ឬ /cancel ដើម្បីលុប។""",
        'order_submitted': "✅ ពាក្យរបស់អ្នកបានដាក់ពាក្យ! លេខការណ៍: #{order_id}\n\nកំពុងរង់ចាំការអនុញ្ញាត។",
        
        # Status
        'status_pending': "⏳ ពាក្យ #{order_id} កំពុងរង់ចាំ។ សូមរង់ចាំការអនុញ្ញាត។",
        'status_approved': "✅ ពាក្យ #{order_id} បានអនុញ្ញាត! KHR នឹងត្រូវផ្ញើក្នុងពេលឆាប់ៗ។",
        'status_rejected': "❌ ពាក្យ #{order_id} បានបដិសេដ។ ទាក់ទងអ្នកគ្រប់គ្រង។",
        
        # Admin
        'admin_new_order': """🆕 ការបញ្ជាថ្មី #{order_id}

អ្នកប្រើ: @{username} (ID: {user_id})
ចំនួន: {amount} USDT
ទទួលបាន: {received} KHR
ធនាគារ: {bank}
គណនី: {account}

{tx_info}""",
        'admin_approve': "✅ អនុញ្ញាត",
        'admin_reject': "❌ បដិសេដ",
        'order_approved_user': "✅ ពាក្យ #{order_id} របស់អ្នកបានអនុញ្ញាត! ការទូទាត់នឹងត្រូវផ្ញើក្នុងពេលឆាប់ៗ។",
        'order_rejected_user': "❌ ពាក្យ #{order_id} របស់អ្នកបានបដិសេដ។ ហេតុផល: {reason}",
        
        # Errors
        'invalid_amount': "❌ ចំនួនមិនត្រឹមត្រូវ។ សូមបញ្ចូលលេខត្រឹមត្រូវ។",
        'invalid_txid': "❌ ទម្រង់ TxID មិនត្រឹមត្រូវ។ សូមពិនិត្យម្តងទៀត។",
        'skip_screenshot': "⏭️ រូបភាពត្រូវបានរំលេះ។",
        'order_not_found': "❌ រកមិនឃើញពាក្យនេះទេ។",
        'not_admin': "❌ អ្នកមិនមានសិទ្ធិប្រើពាក្យបញ្ជានេះទេ។",
        
        # Keyboard
        'cancel': "លុប",
        'skip': "រំលេះ",
        'confirm': "បញ្ជាក់",
        'back': "ត្រលប់"
    },
    
    'zh': {
        # Commands
        'start': """👋 欢迎使用 USDT 兑换机器人！

即时将 USDT (TRC20) 兑换为柬埔寨瑞尔 (KHR)。

支持语言: 🇬🇧 🇰🇭 🇨🇳

使用 /language 更改语言。""",
        'help': """📚 帮助中心

1. 发送 USDT 到: `{wallet}`
2. 获取交易哈希 (TxID) 或截图
3. 填写您的银行信息
4. 等待管理员批准
5. 在您的银行账户收到 KHR

命令:
/start - 启动机器人
/language - 更改语言
/rate - 查看当前汇率
/status - 查看订单状态
/help - 显示此帮助信息""",
        'rate': """💱 当前汇率

1 美元 = {rate} KHR
手续费: {fee}%""",
        'language_select': "🌐 选择您的语言:",
        
        # Order process
        'enter_amount': "💵 输入您发送的 USDT 金额:",
        'enter_txid': "🔗 输入交易 ID (TxID):",
        'upload_screenshot': "📎 上传交易截图 (或使用 /skip 跳过):",
        'enter_bank': "🏦 输入银行名称:",
        'enter_account_number': "🔢 输入账户号码:",
        'enter_account_name': "👤 输入账户持有人姓名:",
        
        # Order confirmation
        'order_confirm': """✅ 订单摘要

USDT 金额: {amount} USDT
汇率: {rate} KHR
手续费 ({fee}%): {fee_amount} USDT
收到金额: {received} KHR

银行: {bank}
账户: {account}
账户姓名: {name}

回复 /confirm 提交 或 /cancel 取消。""",
        'order_submitted': "✅ 您的订单已提交！订单号: #{order_id}\n\n等待管理员批准。",
        
        # Status
        'status_pending': "⏳ 您的订单 #{order_id} 正在等待中。请等待管理员批准。",
        'status_approved': "✅ 您的订单 #{order_id} 已批准！KHR 即将汇出。",
        'status_rejected': "❌ 您的订单 #{order_id} 已被拒绝。请联系管理员。",
        
        # Admin
        'admin_new_order': """🆕 新订单 #{order_id}

用户: @{username} (ID: {user_id})
金额: {amount} USDT
收到: {received} KHR
银行: {bank}
账户: {account}

{tx_info}""",
        'admin_approve': "✅ 批准",
        'admin_reject': "❌ 拒绝",
        'order_approved_user': "✅ 您的订单 #{order_id} 已批准！付款即将处理。",
        'order_rejected_user': "❌ 您的订单 #{order_id} 已被拒绝。原因: {reason}",
        
        # Errors
        'invalid_amount': "❌ 无效金额。请输入有效数字。",
        'invalid_txid': "❌ TxID 格式无效。请检查后重试。",
        'skip_screenshot': "⏭️ 截图已跳过。",
        'order_not_found': "❌ 未找到订单。",
        'not_admin': "❌ 您无权使用此命令。",
        
        # Keyboard
        'cancel': "取消",
        'skip': "跳过",
        'confirm': "确认",
        'back': "返回"
    }
}

def get_text(key, lang='en', **kwargs):
    """Get translated text"""
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text
