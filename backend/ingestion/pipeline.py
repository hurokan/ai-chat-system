from ingestion.loader import Loader
from ingestion.embedder import Embedder


class Pipeline:

    def run(self):

        print("Starting chunking...")
        Loader().run()

        print("Starting embedding...")
        Embedder().run()

        print("Pipeline completed successfully")