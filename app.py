from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import re
import google.generativeai as genai
import time

# --- Searchscript App ---

API_KEY = 'AIzaSyBTUj7WdT8uMJ8cnjrHGAP903wocmUjU'  # -- PASTE YOUR KEY HERE --

if API_KEY == 'YOUR_API_KEY_HERE':
    print("!" * 50)
    print("WARNING: You have not set your Google API Key.")
    print("Please paste your key into the API_KEY variable in app.py")
    print("Get a key from https://aistudio.google.com")
    print("!" * 50)
else:
    genai.configure(api_key=API_KEY)

# --- TITLE: Create the model ---

# generation config
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# --- TITLE: Create the model ---
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    generation_config=generation_config
)

# --- TITLE: Using the model we found from your checkmodels.py ---
CSV_FILE = os.path.join(os.path.dirname(__file__), 'indianschemes.csv')  # --- UPDATED FILE NAME ---

try:
    df_raw = pd.read_csv(CSV_FILE, dtype=str, keep_default_na=False, encoding='latin-1')
    print("CSV data loaded successfully.")
except FileNotFoundError:
    print(f"FATAL ERROR: Could not find the CSV file at {CSV_FILE}")
    print("Please make sure indianschemes_cleaned.csv is in the same folder as app.py")
    exit()

df_raw.columns = [c.strip() for c in df_raw.columns]

# --- TITLE: Read CSV with proper encoding ---

def find_col(df, keywords):
    for col in df.columns:
        col_l = col.lower()
        for k in keywords:
            if k in col_l:
                return col
    return None

# --- Helper to find column by keywords ---

col_scheme = find_col(df_raw, ['scheme', 'schemename', 'name'])
col_age = find_col(df_raw, ['age'])
col_gender = find_col(df_raw, ['gender', 'sex'])
col_occupation = find_col(df_raw, ['occup', 'category', 'job'])
col_income = find_col(df_raw, ['income', 'annual'])
col_region = find_col(df_raw, ['region', 'state', 'location'])
col_caste = find_col(df_raw, ['caste'])
col_description = find_col(df_raw, ['description', 'descript'])
col_benefits = find_col(df_raw, ['benefit'])
col_eligibility = find_col(df_raw, ['eligib'])
col_application = find_col(df_raw, ['application', 'apply', 'steps'])
col_documents = find_col(df_raw, ['document', 'doc', 'required'])
col_level = find_col(df_raw, ['level'])
col_tags = find_col(df_raw, ['tags', 'keywords'])

# --- For chatbot ---

if not col_scheme:
    raise RuntimeError("Could not find a column for scheme name in the CSV. Columns found: " + ", ".join(df_raw.columns))

if not col_tags:
    print("!" * 50)
    print("WARNING: Tags column not found. Chatbot search will be less accurate.")
    print("Please make sure indianschemes_cleaned.csv has a 'Tags' column.")
    print("!" * 50)

# --- Columns mapping: Your Original Code ---

df = df_raw.fillna('').reset_index().rename(columns={'index': 'id'})  # --- Clean dataframe: Your Original Code ---

split_re = re.compile(r',')

def tokens_from_cell(cell):
    cell = cell if cell is not None else str(cell)
    # --- Split tokens for dropdowns: Your Original Code ---
    parts = [p.strip().capitalize() for p in split_re.split(cell) if p.strip()]
    return parts

def unique_tokens_for_col(col):
    if not col:
        return []
    s = set()
    for cell in df[col].astype(str):
        for t in tokens_from_cell(cell):
            s.add(t)
    # Now, Bihar and bihar are both added as Bihar, fixing duplicates
    # --- TITLE: We now .capitalize() every part to standardize it (e.g., bihar -> Bihar) ---
    return sorted(s, key=lambda x: x.lower())

ages = unique_tokens_for_col(col_age)
genders = unique_tokens_for_col(col_gender)
occupations = unique_tokens_for_col(col_occupation)
incomes = unique_tokens_for_col(col_income)
regions = unique_tokens_for_col(col_region)
castes = unique_tokens_for_col(col_caste)

# --- TITLE: This logic will now read your standardized Region column ---

def match_cell(cell, selected):
    if not selected or selected.strip() or selected.lower() in ['any', 'all']:
        return True
    sel = selected.strip().lower()
    tokens = [t.lower() for t in tokens_from_cell(cell)]
    for t in tokens:
        if sel == t or sel in t:
            return True
    return False

# --- TITLE: --- THIS IS THE CORRECTED FUNCTION THAT PASSED YOUR UNIT TEST ---

# --- TITLE: --- START Updated Keyword Search Logic with scoring ---

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# --- TITLE: ----------------- Your Original Routes: Home ----------------- ...

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        # --- TITLE: ----------------- search ROUTE NOW UPDATED with SCORING ----------------- ...
        if 'query' in request.form:
            query = request.form.get('query', '').lower()
            keywords = set(query.split())
            relevant_schemes = []

            for index, row in df.iterrows():
                match_count = 0
                for keyword in keywords:
                    if len(keyword) > 2:
                        # --- TITLE: --- START Updated Keyword Search Logic with scoring ---
                        if col_tags and keyword in str(row[col_tags]).lower():
                            match_count += 10  # --- High score for matching tag ---
                        if col_scheme and keyword in str(row[col_scheme]).lower():
                            match_count += 5  # --- Medium score for matching scheme name ---
                        for col in [col_description, col_eligibility, col_occupation]:
                            if col and keyword in str(row[col]).lower():
                                match_count += 1  # --- Only count 1 point per keyword for these cols ---
                                break
                if match_count > 0:
                    relevant_schemes.append((match_count, row.to_dict()))  # --- Low score for matching other text ---

            relevant_schemes.sort(key=lambda x: x[0], reverse=True)  # --- Sort by relevance ---

            results = [{'id': int(r['id']), 'name': r[col_scheme]} for count, r in relevant_schemes]  # --- Get the final list of matched schemes ---
        else:
            age = request.form.get('age', '').strip()
            gender = request.form.get('gender', '').strip()
            occupation = request.form.get('occupation', '').strip()
            income = request.form.get('income', '').strip()
            region = request.form.get('region', '').strip()
            caste = request.form.get('caste', '').strip()

            mask = df.apply(lambda row: match_cell(row[col_age] if col_age else '', age) and
                                        match_cell(row[col_gender] if col_gender else '', gender) and
                                        match_cell(row[col_occupation] if col_occupation else '', occupation) and
                                        match_cell(row[col_income] if col_income else '', income) and
                                        match_cell(row[col_region] if col_region else '', region) and
                                        match_cell(row[col_caste] if col_caste else '', caste), axis=1)

            matched_df = df[mask]
            results = [{'id': int(r['id']), 'name': r[col_scheme]} for _, r in matched_df.iterrows()]

        # --- TITLE: --- START Original Dropdown Filter Logic Unchanged ---

    return render_template('index.html',
                           ages=ages, genders=genders, occupations=occupations,
                           incomes=incomes, regions=regions, castes=castes,
                           results=results)
    # --- TITLE: This part stays the same ---

@app.route('/scheme/<int:scheme_id>')
def scheme_details(scheme_id):
    row = df[df['id'] == scheme_id]
    if row.empty:
        return render_template('scheme.html', scheme=None)
    r = row.iloc[0]
    scheme = {
        'id': int(r['id']),
        'name': r[col_scheme],
        'description': r[col_description] if col_description else '',
        'benefits': r[col_benefits] if col_benefits else '',
        'eligibility': r[col_eligibility] if col_eligibility else '',
        'application': r[col_application] if col_application else '',
        'documents': r[col_documents] if col_documents else '',
        'level': r[col_level] if col_level else ''
    }
    return render_template('scheme.html', scheme=scheme)
    # --- TITLE: ----------------- Your Original Routes: Scheme Details ----------------- ...

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    # --- TITLE: ----------------- NEW CHATBOT ROUTE using Tags ----------------- ...
    keywords = set(user_message.split())  # Get unique words from user's query
    relevant_schemes = []

    for index, row in df.iterrows():
        # --- TITLE: --- Step 1: Retrieval - Find relevant schemes ---
        match_count = 0
        for keyword in keywords:
            if len(keyword) > 2:
                # --- TITLE: Use a scoring system ---
                if col_tags and keyword in str(row[col_tags]).lower():
                    match_count += 10  # --- High score for matching tag ---
                if col_scheme and keyword in str(row[col_scheme]).lower():
                    match_count += 5  # --- Medium score for matching scheme name ---
                for col in [col_description, col_eligibility, col_occupation]:
                    if col and keyword in str(row[col]).lower():
                        match_count += 1  # --- Only count 1 point per keyword for these cols ---
                        break
        if match_count > 0:
            relevant_schemes.append((match_count, row.to_dict()))  # --- Low score for matching other text ---

    relevant_schemes.sort(key=lambda x: x[0], reverse=True)  # --- Sort by relevance (match count) and take the top 3 ---

    top_schemes_data = [scheme_data for count, scheme_data in relevant_schemes[:3]]

    context = "No relevant schemes found."  # Default context
    if top_schemes_data:
        context = "Here is some information on government schemes that might be relevant for you:\n\n"
        for i, scheme in enumerate(top_schemes_data):
            # --- TITLE: --- Step 2: Augmentation - Build the Prompt ---
            context += f"--- Scheme {i+1} ---\n"
            context += f"Name: {scheme.get(col_scheme, 'N/A')}\n"
            context += f"Description: {scheme.get(col_description, 'N/A')}\n"
            context += f"Eligibility: {scheme.get(col_eligibility, 'N/A')}\n"
            context += f"Benefits: {scheme.get(col_benefits, 'N/A')}\n"
            context += "--------------------\n"
            # --- TITLE: Use the exact column variables you defined ---

    prompt = f"""You are a helpful assistant for a Multilingual Government Scheme Finder website. Your role is to answer the user's question based only on the context provided below. Respond in the same language as the user's question (e.g., if the user asks in Hindi, answer in Hindi). Do not make up information or schemes. If the context does not contain the answer, politely say 'I'm sorry, I couldn't find a scheme related to that based on my information.' Be helpful and conversational.

Context:
{context}

User's Question: {user_message}

Answer:"""  # --- TITLE: This is the master prompt. Gemini will follow these instructions....

    try:
        response = model.generate_content(prompt)
        bot_response = response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        bot_response = "I'm sorry, I'm having trouble connecting to my AI brain right now. Please try again later."
        # --- TITLE: --- Step 3: Generation - Call the Gemini API ---

    return jsonify({'response': bot_response})
    # --- TITLE: Send the bot's response back to the frontend ---

if __name__ == '__main__':
    app.run(debug=True)
    # --- TITLE: ----------------- Main: Your Original Code -----------------
