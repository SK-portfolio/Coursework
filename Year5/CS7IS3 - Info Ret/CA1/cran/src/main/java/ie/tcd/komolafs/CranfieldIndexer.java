package ie.tcd.komolafs;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.search.similarities.ClassicSimilarity;
import org.apache.lucene.search.similarities.Similarity;
import java.io.*;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.util.*;

public class CranfieldIndexer {
	//------------------------------------------------------------------------------------
        //read in command arguments (& init defaults)
    public static void main(String[] args) throws Exception {
        String indexPath = args.length > 0 ? args[0] : "index";                     //index file path
        String docsPath = args.length > 1 ? args[1] : "cran.all.1400";              //cranfield doc file path
        String queryPath = args.length > 2 ? args[2] : "cran.qry";                  //cranfield query file path
        String outPrefix = args.length > 3 ? args[3] : "results";                   //TREC result file prefix
        String analyzerName = args.length > 4 ? args[4].toLowerCase() : "english";  //which analyzer
        String simName = args.length > 5 ? args[5].toLowerCase() : "bm25";          //which similarity model ()

        System.out.println("Index: " + indexPath + ", docs: " + docsPath + ", queries: " + queryPath);
        System.out.println("Analyzer: " + analyzerName + ", Similarity: " + simName);
            //choose analyzer
        Analyzer analyzer;
        switch (analyzerName) {
    		case "standard": analyzer = new StandardAnalyzer(); break;
    		case "whitespace": analyzer = new WhitespaceAnalyzer(); break;
    		//case "custom": analyzer = new CustomEnglishAnalyzer(); break;
    		case "english":
    		default: analyzer = new EnglishAnalyzer(); break;
	    }
            //choose similarity model
        Similarity similarity = simName.startsWith("bm25") ? new BM25Similarity() 
                                : new ClassicSimilarity();      //(ClassicSimilarity -> VSM)

        // ------------------ INDEXING ------------------
        Directory dir = FSDirectory.open(Paths.get(indexPath));     //get index from directory
            //setup IndexWriter with chosen analyzer
        IndexWriterConfig iwc = new IndexWriterConfig(analyzer);
        iwc.setOpenMode(IndexWriterConfig.OpenMode.CREATE);          //create new index 
            //open index stored in dir & apply iwc config
        IndexWriter writer = new IndexWriter(dir, iwc); 
            //parse cranfield docs & add to index
        Map<String, String[]> docs = parseCranfieldDocs(docsPath);
            //for each doc, create Lucene Document & add index it
        for (Map.Entry<String, String[]> e : docs.entrySet()) {
            Document doc = new Document();
            doc.add(new StringField("id", e.getKey(), Field.Store.YES));
            doc.add(new TextField("title", e.getValue()[0], Field.Store.YES));
                // store full text (title+text) for searching
            String full = (e.getValue()[0] + " " + e.getValue()[1]).trim();
            doc.add(new TextField("content", full, Field.Store.YES));
                //add doc to index
            writer.addDocument(doc);
        }
        writer.close();
        System.out.println("Indexing complete. Documents indexed: " + docs.size());

        // ------------------ SEARCH ------------------
            //open search index
        DirectoryReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)));
        IndexSearcher searcher = new IndexSearcher(reader);
            //apply chosen similarity model
        searcher.setSimilarity(similarity);
            //load queries
        Map<String, String> queries = parseCranfieldQueries(queryPath);
            //prepare output file (eg. results-english-bm25.txt)
        String runTag = analyzerName + "-" + simName;
        String outFile = outPrefix + "-" + runTag + ".txt";
        DecimalFormat df = new DecimalFormat("0.000000");                   //format scores
        BufferedWriter out = new BufferedWriter(new FileWriter(outFile));
            //convert text to lucene query
        QueryParser parser = new QueryParser("content", analyzer);
            //for each query-search & write results(TREC format)
        for (Map.Entry<String, String> q : queries.entrySet()) {
            String qid = q.getKey();  // now sequential: 1,2,3...
            String qtext = q.getValue().trim();
            if (qtext.isEmpty()) continue;
            Query query = parser.parse(QueryParser.escape(qtext));  //escape special characters & parse query
            TopDocs topDocs = searcher.search(query, 1000);         //get top 1000 results
                //write results in TREC format
            int rank = 1;
            for (ScoreDoc sd : topDocs.scoreDocs) {
                Document d = searcher.doc(sd.doc);
                out.write(String.format("%s Q0 %s %d %s %s%n", qid, d.get("id"),
                                        rank, df.format(sd.score), runTag));
                rank++;
            }
        }

        out.close();
        reader.close();
        System.out.println("Search complete. Results written to: " + outFile);
    }

	// ------------------ PARSE ------------------ (.I, .T, .W, .A, ...)
    private static Map<String, String[]> parseCranfieldDocs(String filePath) throws IOException {
            //make map of doc id -> [title, text]
        Map<String, String[]> docs = new LinkedHashMap<>();
            //get cran.all.1400
        BufferedReader br = new BufferedReader(new FileReader(filePath));
            // init line to parse per line
        String line;
            //init current doc id, title, text, section
        String id = null, title = "", text = "", section = "";
            //while line in file is not null-read line
        while ((line = br.readLine()) != null) {
            if (line.startsWith(".I")) {    //query id
                    //save previous doc before new
                if (id != null) docs.put(id, new String[]{title.trim(), text.trim()});
                id = line.split("\\s+")[1];
                title = "";
                text = "";
                section = "";
            } 
                //.T = title, .W = query text 
            else if (line.startsWith(".T")) section = "title";
            else if (line.startsWith(".W")) section = "text";
                //.A/.B/.K/.C = ignore
            else if (line.startsWith(".A") || line.startsWith(".B") || line.startsWith(".K") || line.startsWith(".C")) section = "";
            else {
                if ("title".equals(section)) title += line + " ";   //append line to title
                if ("text".equals(section)) text += line + " ";     //append line to text
            }
        }
            //save last doc
        if (id != null) docs.put(id, new String[]{title.trim(), text.trim()});
        br.close();
        return docs;
    }
	// ------------------ PARSE ------------------ (.I, .W only)
    private static Map<String, String> parseCranfieldQueries(String filePath) throws IOException {
    Map<String, String> queries = new LinkedHashMap<>();
    BufferedReader br = new BufferedReader(new FileReader(filePath));
    String line;
    StringBuilder text = new StringBuilder();
    boolean inQuery = false;
    int sequentialId = 1; //queries renumbered 1-225

    while ((line = br.readLine()) != null) {
        line = line.trim();             //trim whitespace
        if (line.startsWith(".I")) {
            if (text.length() > 0) {    //save previous query
                queries.put(String.valueOf(sequentialId++), text.toString().trim());
                text.setLength(0);
            }
            inQuery = false;
        } else if (line.startsWith(".W")) { //start of query text
            inQuery = true;
        } else if (inQuery) {
            text.append(line).append(" ");  //add terms while in .W section
        }
    }
        // add last query
    if (text.length() > 0) {
        queries.put(String.valueOf(sequentialId++), text.toString().trim());
    }
        //close reader & return queries
    br.close();
    return queries;
    }
	//------------------------------------------------------------------------------------
}