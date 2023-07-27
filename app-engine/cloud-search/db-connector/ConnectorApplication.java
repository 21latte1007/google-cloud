package com.example.appengine.demos.springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.google.enterprise.cloudsearch.sdk.indexing.IndexingApplication;
import com.google.enterprise.cloudsearch.sdk.indexing.template.FullTraversalConnector;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

@SpringBootApplication
public class ConnectorApplication {
  private static final Logger logger = Logger.getLogger(ConnectorApplication.class.getName());
  public static void main(String[] args) throws IOException, InterruptedException {
    SpringApplication.run(ConnectorApplication.class, args);
  }
  
  public static String connector() throws InterruptedException {
    String[] args = {};
		IndexingApplication application = new IndexingApplication.Builder(
			new FullTraversalConnector(new DatabaseRepository()), args).build();
		application.start();
    return;
  }
}
