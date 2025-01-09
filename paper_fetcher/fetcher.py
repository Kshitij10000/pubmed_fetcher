# paper_fetcher/fetcher.py
from typing import Tuple, List, Dict, Any, Optional
from Bio import Entrez
import re
import csv

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch credentials from environment variables
EMAIL: str = os.getenv("EMAIL")
API_KEY: str = os.getenv("API_KEY")

if not EMAIL or not API_KEY:
    raise EnvironmentError("EMAIL and API_KEY must be set in the environment.")

Entrez.email = EMAIL
Entrez.api_key = API_KEY

def fetch_articles(query: str, max_results: int = 20) -> Tuple[List[str], Optional[Dict[str, Any]]]:
    """Fetch articles from PubMed based on a query."""
    try:
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        search_results = Entrez.read(search_handle)
        search_handle.close()
    except Exception as e:
        raise RuntimeError(f"Error during search: {e}")

    article_ids = search_results.get("IdList", [])
    if not article_ids:
        return [], None

    try:
        fetch_handle = Entrez.efetch(db="pubmed", id=",".join(article_ids), retmode="xml")
        articles = Entrez.read(fetch_handle)
        fetch_handle.close()
    except Exception as e:
        raise RuntimeError(f"Error during fetching articles: {e}")

    return article_ids, articles

def extract_article_info(article: Dict[str, Any]) -> Dict[str, Any]:
    """Extract required information from an article record."""
    title: str = "No title"
    pub_date: str = "Unknown"
    non_academic_authors: List[str] = []
    company_affiliations: List[str] = []
    corresponding_emails: List[str] = []

    # Extract title
    try:
        title = article["MedlineCitation"]["Article"].get("ArticleTitle", title)
    except KeyError:
        pass

    # Extract publication date
    try:
        journal_issue = article["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]
        pub_date_info = journal_issue.get("PubDate", {})
        year = pub_date_info.get("Year", "")
        month = pub_date_info.get("Month", "")
        day = pub_date_info.get("Day", "")
        pub_date = " ".join(filter(None, [year, month, day])).strip() or "Unknown"
    except KeyError:
        pass

    # Process authors and affiliations
    authors = article["MedlineCitation"]["Article"].get("AuthorList", [])
    for author in authors:
        affiliations = author.get("AffiliationInfo", [])
        for aff_info in affiliations:
            affiliation = aff_info.get("Affiliation", "")
            affiliation_lower = affiliation.lower()

            # Extract emails using regex
            found_emails = re.findall(r'[\w\.-]+@[\w\.-]+', affiliation)
            corresponding_emails.extend(found_emails)

            # Heuristic for non-academic affiliations
            academic_keywords = ["university", "college", "institute", "hospital", "clinic", "school"]
            if affiliation and not any(keyword in affiliation_lower for keyword in academic_keywords):
                non_academic_authors.append(affiliation)

            # Heuristic for company affiliations
            company_keywords = ["inc", "ltd", "corp", "pharma", "biotech", "company", "corp.", "llc", "gmbh"]
            if affiliation and any(keyword in affiliation_lower for keyword in company_keywords):
                company_affiliations.append(affiliation)

    # Remove duplicates
    non_academic_authors = list(set(non_academic_authors))
    company_affiliations = list(set(company_affiliations))
    corresponding_emails = list(set(corresponding_emails))

    return {
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Authors": non_academic_authors,
        "Company Affiliations": company_affiliations,
        "Corresponding Emails": corresponding_emails
    }

def filter_articles(articles: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filter articles to only include those with at least one non-academic author affiliated with a company."""
    filtered_results = []
    if not articles or "PubmedArticle" not in articles:
        return filtered_results

    for article in articles["PubmedArticle"]:
        info = extract_article_info(article)
        # Check if at least one company affiliation exists
        if info["Company Affiliations"]:
            pmid = article["MedlineCitation"].get("PMID", "Unknown")
            info["PubmedID"] = str(pmid)
            filtered_results.append(info)

    return filtered_results

def save_to_csv(data: List[Dict[str, Any]], filename: str) -> None:
    """Save the list of article info dictionaries to a CSV file."""
    fieldnames = [
        "PubmedID", 
        "Title", 
        "Publication Date", 
        "Non-academic Authors", 
        "Company Affiliations", 
        "Corresponding Emails"
    ]
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    "PubmedID": entry.get("PubmedID", ""),
                    "Title": entry.get("Title", ""),
                    "Publication Date": entry.get("Publication Date", ""),
                    "Non-academic Authors": "; ".join(entry.get("Non-academic Authors", [])),
                    "Company Affiliations": "; ".join(entry.get("Company Affiliations", [])),
                    "Corresponding Emails": "; ".join(entry.get("Corresponding Emails", []))
                })
    except Exception as e:
        raise RuntimeError(f"Error saving to CSV: {e}")