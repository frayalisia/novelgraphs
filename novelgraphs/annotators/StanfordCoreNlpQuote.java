import java.io.*;
import java.util.*;

import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;

public class StanfordCoreNlpQuote {

  public static void main(String[] args) throws IOException {
    PrintWriter out;
    if (args.length > 1) {
      out = new PrintWriter(args[1]);
    } else {
      out = new PrintWriter(System.out);
    }

    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, quote");
    props.put("quote.singleQuotes", "true");
    // props.put("quote.asciiQuotes", "true");
    props.put("tokenize.whitespace", "true");
    props.put("ssplit.eolonly", "true");

    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

    Annotation annotation;
    if (args.length > 0) {
      annotation = new Annotation(IOUtils.slurpFileNoExceptions(args[0]));
    } else {
      annotation = new Annotation("Kosgi Santosh sent an email to Stanford University. He did not get a reply.");
    }

    pipeline.annotate(annotation);

    List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
    for(CoreMap sentence: sentences) {
      for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {
        String text = token.get(CoreAnnotations.OriginalTextAnnotation.class);
        Integer quotation = token.get(CoreAnnotations.QuotationIndexAnnotation.class);
        System.out.println(text + "\t" + quotation);
      }
    }
  }
}
