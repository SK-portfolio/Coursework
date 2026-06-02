package ie.tcd.komolafs;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.LowerCaseFilter;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.en.PorterStemFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;

public class CustomEnglishAnalyzer extends Analyzer {
    @Override
    protected TokenStreamComponents createComponents(String fieldName) {
        Tokenizer tokenizer = new StandardTokenizer();
        // Use EnglishAnalyzer's default stopwords
        CharArraySet stopWords = EnglishAnalyzer.getDefaultStopSet();
        TokenStream stream = new LowerCaseFilter(tokenizer);
        stream = new StopFilter(stream, stopWords);
        stream = new PorterStemFilter(stream);
        return new TokenStreamComponents(tokenizer, stream);
    }
}
