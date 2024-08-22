import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

import org.apache.commons.math3.util.Pair;

/**
 * Main
 */
public class Main {
    // Redirect the file content to the executable
    public static void main(String[] args) throws Exception {
        HashMap<Integer, HashSet<String>> fotos = new HashMap<>();
        ArrayList<Integer> verticais = new ArrayList<>();

        int count = 0;
        BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
        for (String line = stdin.readLine(); line != null; line = stdin.readLine()) {
            String[] tags = line.split(" ");

            HashSet<String> tagsToAdd = new HashSet<>();
            for (int i = 2; i < tags.length; i++)
                tagsToAdd.add(tags[i]);

            fotos.put(count, tagsToAdd);
            if (tags[0].equals("V"))
                verticais.add(count);
            count++;
        }

    }

    public static ArrayList<Pair<Integer, Integer>> name() {

    }
}
