import java.io.*;
import java.util.LinkedList;
import java.util.Random;

public class Twist {

    public static void main(String[] args) throws FileNotFoundException, IOException {
        //Einlesen des Textes durch BufferedReader
        String filename = "twist1.txt";
        String currentDirectory;
        File file = new File(filename);
        currentDirectory = file.getAbsolutePath();
        final BufferedReader in = new BufferedReader(new FileReader(currentDirectory));

        //Neue Text Datei mit getwisteten Text
        BufferedWriter writer = new BufferedWriter(new FileWriter("twisted_"+filename));

        int s;
        String word = "";
        String twistedWord;
        while ((s = in.read()) != -1) {
            char l = (char) (s);
            if (Character.isLetter(l)) {
                word = word + l;
            } else {
                //System.out.print(word);
                //bei einem Wort mit weniger als 4 Zeichen muss nicht getwistet werden
                if (word.length() > 3) {
                    char[] wordArray = word.toCharArray();
                    twistedWord = twistWord(wordArray);
                } else {
                    twistedWord = word;
                }
                System.out.print(twistedWord);
                System.out.print(l);
                writer.write(twistedWord+l);
                word = "";
            }

        }
        writer.close();

    }

    //twistet ein einzelnes Wort
    static String twistWord(char[] wordArray) {
        char[] wordArrayTwist = new char[wordArray.length]; //wordArrayTwist enthält das getwistete Wort
        wordArrayTwist[0] = wordArray[0]; //erster Buchstabe bleibt gleich
        wordArrayTwist[wordArray.length - 1] = wordArray[wordArray.length - 1];
        LinkedList<Integer> positions = new LinkedList(); //Liste der noch nicht besetzen Positionen
        for (int j = 1; j < wordArray.length - 1; j++) {
            positions.add(j);
        }
        int pos;
        //allen Buchstaben von der 2. bis zur vorletzen Position wird eine neue zufällige Position zugeordente
        for (int i = 1; i < wordArray.length - 1; i++) {
            pos = randomPosition(positions);
            wordArrayTwist[pos] = wordArray[i];
        }
        String twistedWord = new String(wordArrayTwist);
        return twistedWord;
    }

    //generiert eine zufällige neue Position und entfernt diese aus der Liste der noch freien neuen Positionen
    static int randomPosition(LinkedList<Integer> positions) {
        Random rand = new Random();
        int index = rand.nextInt(positions.size());
        int newPos = positions.get(index);
        positions.remove(index);
        return newPos;
    }

}

