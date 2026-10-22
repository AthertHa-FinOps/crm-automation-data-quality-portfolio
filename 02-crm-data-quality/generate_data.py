"""Generates FICTIONAL source-lead and CRM-export datasets with deliberate errors.
Seeded, so results are reproducible:  python generate_data.py"""
import csv, random
random.seed(42)
FIRST = "Olivia Liam Emma Noah Ava Lucas Mia Ethan Sofia Mason Isla Logan Chloe Jacob Zoe Aiden Nora Owen Lily Wyatt Priya Arjun Mei Wei Carlos Maria Diego Elena Omar Fatima Kenji Yuki Anika Rohan".split()
LAST = "Tremblay Singh Chen Martin Roy Wilson Patel Nguyen Garcia Lopez Brown Ali Kim Cohen Silva Rossi Novak Khan Murphy Campbell Reyes Santos Ito Park Mehta Fraser".split()
CITIES = ["Markham","Stouffville","Toronto","Richmond Hill","Vaughan","Pickering","Whitby","Oshawa","Newmarket","Mississauga"]
SOURCES = ["Website Form","Property Inquiry","Online Ad","Referral","Open House"]
def phone(): return f"416-555-{random.randint(0,9999):04d}"
def date(): return f"2026-{random.randint(1,9):02d}-{random.randint(1,28):02d}"

source, seen = [], set()
while len(source) < 700:
    f, l = random.choice(FIRST), random.choice(LAST)
    email = f"{f}.{l}{random.randint(1,999)}@example.com".lower()
    if email in seen: continue
    seen.add(email)
    source.append(dict(lead_id=f"L{len(source)+1:04d}", first_name=f, last_name=l, email=email,
        phone=phone(), lead_source=random.choice(SOURCES), city=random.choice(CITIES), province="ON", created_date=date()))

crm = [dict(r) for r in source]
random.shuffle(crm)
for r in random.sample(crm, 40): crm.remove(r)          # 1) never synced to CRM
rows = list(crm)
def pick(n): return random.sample(rows, n)
for r in pick(60): r["email"] = random.choice([r["email"].upper(), " "+r["email"], r["email"].title()+" "])  # 2) case/whitespace
for r in pick(70):                                                                                       # 3) phone formats
    d = r["phone"].replace("-","")
    r["phone"] = random.choice([f"({d[:3]}) {d[3:6]}-{d[6:]}", d, f"+1 {d[:3]} {d[3:6]} {d[6:]}", f"{d[:3]}.{d[3:6]}.{d[6:]}"])
for r in pick(45): r["province"] = random.choice(["Ontario","Ont.","on","ONT"])                          # 4) province drift
for r in pick(30): r["lead_source"] = ""                                                                 # 5) blank source
for r in pick(12): r["email"] = random.choice([r["email"].replace("@",""), r["email"].replace(".com",""), r["email"].replace("@","@@")])  # 6) invalid email
mm = pick(25)                                                                                            # 7) conflicts vs source
for r in mm[:13]: r["phone"] = phone()
for r in mm[13:]: r["last_name"] = r["last_name"][:-1] + random.choice("aeiouy")
dups = []                                                                                                # 8) duplicates
for r in pick(40):
    d = dict(r); d["email"] = d["email"].strip().upper(); d["created_date"] = date(); dups.append(d)
rows += dups
for i in range(18):                                                                                      # 9) CRM-only, no email
    f, l = random.choice(FIRST), random.choice(LAST)
    rows.append(dict(lead_id="", first_name=f, last_name=l, email="", phone=phone(), lead_source=random.choice(SOURCES),
                     city=random.choice(CITIES), province="ON", created_date=date()))
for i in range(15):                                                                                      # 10) CRM-only, has email
    f, l = random.choice(FIRST), random.choice(LAST)
    rows.append(dict(lead_id="", first_name=f, last_name=l, email=f"{f}.{l}{1000+i}@example.com".lower(), phone=phone(),
                     lead_source=random.choice(SOURCES), city=random.choice(CITIES), province="ON", created_date=date()))
random.shuffle(rows)
for i, r in enumerate(rows, 1):
    r["crm_id"] = f"C{i:05d}"; r.pop("lead_id", None)

with open("data/source_leads.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(source[0])); w.writeheader(); w.writerows(source)
cols = ["crm_id","first_name","last_name","email","phone","lead_source","city","province","created_date"]
with open("data/crm_export.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(source), "source leads;", len(rows), "CRM rows")
