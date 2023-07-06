/*
 * Copyright © 2017 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.google.enterprise.cloudsearch.sdk.indexing.template;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;
import static com.google.common.base.Preconditions.checkState;
import static com.google.common.base.Strings.isNullOrEmpty;

import com.google.common.annotations.VisibleForTesting;
import com.google.common.io.ByteStreams;
import com.google.enterprise.cloudsearch.sdk.config.Configuration;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 * Object used to manage storing checkpoints to local disc.
 *
 * <p>Optional configuration file parameters used:
 *
 * <ul> <li>{@value CONNECTOR_CHECKPOINT_DIRECTORY} - Specifies the directory to use for storing
 * traversal checkpoints. Default is the current directory.</ul>
 */
class LocalFileCheckpointHandler implements CheckpointHandler {
  private static final Logger logger = Logger.getLogger(LocalFileCheckpointHandler.class.getName());

  public static final String CONNECTOR_CHECKPOINT_DIRECTORY = "connector.checkpointDirectory";
  @VisibleForTesting static final String DEFAULT_CHECKPOINT_DIRECTORY = "./WEB-INF/classes";
  
  private final Path basePath;
  private final FileHelper fileHelper;

  public String[] checkPoint_Array = {"{", "\"operationName\"", ":", "\"\"", ",", "\"queueName\"", ":", "\"FullTraversal||B: DatabaseRepository\"", "}"};
  public String checkPoint_String;
  JSONObject checkPoint_JSON;

  @VisibleForTesting
  LocalFileCheckpointHandler(String directory, FileHelper fileHelper) {
    String checkpointDir =
        checkNotNull(directory, "checkpoint directory can not be null").trim();
    this.basePath = FileSystems.getDefault().getPath(checkpointDir);
    this.fileHelper = checkNotNull(fileHelper);
  }

  @VisibleForTesting
  Path getCheckpointFilePath(String checkpointName) {
    checkState(!isNullOrEmpty(checkpointName), "checkpoint name can't be null or empty");
    return basePath.resolve(checkpointName);
  }

  static LocalFileCheckpointHandler fromConfiguration() {
    checkState(Configuration.isInitialized(), "Configuration object not initialized");
    return new LocalFileCheckpointHandler(
        Configuration.getString(CONNECTOR_CHECKPOINT_DIRECTORY, DEFAULT_CHECKPOINT_DIRECTORY).get(),
        new FileHelper());
  }

  public JSONObject CreateCheckPoint(String originString) {
    try {
        checkPoint_String = "";
        for (int i = 0; i < checkPoint_Array.length; i++) {
            checkPoint_String += checkPoint_Array[i];
        }
        System.out.println(checkPoint_String);
        checkPoint_JSON = (JSONObject) new JSONParser().parse(checkPoint_String);
    } catch (ParseException e) {
        e.printStackTrace();
    }

    return checkPoint_JSON;
  }

  @Override
  public byte[] readCheckpoint(String checkpointName) throws IOException {
    logger.log(Level.INFO, "readCheckpoint {0}", CreateCheckPoint(checkPoint_String).toString().getBytes(StandardCharsets.UTF_8));
    return CreateCheckPoint(checkPoint_String).toString().getBytes(StandardCharsets.UTF_8);
    // return getCheckpointContent(getCheckpointFilePath(checkpointName));
  }

  @Override
  public void saveCheckpoint(String checkpointName, byte[] checkpoint) throws IOException {
    writeCheckpoint(getCheckpointFilePath(checkpointName), checkpoint);
    logger.log(Level.INFO, "writeCheckpoint {0}", checkPoint_Array.toString());
  }

  // private byte[] getCheckpointContent(Path checkpointFilePath) throws IOException {
  //   File checkpointFile = fileHelper.getFile(checkpointFilePath);
  //   if (!checkpointFile.exists()) {
  //     return null;
  //   }
  //   checkArgument(checkpointFile.isFile(), "checkpoint file is not pointing to file");
  //   return fileHelper.readFile(checkpointFile);
  // }

  private void writeCheckpoint(Path checkpointFilePath, byte[] payload) throws IOException {
    File checkpointFile = fileHelper.getFile(checkpointFilePath);
    boolean exists = checkpointFile.exists();
    checkArgument(
        !exists || checkpointFile.isFile(),
        "checkpoint file is not pointing to file");
    if (payload == null) {
      if (exists) {
        // delete checkpoint file if current checkpoint is null
        checkpointFile.delete();
      }
      return;
    }
    String checkPoint_String = new String(payload);
    String[] checkPoint = checkPoint_String.split("\"");

    checkPoint_Array[3] = "\"" + checkPoint[3] + "\"";
    checkPoint_Array[7] = "\"" + checkPoint[7] + "\"";

    // fileHelper.writeFile(checkpointFile, payload);
  }

  /** Helper utility to wrap File operations and testing */
  static class FileHelper {

    File getFile(Path filePath) {
      return filePath.toFile();
    }

    byte[] readFile(File file) throws IOException {
      try (FileInputStream inputStream = new FileInputStream(file)) {
        return ByteStreams.toByteArray(inputStream);
      }
    }

    void writeFile(File file, byte[] content) throws IOException {
      // try (FileOutputStream outputStream =
      //     new FileOutputStream(
      //         file,
      //         // append is false. Overwrite file
      //         false)) {
      //   outputStream.write(content);
      //   outputStream.flush();
      // }
    }
  }
}
