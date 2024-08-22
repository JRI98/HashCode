import java.util.HashSet;

/**
 * Interest
 */
public class Interest {
    public static HashSet<String> union(HashSet<String> tags1, HashSet<String> tags2) {
        HashSet<String> tags = new HashSet<>(tags1);
        tags.addAll(tags2);
        return tags;
    }

    public static int numCommon(HashSet<String> tags1, HashSet<String> tags2) {
        int res = 0;
        for (String s : tags1) {
            if (tags2.contains(s))
                res++;
        }
        return res;
    }

    public static int interest(HashSet<String> tags1, HashSet<String> tags2) {
        int commonTags = numCommon(tags1, tags2);
        return Math.min(tags2.size() - commonTags, Math.min(commonTags, tags1.size() - commonTags));
    }
}
