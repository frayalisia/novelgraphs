import java.io.*;
import java.util.*;

import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;

public class StanfordCoreNlpQuote {

  public static void main(String[] args) throws IOException {
    Properties props = new Properties();
    props = StringUtils.argsToProperties(args);
    props.put("annotators", "tokenize, ssplit, quote");

    String filename = props.getProperty("file");
    props.remove("file");
    Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(filename));
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

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
