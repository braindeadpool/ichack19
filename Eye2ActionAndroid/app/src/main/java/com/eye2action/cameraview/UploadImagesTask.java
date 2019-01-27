package com.eye2action.cameraview;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.Toast;

import com.eye2action.util.Executor;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

import java.io.File;

public class UploadImagesTask extends AsyncTask<File, Void, String> {
    private Exception exception;
    private final static String SERVER_URL = "http://10.78.185.184:8090/api/images_to_eye_letters/";

    private final Executor executor;
    private final Context context;

    public UploadImagesTask(Context context, Executor executor) {
        this.context = context;
        this.executor = executor;
    }

    protected String doInBackground(File... params) {

        try {
            HttpClient client = new DefaultHttpClient();
            HttpPost post = new HttpPost(SERVER_URL);

            MultipartEntityBuilder entityBuilder = MultipartEntityBuilder.create();

            for (File file : params) {
                if (file != null) {
                    entityBuilder.addBinaryBody("file", file, ContentType.DEFAULT_BINARY, file.getName());
                }
            }


            HttpEntity entity = entityBuilder.build();
            post.setEntity(entity);
            HttpResponse response = client.execute(post);
            HttpEntity httpEntity = response.getEntity();
            String sresult = EntityUtils.toString(httpEntity);
            return sresult;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    protected void onPostExecute(String result) {
        try {
            boolean success = executor.execute(result);
            if (!success) {
                Toast.makeText(context, "Invalid command!", Toast.LENGTH_LONG).show();
            }
        } catch (Exception exception) {
            exception.printStackTrace();
            Toast.makeText(context, "An error has occurred!", Toast.LENGTH_LONG).show();
        }
    }
}
