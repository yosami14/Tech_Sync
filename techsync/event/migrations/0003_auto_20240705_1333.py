# Example: event/migrations/00XX_auto_add_event_categories.py

from django.db import migrations

# Function to add event categories
def add_event_categories(apps, schema_editor):
    EventCategory = apps.get_model('event', 'EventCategory')
    categories = [
        "Industry News",
        "Company News",
        "Product Launches",
        "Technology Trends",
        "Startups",
        "Gadget Reviews",
        "Software Reviews",
        "App Reviews",
        "Hardware Reviews",
        "Programming Tutorials",
        "Software Development",
        "Web Development",
        "Mobile Development",
        "Data Science and AI",
        "Cybersecurity",
        "Buying Guides",
        "Setup Guides",
        "Troubleshooting Guides",
        "Expert Opinions",
        "Market Analysis",
        "Tech Policy and Ethics",
        "Conferences and Meetups",
        "Webinars",
        "Workshops",
        "Hackathons",
        "Specs and Features",
        "Comparisons",
        "Updates and Upgrades",
        "User Reviews",
        "Expert Reviews",
        "Top Picks",
        "Industry Leaders",
        "Innovators",
        "Tech Entrepreneurs",
        "Job Listings",
        "Career Advice",
        "Online Courses",
        "Certifications",
        "Emerging Technologies",
        "Research and Development",
        "Innovations",
        "User Discussions",
        "Q&A",
        "Project Showcases",
        "Tech in Everyday Life",
        "Smart Home",
        "Wearables",
        "Tech Deals",
        "Discounts",
        "Promotions",
        "Tech Research",
        "Scientific Discoveries",
        "Academic Papers",
        "Columns",
        "Editorials",
        "Guest Posts",
    ]
    for category in categories:
        EventCategory.objects.get_or_create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_initial'),  # Previous migration file
    ]

    operations = [
        migrations.RunPython(add_event_categories),
    ]


