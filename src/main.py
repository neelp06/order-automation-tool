from ingest import load_orders
from database import save_to_db
from job_cards import generate_job_card
from report import generate_report

print("🚀 Starting Order Automation Tool...")
print("=" * 40)

# Step 1 - Load and validate orders
print("\n📂 Step 1: Loading orders...")
df = load_orders('../data/orders.csv')
print(f"✅ {len(df)} orders loaded.")

# Step 2 - Save to database
print("\n💾 Step 2: Saving to database...")
save_to_db(df)

# Step 3 - Generate job cards for valid orders only
print("\n🖨️  Step 3: Generating job cards...")
valid_orders = df[~df['is_duplicate'] & ~df['missing_data']]
for _, order in valid_orders.iterrows():
    generate_job_card(order)
print(f"✅ {len(valid_orders)} job cards created.")

# Step 4 - Generate Excel report
print("\n📊 Step 4: Generating report...")
generate_report(df)

print("\n" + "=" * 40)
print("✅ All done! Check your job_cards/ and output/ folders.")