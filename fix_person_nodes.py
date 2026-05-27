#!/usr/bin/env python3
"""
Enrich and normalize Person schema nodes across all HTML pages.
- index.html (Pattern A): replace stub with full enriched Person block
- all others (Pattern B): replace every "@type":"Person" object with @id pointer
"""
import re
import os

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_object_end(text, start):
    """Return index of the closing '}' of the JSON object that opens at 'start'."""
    depth = 0
    i = start
    in_string = False
    escape_next = False
    while i < len(text):
        ch = text[i]
        if escape_next:
            escape_next = False
        elif ch == '\\' and in_string:
            escape_next = True
        elif ch == '"':
            in_string = not in_string
        elif not in_string:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def replace_person_objects(content, inline_ptr, standalone_ptr):
    """Replace every {"@type":"Person",...} object in content with the pointer."""
    result = []
    i = 0
    pattern = re.compile(r'"@type"\s*:\s*"Person"')

    while True:
        m = pattern.search(content, i)
        if not m:
            result.append(content[i:])
            break

        abs_pos = m.start()

        # Find the opening brace of this Person object
        obj_start = content.rfind('{', 0, abs_pos)
        if obj_start == -1:
            result.append(content[i:])
            break

        obj_end = find_object_end(content, obj_start)
        if obj_end == -1:
            result.append(content[i:])
            break

        obj_text = content[obj_start:obj_end + 1]

        # Standalone if it owns @context
        replacement = standalone_ptr if '"@context"' in obj_text else inline_ptr

        result.append(content[i:obj_start])
        result.append(replacement)
        i = obj_end + 1

    return ''.join(result)


# ---------------------------------------------------------------------------
# Pattern A replacement string for index.html
# (indented to match the 8-space object in @graph)
# ---------------------------------------------------------------------------

ENRICHED_PERSON = '''{
            "@type": "Person",
            "@id": "https://meltke.com/#person",
            "name": "Frank Meltke",
            "url": "https://meltke.com",
            "description": "German inventor, founder and CEO of contraco, guest lecturer at Kyung Hee University in Seoul, and Insight Panelist at BBC Global Minds. Specializing in search systems and AI transformation since 1998.",
            "jobTitle": [
                "German Inventor",
                "Founder and CEO of contraco",
                "Guest Lecturer at Kyung Hee University",
                "Insight Panelist at BBC Global Minds"
            ],
            "gender": "Male",
            "birthPlace": { "@type": "Place", "name": "Germany" },
            "homeLocation": { "@type": "Place", "name": "Missouri, USA" },
            "nationality": { "@type": "Country", "name": "Germany" },
            "worksFor": { "@id": "https://contraco.net/#organization" },
            "affiliation": [
                {
                    "@type": "EducationalOrganization",
                    "name": "Kyung Hee University",
                    "url": "https://com.khu.ac.kr/biz_eng/user/contents/view.do?menuNo=14600113",
                    "location": { "@type": "Place", "name": "Seoul, South Korea" }
                },
                {
                    "@type": "Organization",
                    "name": "BBC Global Minds",
                    "url": "https://bbcglobalminds.com/"
                }
            ],
            "alumniOf": {
                "@type": "EducationalOrganization",
                "name": "Fachhochschule des Bundes für öffentliche Verwaltung"
            },
            "hasCredential": [
                {
                    "@type": "EducationalOccupationalCredential",
                    "credentialCategory": "degree",
                    "name": "Diplom",
                    "educationalLevel": "Graduate",
                    "recognizedBy": {
                        "@type": "EducationalOrganization",
                        "name": "Fachhochschule des Bundes für öffentliche Verwaltung"
                    }
                }
            ],
            "award": "Patent DE10313420A1: Search system and method for determining information from a database (2003)",
            "memberOf": {
                "@type": "OrganizationRole",
                "startDate": "2008-05",
                "memberOf": {
                    "@type": "Organization",
                    "name": "i-COM Global"
                }
            },
            "knowsAbout": [
                "Information Retrieval",
                "Search Systems",
                "Digital Transformation",
                "AI Adoption and Change Management",
                "Organisational Design for the AI Era",
                "The Resonance Method",
                "Pricing Psychology",
                "Behavioural Economics",
                "Cross-Cultural Transformation",
                "Enterprise AI Strategy"
            ],
            "knowsLanguage": [
                { "@type": "Language", "name": "English" },
                { "@type": "Language", "name": "German" },
                { "@type": "Language", "name": "Russian" }
            ],
            "image": {
                "@type": "ImageObject",
                "url": "https://meltke.com/Frank_Meltke.png",
                "description": "Frank Meltke: Founder of contraco"
            },
            "sameAs": [
                "https://www.wikidata.org/wiki/Q139680598",
                "https://meltke.com",
                "https://orcid.org/0009-0006-9001-0078",
                "https://scholar.google.com/citations?user=Md3quCcAAAAJ",
                "https://www.linkedin.com/in/frankmeltke",
                "https://www.google.com/search?kgmid=/g/11rqtzq613",
                "https://x.com/frankmeltke",
                "https://mastodon.social/@frankmeltke",
                "https://www.researchgate.net/profile/Frank-Meltke",
                "https://independentresearcher.academia.edu/FrankMeltke",
                "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=11614068",
                "https://speakerhub.com/speaker/frank-meltke",
                "https://gravatar.com/spookyimpossiblyad5a2a54fb",
                "https://isni.org/isni/0000000530311210"
            ]
        }'''

# ---------------------------------------------------------------------------
# Pattern B pointer strings
# ---------------------------------------------------------------------------

INLINE_PTR = '{ "@id": "https://meltke.com/#person" }'
STANDALONE_PTR = '{\n    "@context": "https://schema.org",\n    "@id": "https://meltke.com/#person"\n}'

# ---------------------------------------------------------------------------
# index.html — Pattern A
# ---------------------------------------------------------------------------

def patch_index(content):
    """Replace the stub Person object in @graph with the full enriched block."""
    pattern = re.compile(r'"@type"\s*:\s*"Person"')
    m = pattern.search(content)
    if not m:
        print("index.html: no Person node found!")
        return content

    obj_start = content.rfind('{', 0, m.start())
    obj_end = find_object_end(content, obj_start)
    if obj_start == -1 or obj_end == -1:
        print("index.html: could not find object boundaries!")
        return content

    return content[:obj_start] + ENRICHED_PERSON + content[obj_end + 1:]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

PATTERN_B_FILES = [
    'about.html',
    'ai-adoption-research.html',
    'ai-strategy-framework.html',
    'contact.html',
    'cultural-adaptation-guide.html',
    'copyright.html',
    'cfo-digital-transformation-roi.html',
    'digital-transformation-roi.html',
    'organizational-design-ai.html',
    'leading-ai-transformation.html',
    'resonance-method.html',
    'press.html',
    'privacy-statement.html',
    'insights.html',
    'pricing-psychology.html',
    'vendor-selection-mastery.html',
    'strategic-intelligence.html',
    'thank-you.html',
]

os.chdir('/home/user/contraco-ru')

# index.html — Pattern A
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
new_content = patch_index(content)
if new_content != content:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated: index.html")
else:
    print("No change: index.html")

# Pattern B files
for fname in PATTERN_B_FILES:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = replace_person_objects(content, INLINE_PTR, STANDALONE_PTR)
    if new_content != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {fname}")
    else:
        print(f"No change: {fname}")

print("Done.")
