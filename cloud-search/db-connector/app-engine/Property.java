package com.google.enterprise.cloudsearch.sdk.config;

import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Property {
    private static final Logger logger = Logger.getLogger(Property.class.getName());

    public Properties config(){
        Properties props = new Properties();
        props.setProperty("api.sourceId","");
        props.setProperty("api.identitySourceId","");
        props.setProperty("api.serviceAccountPrivateKeyFile","./WEB-INF/classes/PrivateKey.json");

        props.setProperty("db.url","");
        props.setProperty("db.user","");
        props.setProperty("db.password","");

        props.setProperty("db.allRecordsSql","SELECT guestName, content, entryID FROM entries");

        props.setProperty("db.timestamp","1679990930");

        props.setProperty("db.allColumns","guestName, content, entryID");
        props.setProperty("db.contentColumns","guestName, content, entryID");
        props.setProperty("db.uniqueKeyColumns","entryID");
        props.setProperty("url.columns","entryID");

        props.setProperty("contentTemplate.db.title","entryID");

        props.setProperty("defaultAcl.mode","fallback");
        props.setProperty("defaultAcl.public","true");

        props.setProperty("schedule.traversalIntervalSecs","36000");
        props.setProperty("schedule.performTraversalOnStart","true");
        props.setProperty("schedule.incrementalTraversalIntervalSecs","3600");

        return props;
    }
}
