import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;

public class UnTwist {

    static HashMap<String, ArrayList<String>> wortliste;

    public static void main(String[] args) throws FileNotFoundException, IOException {
        buildWordMap();

        //Einlesen des Textes durch BufferedReader
        String filename = "enttwist.txt";
        String currentDirectory;
        File file = new File(filename);
        currentDirectory = file.getAbsolutePath();
        final BufferedReader in = new BufferedReader(new FileReader(currentDirectory));

        //Neue Text Datei mit entwisteten Text
        BufferedWriter writer = new BufferedWriter(new FileWriter("enttwist_" + filename));

        int s;
        String word = "";
        String enttwist;
        while ((s = in.read()) != -1) {
            char l = (char) (s);
            if (Character.isLetter(l)) {
                word = word + l;
            } else {
                if (word.length() > 3) {
                    enttwist = untwistWord(word);
                } else {
                    enttwist = word;
                }

                //Kontrolle Großschreibung
                if (!word.equals("")) {
                    String uWord = word.substring(0, 1).toUpperCase() + word.substring(1, word.length());
                    if (word.equals(uWord)) {
                        enttwist = enttwist.substring(0, 1).toUpperCase() + enttwist.substring(1, enttwist.length());
                    }
                }
                System.out.print(enttwist + l);
                writer.write(enttwist + l);
                word = "";
            }

        }
        writer.close();

    }

    //enttwistet ein einzelnes Wort
    static String untwistWord(String word) {
        String enttwist = word + "(n)";
        String k = computeKey(word);
        if (wortliste.containsKey(k)) {
            ArrayList<String> possible = wortliste.get(k);
            if (possible.size() == 1) {
                enttwist = possible.get(0);
            } else {
                int hword = computeWordHash(word);
                for (int j = 0; j < possible.size(); j++) {
                    if (hword == (computeWordHash(possible.get(j)))) {
                        if (compareLetters(possible.get(j), word))
                            enttwist = possible.get(j);
                    }

                }

            }
        } else {
            enttwist = word + "(n)";
        }
        return enttwist;
    }

    //enthält Wort w1 alle Buchstaben aus w2?
    static boolean compareLetters(String w1, String w2) {
        w1 = w1.substring(1, w1.length() - 1);
        w2 = w2.substring(1, w2.length() - 1);
        for (int i = 0; i < w1.length(); i++) {
            char c = w1.charAt(i);
            boolean in = false;
            for (int j = 0; j < w2.length(); j++) {
                if (w2.charAt(j) == c) {
                    in = true;
                }
            }
            if (in == false) {
                return false;
            }
        }
        return true;
    }

    //Schlüssel der Form [erster Buchstabe][letzter Buchstabe][Länge]
    static String computeKey(String word) {
        word = word.toLowerCase();
        String fl = Character.toString(word.charAt(0));
        String ll = Character.toString(word.charAt(word.length() - 1));
        int length = word.length();
        return (fl + ll + length);

    }

    //Summe der Unicodewerte
    static int computeWordHash(String w) {
        int h = 0;
        for (int i = 1; i < w.length() - 1; i++) {
            int n = Character.getNumericValue(w.charAt(i));
            h = h + n;
        }
        return h;
    }


    //erstellt Hashmap zur Darstellung der Daten aus der Wörterliste
    static void buildWordMap() throws IOException {
        wortliste = new HashMap<>();
        String filename = "woerterliste.txt";
        String currentDirectory;
        File file = new File(filename);
        currentDirectory = file.getAbsolutePath();
        final BufferedReader in = new BufferedReader(new FileReader(currentDirectory));
        String line;
        while ((line = in.readLine()) != null) {
            String k = computeKey(line);
            if (wortliste.containsKey(k)) {
                wortliste.get(k).add(line);
            } else {
                ArrayList<String> w = new ArrayList<>();
                wortliste.put(k, w);
            }
        }

    }


}
