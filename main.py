from knowitall import Crawler

if __name__ == "__main__":
    crawler = Crawler("OPENAI_API_KEY", save_output=True)
    crawler.search_and_summarise("Transformer Models")
    crawler.write_to_file()
    