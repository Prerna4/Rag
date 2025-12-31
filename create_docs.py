"""
Create sample documents for the RAG system.
Run this script to generate the docs/ directory with sample .txt files.
"""

import os

def create_sample_documents():
    """Create sample documents in docs/ directory"""
    
    # Create docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Document 1: Product Manual - UltraBlend 3000
    doc1 = """UltraBlend 3000 User Manual

Welcome to your new UltraBlend 3000 blender! This powerful kitchen appliance is designed to make your food preparation easier and more efficient.

Product Overview:
The UltraBlend 3000 features a 1200-watt motor, stainless steel blades, and a 64-ounce pitcher. It includes 10 speed settings and 3 preset programs for smoothies, ice crushing, and soup making.

Warranty Information:
The UltraBlend 3000 comes with a comprehensive 2-year warranty covering all manufacturing defects. This warranty includes free replacement of defective parts and labor costs. Extended warranty options are available for purchase.

Maintenance and Care:
To maintain optimal performance, clean the blender after each use. The pitcher and lid are dishwasher safe. Wipe the motor base with a damp cloth. For best results, replace the blades every 18-24 months depending on usage frequency.

Scheduling Maintenance:
For professional maintenance or repairs, you can schedule a service appointment by calling our support line at 1-800-BLEND-NOW or visiting our website at ultrablend.com/service, Our technicians are available Monday through Friday, 8 AM to 6 PM EST.

Safety Features:
The UltraBlend 3000 includes multiple safety features such as automatic shut-off when the pitcher is removed, overload protection, and a locking lid mechanism to prevent spills during operation.

Troubleshooting:
If your blender stops working, first check that it is properly plugged in and the pitcher is correctly seated on the base. If problems persist, contact customer service for assistance.

"""

    # Document 2: Product Manual - SafeGrill Pro
    doc2 = """SafeGrill Pro Electric Grill Manual

Thank you for purchasing the SafeGrill Pro electric grill! This indoor/outdoor grill offers safe and convenient grilling year-round.

Product Features:
The SafeGrill Pro includes a non-stick grilling surface, adjustable temperature control, and a removable drip tray for easy cleaning, The grill heats up to 450°F and has a cooking surface of 240 square inches.

Safety Features:
The SafeGrill Pro is equipped with an auto-shutoff feature that activates if the unit overheats. The cool-touch handles ensure you can safely move the grill even during operation. A built-in timer with auto-shutoff prevents overcooking and potential fire hazards.

Warranty Coverage:
Your SafeGrill Pro is covered by a 1-year limited warranty. This covers defects in materials and workmanship. The heating element is covered for up to 3 years with proper registration.

Cleaning Instructions:
Allow the safegrill pro to cool completely before cleaning,Remove the drip tray and wash with warm soapy water,The grilling surface can be wiped clean with a damp cloth or sponge. Never immerse the main unit in water.

Operation Guidelines:
Preheat the safegrill pro for 5-10 minutes before cooking, Use the temperature dial to select your desired heat level and Always use heat-resistant utensils to avoid damaging the non-stick surface.

Customer Support:
For questions or concerns, contact SafeGrill customer service at support@safegrill.com or call 1-888-GRILL-4U. Our representatives are available 24/7 to assist you.

"""

    # Document 3: Employee Handbook
    doc3 = """TechCorp Employee Handbook

Welcome to TechCorp! This handbook contains important information about your employment, benefits, and company policies.

Time Off and Leave Policies:

Paid Time Off (PTO):
New employees receive 15 days of paid leave per year and After 3 years of service, this increases to 20 days annually. 

Holidays:
TechCorp observes 10 federal holidays each year, including New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving, and Christmas. These are paid holidays for all full-time employees.

Sick Leave:
In addition to PTO, employees receive 5 days of sick leave per year. Unused sick leave does not roll over to the next year. Employees must notify their supervisor as soon as possible when taking sick leave.

Parental Leave:
New parents are eligible for 12 weeks of paid parental leave. This applies to birth parents, adoptive parents, and foster parents. Leave must be taken within the first year of the child's arrival.

Work Hours and Schedule:
Standard work hours are 9 AM to 5 PM, Monday through Friday. We offer flexible scheduling options for eligible employees. Remote work arrangements are available with manager approval.

Benefits Overview:
TechCorp offers comprehensive health insurance, dental and vision coverage, 401(k) retirement plan with company matching, life insurance, and professional development opportunities.

Code of Conduct:
All employees are expected to maintain professional behavior, respect confidentiality, and adhere to company values of integrity, innovation, and collaboration.

"""

    # Document 4: Return Policy
    doc4 = """Company Return and Refund Policy

At ShopSmart, customer satisfaction is our priority. We want you to be completely happy with your purchase.

Return Window:
You may return most items within 30 days of delivery for a full refund. Some exclusions apply, including personalized items, perishable goods, and opened software or media.

Return Process:
To initiate a return, log into your account and select the order you wish to return. Print the prepaid return label and package the item securely in its original packaging if possible. Drop off the package at any authorized shipping location.

Refunds process:
Once we receive your returned item, our team will inspect it within 2-3 business days and refund will appear in 5-7 days and For returns made after 30 days but within 60 days, store credit will be issued instead of a refund.

Defective or Damaged Items:
If you receive a defective or damaged item, please contact us immediately, We will provide a prepaid return label and expedite your refund or replacement. You will not be charged return shipping for defective items.

Exchange Policy:
We do not offer direct exchanges, To exchange an item, please return the original item for a refund and place a new order for the desired product. 

Non-Returnable Items:
Items marked as final sale, gift cards, downloadable software, and intimate apparel cannot be returned and Custom orders are also non-returnable unless defective.
"""

    # Write documents to files
    documents = {
        'ultrablend_manual.txt': doc1,
        'safegrill_manual.txt': doc2,
        'employee_handbook.txt': doc3,
        'return_policy.txt': doc4
    }
    
    for filename, content in documents.items():
        filepath = os.path.join('docs', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filepath}")
    
    print(f"\nSuccessfully created {len(documents)} sample documents in 'docs/' directory")


if __name__ == "__main__":
    create_sample_documents()