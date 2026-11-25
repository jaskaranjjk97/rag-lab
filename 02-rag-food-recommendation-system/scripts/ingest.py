import argparse
from src.vector_store import build_index

def main():
    parser=argparse.ArgumentParser(description="Ingest food records into ChromaDB.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete the existing collection and rebuild it."
    )
    args=parser.parse_args()
    collection=build_index(rebuild=args.rebuild)

    print("\n Ingestion succesfully completed.")
    print(f"Collection Name:{collection.name}")
    print(f"Total records:{collection.count()}")

if __name__=="__main__":
    main()