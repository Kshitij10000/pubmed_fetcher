# cli.py
import sys
import argparse
from typing import List, Dict, Any
from paper_fetcher.fetcher import fetch_articles, filter_articles, save_to_csv

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed based on a query."
    )
    parser.add_argument("query", type=str, help="Search query for fetching research papers.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information during execution.")
    parser.add_argument("-f", "--file", type=str, help="Specify the filename to save the results as CSV.")
    return parser.parse_args()

def main() -> None:
    args = parse_arguments()

    if args.debug:
        print("Debug Mode: ON")
        print(f"Query: {args.query}")

    try:
        article_ids, articles = fetch_articles(args.query)
    except Exception as err:
        print(f"An error occurred while fetching articles: {err}")
        sys.exit(1)

    if not articles:
        print("No articles found.")
        sys.exit(0)

    filtered_results: List[Dict[str, Any]] = filter_articles(articles)
    if not filtered_results:
        print("No articles matched the filtering criteria.")
        sys.exit(0)

    # If filename is provided, save results to CSV; otherwise, print to console.
    if args.file:
        try:
            save_to_csv(filtered_results, args.file)
            print(f"Results saved to {args.file}")
        except Exception as e:
            print(f"Failed to save CSV: {e}")
    else:
        # Print to console
        for entry in filtered_results:
            print(f"PubMed ID: {entry.get('PubmedID')}")
            print("Title:", entry.get("Title"))
            print("Publication Date:", entry.get("Publication Date"))
            print("Non-academic Authors:", entry.get("Non-academic Authors"))
            print("Company Affiliations:", entry.get("Company Affiliations"))
            print("Corresponding Emails:", entry.get("Corresponding Emails"))
            print("-" * 40)

if __name__ == "__main__":
    main()
