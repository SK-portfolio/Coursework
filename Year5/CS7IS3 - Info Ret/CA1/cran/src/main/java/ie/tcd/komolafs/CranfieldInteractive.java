package ie.tcd.komolafs;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.similarities.*;
import org.apache.lucene.store.*;

import java.io.IOException;
import java.nio.file.*;
import java.util.Scanner;

public class CranfieldInteractive{
        //default settings(no command line args)
    private static final String DEFAULT_INDEX = "index";
    private static final String DEFAULT_ANALYZER = "english";
    private static final String DEFAULT_SIMILARITY = "bm25";
    private static final int MAX_RESULTS = 10; //max # of results printed per query
        //read command line args
    public static void main(String[] args) throws IOException, ParseException {
        String indexPath = args.length > 0 ? args[0] : DEFAULT_INDEX;
        String analyzerName = args.length > 1 ? args[1].toLowerCase() : DEFAULT_ANALYZER;
        String simName = args.length > 2 ? args[2].toLowerCase() : DEFAULT_SIMILARITY;

        //-------------------Choose Analyzer-------------------
        Analyzer analyzer;
        switch (analyzerName) {
            case "standard": analyzer = new StandardAnalyzer(); break;
            case "whitespace": analyzer = new WhitespaceAnalyzer(); break;
            case "english":
                //default to EnglishAnalyzer(tokenisation, lowercasing, stop-word removal, stemming)
            default: analyzer = new EnglishAnalyzer(); break;
        }

        //-------------------Choose Similarity Model-------------------
        Similarity similarity;
	if (simName.startsWith("bm25")) {
    		similarity = new BM25Similarity(1.0f, 0.3f); // tuned BM25 for short docs
	} else {
    		similarity = new ClassicSimilarity();   // <- (TF-IDF / Vector Space Model)
	}

        //-------------------Index Exists?-------------------
        Path indexDir = Paths.get(indexPath);
            //if index directory does not exist or is empty
        if (!Files.exists(indexDir) || indexDir.toFile().list() == null || indexDir.toFile().list().length == 0) {
            System.err.println("Error: No index found at '" + indexPath + "'.");
            System.err.println("Please run CranfieldIndexer first to build the index.");
            return;
        }

        //-------------------Open Index-------------------
        Directory directory = FSDirectory.open(indexDir);           //get index directory
        DirectoryReader reader = DirectoryReader.open(directory);   //open index for reading 
        IndexSearcher searcher = new IndexSearcher(reader);         //use reader to create searcher
        searcher.setSimilarity(similarity);                         //set chosen similarity model
            //parse query text into lucene query object
        QueryParser parser = new QueryParser("content", analyzer);
            //to scan for user input
        Scanner scanner = new Scanner(System.in);
        String queryString;

        System.out.println("Cranfield Search");
        System.out.println("Type a query (\\q to quit)");
        System.out.println("------------------------------------");

        System.out.print(">>> ");
            //read user queries until \q is entered
        while (!(queryString = scanner.nextLine().trim()).equals("\\q")) {
            if (queryString.isEmpty()) {
                System.out.print(">>> ");
                continue;
            }

            try {
                    //convert user query into query object(& escape special characters)
                Query query = parser.parse(QueryParser.escape(queryString));
                    //retrieve top results
                TopDocs results = searcher.search(query, MAX_RESULTS);
                    //display results
                System.out.println("\nTop " + results.scoreDocs.length + " results:");
                int rank = 1;
                    //for each result, retrieve document & print details
                for (ScoreDoc sd : results.scoreDocs) {
                    Document d = searcher.doc(sd.doc);
                        //print rank, docID, rel score, title
                    System.out.printf("%2d. DocID=%s | Score=%.4f | Title=%s%n",
                            rank++, d.get("id"), sd.score, d.get("title"));
                }
                System.out.println();

            } 
            catch (ParseException e) {
                    //handle invalid query syntax
                System.out.println("Invalid query: " + e.getMessage());
            }
            System.out.print(">>> ");   //prompt for next query
        }
        //-------------------Cleanup & Exit-------------------
        reader.close();
        directory.close();
        scanner.close();
        System.out.println("Goodbye!");
    }
}
