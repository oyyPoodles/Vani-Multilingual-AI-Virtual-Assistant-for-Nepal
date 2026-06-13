"""
VANI — Intent Dataset Generator
Creates 9 JSON files x 1000 examples each = 9,000 utterances
Output: datasets/intents/
"""
import os, json, random

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'intents')
os.makedirs(OUT, exist_ok=True)

# Templates per intent - we'll generate variations
INTENTS = {
    "sales_query": {
        "ne": [
            "आजको बिक्री कति भयो?", "आज कति बिक्यो?", "आजको कुल बिक्री?",
            "हिजोको बिक्री कति थियो?", "यो महिनाको बिक्री?", "बिक्री रिपोर्ट देखाऊ",
            "आजको revenue कति भयो?", "कति कमायौं आज?", "बिक्री कस्तो छ?",
            "यो हप्ताको बिक्री कति?", "गत महिनाको बिक्री?", "बिक्री बढ्यो कि घट्यो?",
            "कुन product सबैभन्दा बढी बिक्यो?", "बिक्रीको trend कस्तो छ?",
            "आजको sales figure?", "दैनिक बिक्री कति?", "मासिक बिक्री summary",
            "बिक्री data चाहिन्छ", "कति revenue आयो?", "आजको income कति?"
        ],
        "en": [
            "What are today's sales?", "How much did we sell today?", "Today's revenue?",
            "Show me sales report", "Daily sales figure", "Total sales today?",
            "What's the revenue for today?", "Sales summary please", "How much revenue?",
            "Show today's sales data", "Sales for this week?", "Monthly sales report",
            "What were yesterday's sales?", "Sales performance today?", "Revenue update",
            "How are sales going?", "Total sales amount?", "Sales breakdown today",
            "Give me the sales numbers", "What's our daily revenue?"
        ],
        "mixed": [
            "Sales कति भयो आज?", "आज sales report देखाऊ", "Today को बिक्री?",
            "Revenue कति आयो?", "Sales data चाहिन्छ", "आजको sales figure?",
            "Daily sales कति?", "बिक्री report generate गर", "Total revenue आज?",
            "Sales summary देखाऊ", "Monthly sales कति?", "Weekly sales report चाहिन्छ",
            "आज कति sales भयो?", "Revenue report देखाऊ", "Sales trend कस्तो छ?"
        ]
    },
    "inventory_query": {
        "ne": [
            "स्टकमा कति बाँकी छ?", "गोदाममा के के छ?", "कुन सामान सकियो?",
            "इन्भेन्टरी चेक गर", "स्टक अपडेट?", "कति सामान बाँकी छ?",
            "गोदामको अवस्था?", "कुन product स्टकमा छैन?", "स्टक रिपोर्ट?",
            "सामानको हिसाब?", "बाँकी स्टक कति?", "कति item बाँकी?",
            "गोदाम भरिएको छ?", "स्टक कम भएको product?", "इन्भेन्टरी स्टेटस?",
            "सामान कति छ?", "product कति बाँकी?", "स्टक level?",
            "गोदामको रिपोर्ट?", "कुन सामान order गर्नुपर्छ?"
        ],
        "en": [
            "Check inventory", "What's in stock?", "Stock status?",
            "How many items left?", "Inventory report", "Which products are out of stock?",
            "Stock level update", "Show warehouse status", "What needs reordering?",
            "Current stock count", "Inventory check please", "How much stock do we have?",
            "List low stock items", "Product availability?", "Warehouse inventory report",
            "Stock remaining?", "What's the inventory status?", "Items in warehouse?",
            "Show me the stock levels", "Any items out of stock?"
        ],
        "mixed": [
            "Inventory मा कति laptop बाँकी छ?", "Stock check गर",
            "कति item stock मा छ?", "Inventory status देखाऊ", "Stock level कति?",
            "Product कति बाँकी stock मा?", "Warehouse को status?", "Stock report चाहिन्छ",
            "Low stock items देखाऊ", "Inventory update गर", "कुन product out of stock छ?",
            "Stock count कति?", "Reorder गर्नुपर्ने items?", "Inventory check गर",
            "Stock मा कति छ?"
        ]
    },
    "invoice_creation": {
        "ne": [
            "बिल बनाऊ", "इन्भ्वाइस तयार गर", "बिल पठाऊ",
            "ग्राहकलाई बिल दिनुस्", "बिल छाप्नुस्", "नयाँ बिल बनाऊ",
            "बिल generate गर", "इन्भ्वाइस पठाउनुस्", "बिल तयार गर",
            "ग्राहकको बिल बनाऊ", "VAT बिल चाहिन्छ", "बिल प्रिन्ट गर",
            "बिलको status?", "बिल भुक्तानी?", "बिल रद्द गर",
            "pending बिल कति छ?", "बिल अपडेट गर", "बिलको विवरण?",
            "अन्तिम बिल देखाऊ", "बिल सूची?"
        ],
        "en": [
            "Generate invoice", "Create a bill", "Send invoice to customer",
            "Print invoice", "New invoice please", "Make an invoice",
            "Invoice for customer A", "Create billing", "Generate bill",
            "Send the invoice", "Invoice status?", "Pending invoices?",
            "Cancel invoice", "Update invoice", "Invoice details?",
            "List all invoices", "Last invoice?", "Create VAT invoice",
            "Invoice payment status?", "How many pending invoices?"
        ],
        "mixed": [
            "Invoice बनाऊ", "राम ट्रेडर्सलाई invoice पठाऊ", "Bill generate गर",
            "Customer को invoice?", "Invoice print गर", "New bill बनाऊ",
            "VAT invoice चाहिन्छ", "Pending invoice कति?", "Invoice status देखाऊ",
            "Bill cancel गर", "Invoice update गर", "Invoice details देखाऊ",
            "Last invoice देखाऊ", "Invoice list चाहिन्छ", "Bill payment status?"
        ]
    },
    "customer_lookup": {
        "ne": [
            "ग्राहकको विवरण?", "ग्राहक खोज", "ग्राहकको जानकारी दिनुस्",
            "ग्राहक सूची देखाऊ", "ग्राहकको फोन नम्बर?", "ग्राहकको ठेगाना?",
            "ग्राहकको बाँकी रकम?", "ग्राहक कति छन्?", "नयाँ ग्राहक थप",
            "ग्राहकको इतिहास?", "ग्राहक डाटा?", "ग्राहक प्रोफाइल?",
            "ग्राहकको credit?", "ग्राहक update गर", "ग्राहकको नाम?",
            "ग्राहकको order history?", "ग्राहक लिस्ट?", "ग्राहकको email?",
            "ग्राहक search गर", "ग्राहकको payment history?"
        ],
        "en": [
            "Find customer info", "Customer details please", "Look up customer",
            "Customer phone number?", "Customer address?", "Customer list",
            "Search customer", "Customer credit balance?", "Add new customer",
            "Customer history?", "Customer data?", "Customer profile?",
            "Update customer info", "Customer name?", "Customer order history?",
            "Show all customers", "Customer email?", "Customer payment history?",
            "How many customers?", "Customer database?"
        ],
        "mixed": [
            "Customer details देखाऊ", "Ram को details दिनुस्", "Customer search गर",
            "ग्राहकको info?", "Customer list देखाऊ", "Customer को phone number?",
            "Customer credit कति?", "New customer add गर", "Customer profile देखाऊ",
            "Customer data चाहिन्छ", "Customer history देखाऊ", "Customer update गर",
            "Customer ko address?", "Customer payment history?", "Customer database खोल"
        ]
    },
    "employee_query": {
        "ne": [
            "कर्मचारीको विवरण?", "कर्मचारी सूची?", "स्टाफ जानकारी?",
            "कर्मचारी कति छन्?", "कर्मचारीको तलब?", "कर्मचारी खोज",
            "नयाँ कर्मचारी थप", "कर्मचारीको विभाग?", "कर्मचारी अपडेट",
            "कर्मचारीको पद?", "कर्मचारी प्रोफाइल?", "कर्मचारीको फोन?",
            "कर्मचारी हटाऊ", "कर्मचारीको email?", "कर्मचारी रिपोर्ट?",
            "कति जना स्टाफ छन्?", "कर्मचारीको नियुक्ति मिति?",
            "कर्मचारीको performance?", "HR रिपोर्ट?", "स्टाफ डाटा?"
        ],
        "en": [
            "Employee list please", "Staff information?", "How many employees?",
            "Employee details?", "Employee salary?", "Search employee",
            "Add new employee", "Employee department?", "Update employee",
            "Employee position?", "Employee profile?", "Employee phone?",
            "Remove employee", "Employee email?", "Employee report?",
            "Total staff count?", "Employee hire date?", "Employee performance?",
            "HR report?", "Staff data?", "Show all employees",
            "Employee database?", "Who works in sales?", "List managers"
        ],
        "mixed": [
            "Employee list देखाऊ", "Staff information चाहिन्छ", "Employee details देखाऊ",
            "कर्मचारी salary कति?", "Employee search गर", "New employee add गर",
            "Employee department कुन?", "Employee update गर", "Staff count कति?",
            "Employee profile देखाऊ", "HR report चाहिन्छ", "Employee data देखाऊ",
            "कर्मचारी phone number?", "Employee performance report?", "Staff list देखाऊ"
        ]
    },
    "attendance_query": {
        "ne": [
            "आज को-को आयो?", "उपस्थिति कस्तो छ?", "हाजिरी रिपोर्ट?",
            "आज कति जना आए?", "कोसँग अनुपस्थित?", "हाजिरी चेक गर",
            "आजको उपस्थिति?", "गैरहाजिर को हो?", "हाजिरी अपडेट गर",
            "मासिक हाजिरी?", "कर्मचारी उपस्थिति?", "हाजिरी विवरण?",
            "आजको attendance?", "कति जना गैरहाजिर?", "हाजिरी record?",
            "बिदामा को छ?", "late आउने कर्मचारी?", "हाजिरी summary?",
            "साप्ताहिक हाजिरी?", "उपस्थिति percentage?"
        ],
        "en": [
            "Employee attendance?", "Who came today?", "Attendance report?",
            "How many present today?", "Who is absent?", "Check attendance",
            "Today's attendance?", "Absent employees?", "Update attendance",
            "Monthly attendance?", "Employee presence?", "Attendance details?",
            "Attendance record?", "How many absent?", "Who is on leave?",
            "Late arrivals?", "Attendance summary?", "Weekly attendance?",
            "Attendance percentage?", "Show attendance sheet"
        ],
        "mixed": [
            "Attendance check गर", "आज को-को present छ?", "Attendance report देखाऊ",
            "कति जना absent?", "Today को attendance?", "Attendance update गर",
            "Monthly attendance चाहिन्छ", "Absent employees को?", "Leave मा को छ?",
            "Attendance summary देखाऊ", "कर्मचारी attendance कस्तो?",
            "Late आउने को-को?", "Attendance record देखाऊ", "Weekly attendance?",
            "Attendance percentage कति?"
        ]
    },
    "report_generation": {
        "ne": [
            "रिपोर्ट बनाऊ", "मासिक रिपोर्ट चाहिन्छ", "बार्षिक रिपोर्ट?",
            "बिक्री रिपोर्ट बनाऊ", "वित्तीय रिपोर्ट?", "रिपोर्ट generate गर",
            "दैनिक रिपोर्ट?", "साप्ताहिक रिपोर्ट?", "रिपोर्ट डाउनलोड गर",
            "profit/loss रिपोर्ट?", "कर्मचारी रिपोर्ट बनाऊ", "ग्राहक रिपोर्ट?",
            "इन्भेन्टरी रिपोर्ट?", "tax रिपोर्ट?", "analytics रिपोर्ट?",
            "रिपोर्ट प्रिन्ट गर", "रिपोर्ट summary?", "business रिपोर्ट?",
            "performance रिपोर्ट?", "रिपोर्ट export गर"
        ],
        "en": [
            "Generate report", "Monthly report please", "Annual report?",
            "Sales report", "Financial report?", "Create report",
            "Daily report?", "Weekly report?", "Download report",
            "Profit loss report?", "Employee report", "Customer report?",
            "Inventory report?", "Tax report?", "Analytics report?",
            "Print report", "Report summary?", "Business report?",
            "Performance report?", "Export report", "Generate this month's report",
            "Show me the reports", "Quarterly report?", "Year-end report?"
        ],
        "mixed": [
            "Sales report generate गर", "Monthly report चाहिन्छ", "Report बनाऊ",
            "Financial report देखाऊ", "Daily report generate गर", "Report download गर",
            "Profit loss report?", "Employee report बनाऊ", "Inventory report चाहिन्छ",
            "Tax report generate गर", "Analytics report देखाऊ", "Report print गर",
            "Business report चाहिन्छ", "Performance report?", "Report export गर"
        ]
    },
    "reminder": {
        "ne": [
            "सम्झना दिनुस्", "भोलिको बैठक सम्झाऊ", "रिमाइन्डर सेट गर",
            "बैठक छ भनी सम्झाऊ", "भुक्तानी सम्झना", "काम सम्झाऊ",
            "deadline सम्झाऊ", "appointment सम्झना", "follow up गर",
            "सम्झना राख", "alarm सेट गर", "notification पठाऊ",
            "schedule गर", "बैठक तालिका?", "आजको कार्यसूची?",
            "भोलि के गर्नु छ?", "pending काम?", "due date सम्झाऊ",
            "task list?", "to-do list?"
        ],
        "en": [
            "Set reminder", "Remind me about meeting", "Set alarm",
            "Remind payment due", "Schedule meeting", "Follow up reminder",
            "Task reminder", "Deadline reminder", "Appointment reminder",
            "Set notification", "Tomorrow's schedule?", "Today's agenda?",
            "What's pending?", "Due dates?", "Task list?",
            "To-do list?", "Remind me tomorrow", "Set a reminder for 3pm",
            "Meeting schedule?", "Calendar check?"
        ],
        "mixed": [
            "Meeting remind गर", "Reminder set गर", "भोलि remind गर",
            "Payment due सम्झाऊ", "Schedule देखाऊ", "Follow up गर",
            "Task reminder set गर", "Deadline सम्झाऊ", "Appointment remind गर",
            "Notification पठाऊ", "Tomorrow schedule?", "Today agenda?",
            "Pending task?", "Due date सम्झाऊ", "Calendar check गर"
        ]
    },
    "general_conversation": {
        "ne": [
            "तिमी कस्तो छौ?", "नमस्ते", "धन्यवाद", "VANI, के गर्न सक्छौ?",
            "तिमी को हौ?", "मलाई सहयोग गर", "तिमीले के के गर्छौ?",
            "help चाहिन्छ", "कसरी काम गर्छ?", "तिमी AI हौ?",
            "good morning", "शुभ दिन", "bye", "फेरि भेटौंला",
            "thank you", "sorry", "माफ गर्नुस्", "कृपया",
            "हो", "होइन"
        ],
        "en": [
            "Hello", "Hi VANI", "How are you?", "What can you do?",
            "Who are you?", "Help me", "What are your features?",
            "I need help", "How does this work?", "Are you an AI?",
            "Good morning", "Good evening", "Goodbye", "See you later",
            "Thank you", "Sorry", "Please", "Yes", "No",
            "Tell me about yourself", "VANI, how are you?", "Hey there"
        ],
        "mixed": [
            "VANI, तिमी कस्तो?", "Help चाहिन्छ", "तिमी AI हो?",
            "Good morning, कस्तो छ?", "Thank you, धन्यवाद", "Bye, फेरि भेटौंला",
            "VANI, what can you do?", "Features के के छन्?", "How does यो work?",
            "Please help गर", "Sorry, माफ गर्नुस्", "Yes, हो",
            "No, होइन", "Tell me about yourself", "VANI के हो?"
        ]
    }
}

# Time/date modifiers for variation
TIME_NE = ["आज", "हिजो", "यो हप्ता", "गत हप्ता", "यो महिना", "गत महिना", "आजको", "हिजोको"]
TIME_EN = ["today", "yesterday", "this week", "last week", "this month", "last month", "today's", "yesterday's"]
PRODUCTS = ["laptop", "mobile", "rice", "pen", "cement", "shirt", "medicine", "keyboard", "oil", "notebook"]
CUSTOMERS_N = ["राम", "श्याम", "हरि", "सीता", "गीता", "कृष्ण", "बिनोद", "सरिता", "गोपाल", "सुनिल"]
CUSTOMERS_E = ["Ram", "Shyam", "Hari", "Sita", "Gopal", "Krishna", "Binod", "Sarita", "Sunil", "Anita"]
AMOUNTS = ["1000", "5000", "10000", "50000", "25000", "500", "15000", "2000", "75000", "100000"]

def make_variations(templates, intent, target=1000):
    """Generate variations from templates to reach target count."""
    results = []
    all_templates = []
    for lang_templates in templates.values():
        all_templates.extend(lang_templates)
    
    # Add originals
    for t in all_templates:
        results.append({"text": t, "intent": intent})
    
    # Generate variations until we reach target
    while len(results) < target:
        base = random.choice(all_templates)
        variation = base
        
        # Randomly modify
        r = random.random()
        if r < 0.15:
            variation = variation + "?"
        elif r < 0.3:
            variation = variation.rstrip("?").rstrip("।")
        elif r < 0.45:
            time_word = random.choice(TIME_NE + TIME_EN)
            variation = f"{time_word} {variation}"
        elif r < 0.55:
            product = random.choice(PRODUCTS)
            variation = variation.replace("laptop", product).replace("सामान", product)
        elif r < 0.65:
            customer = random.choice(CUSTOMERS_N + CUSTOMERS_E)
            variation = f"{customer} को {variation}" if random.random() > 0.5 else f"{variation} for {customer}"
        elif r < 0.75:
            variation = variation.lower()
        elif r < 0.85:
            variation = variation.upper()
        elif r < 0.9:
            amount = random.choice(AMOUNTS)
            variation = f"{variation} NPR {amount}"
        else:
            # Add please/कृपया
            prefix = random.choice(["please ", "कृपया ", ""])
            variation = f"{prefix}{variation}"
        
        # Avoid exact duplicates
        if not any(r["text"] == variation for r in results):
            results.append({"text": variation, "intent": intent})
    
    return results[:target]

if __name__ == "__main__":
    print("=" * 50)
    print("VANI - Intent Dataset Generator")
    print("=" * 50)
    
    total = 0
    for intent_name, templates in INTENTS.items():
        data = make_variations(templates, intent_name, target=1000)
        random.shuffle(data)
        
        filepath = os.path.join(OUT, f"{intent_name}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  OK {intent_name}.json -> {len(data)} examples")
        total += len(data)
    
    print(f"\nTotal: {total} utterances across {len(INTENTS)} intents")
    print(f"Output: {os.path.abspath(OUT)}")
