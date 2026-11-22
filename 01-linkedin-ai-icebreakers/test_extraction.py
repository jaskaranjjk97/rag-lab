from modules.data_extraction import extract_linkedin_profile
from modules.data_preprocessing import split_profile_data

profile_url=profile_url = ("https://www.linkedin.com/in/bharat-gaurav-ab12ec/"
)

profile=extract_linkedin_profile(
    linkedin_profile_url=profile_url,
    mock=False,
)

print("\nProfile extracted successfully!")
print("Name:", profile.get("full_name"))
print("Headline:", profile.get("headline"))
print("Skills:", len(profile.get("skills", [])))
print("Experience:", len(profile.get("position_groups", [])))
print("Education:", len(profile.get("educations", [])))

for group in profile.get("position_groups", []):
    company = group.get("company", {})
    print("\nCompany:", company.get("name", ""))

    for position in group.get("profile_positions", []):
        print("Title:", position.get("title"))
        print("Description:", position.get("description"))
        print("Date:", position.get("date"))


# Test preprocessing and chunking
nodes = split_profile_data(profile)

print("\n========== PREPROCESSING RESULTS ==========")
print("Total nodes created:", len(nodes))

for i, node in enumerate(nodes):
    print(f"\n--- Node {i + 1} ---")
    print("Section:", node.metadata.get("section"))
    print("Company:", node.metadata.get("company"))
    print("Position:", node.metadata.get("position"))
    print("Content:", node.text[:1000])


print("\n========== NODE LENGTH ANALYSIS ==========")

for i, node in enumerate(nodes):
    print(
        f"Node {i + 1}: "
        f"{len(node.text)} characters | "
        f"{node.metadata.get('section')} | "
        f"{node.metadata.get('company', '')}"
    )

# Check important Deloitte information
deloitte_text = "\n".join(
    node.text for node in nodes
    if node.metadata.get("company") == "Deloitte"
)

keywords = [
    "$3.2B",
    "2030 strategic plan",
    "40% reduction",
    "GenAI",
    "20+ Deloitte Member Firms"
]

print("\n========== DELOITTE CONTENT CHECK ==========")

for keyword in keywords:
    print(keyword, ":", keyword.lower() in deloitte_text.lower())