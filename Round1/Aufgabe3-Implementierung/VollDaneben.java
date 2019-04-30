import java.io.*;
import java.util.ArrayList;
import java.util.Collections;

public class VollDaneben {

    static ArrayList<Integer>  gzahlen; //Glückszahlen der Teilnehmer
    static int[] czahlen; // 10 Zahlen

    public static void main(String[] args) throws FileNotFoundException, IOException {
        //Einlesen des Textes durch BufferedReader
        String filename = "beispiel1.txt";
        String currentDirectory;
        File file = new File(filename);
        currentDirectory = file.getAbsolutePath();
        final BufferedReader in = new BufferedReader(new FileReader(currentDirectory));
        gzahlen = new ArrayList<>();
        String line;
        while((line = in.readLine()) != null){
            gzahlen.add(Integer.parseInt(line));
        }
        if(gzahlen.size()<11){
            int bilanz = 25*gzahlen.size();
            for(int j = 0; j<gzahlen.size(); j++){
                System.out.print(gzahlen.get(j)+", ");
            }
            for(int k = gzahlen.size(); k<11; k++){
                System.out.print(0+", ");
            }
            System.out.println();
            System.out.println("Bilanz: "+bilanz);
            return;
        }

        int subset1 = 0;
        int z1 = 0;
        int subset2 = 0;
        int z2 = 0;
        int subset3 = 0;
        int z3 = 0;
        int subset4 = 0;
        int z4 = 0;
        int subset5 = 0;
        int z5 = 0;
        int subset6 = 0;
        int z6 = 0;
        int subset7 = 0;
        int z7 = 0;
        int subset8 = 0;
        int z8 = 0;
        int subset9 = 0;
        int z9 = 0;
        int subset10 = 0;
        int z10 = 0;
        Collections.sort(gzahlen);
        int abschnitt = ((gzahlen.get(gzahlen.size()-1)-gzahlen.get(0))/10);
        int i=0;
        for(int n = 1; n<=11; n++){
            while(i<gzahlen.size() && gzahlen.get(i)<(gzahlen.get(0)+n*abschnitt)){
                switch(n){
                    case 1:
                        subset1 = subset1 + gzahlen.get(i);
                        z1++;
                        break;
                    case 2:
                        subset2 = subset2 + gzahlen.get(i);
                        z2++;
                        break;
                    case 3:
                        subset3 = subset3 + gzahlen.get(i);
                        z3++;
                        break;
                    case 4:
                        subset4 = subset4 + gzahlen.get(i);
                        z4++;
                        break;
                    case 5:
                        subset5 = subset5 + gzahlen.get(i);
                        z5++;
                        break;
                    case 6:
                        subset6 = subset6 + gzahlen.get(i);
                        z6++;
                        break;
                    case 7:
                        subset7 = subset7 + gzahlen.get(i);
                        z7++;
                        break;
                    case 8:
                        subset8 = subset8 + gzahlen.get(i);
                        z8++;
                        break;
                    case 9:
                        subset9 = subset9 + gzahlen.get(i);
                        z9++;
                        break;
                    case 10:
                        subset10 = subset10 + gzahlen.get(i);
                        z10++;
                        break;
                }
                i++;
            }
        }
        czahlen = new int[10];
        if(z1 != 0) {
            czahlen[0] = subset1 / z1;
        }else{
            czahlen[0] = gzahlen.get(0)+ abschnitt;
        }
        if(z2 != 0) {
            czahlen[1] = subset2/z2;
        }else{
            czahlen[1] = gzahlen.get(0)+ 2*abschnitt;
        }
        if(z3 != 0) {
            czahlen[2] = subset3/z3;
        }else{
            czahlen[2] = gzahlen.get(0)+ 3*abschnitt;
        }
        if(z4 != 0) {
            czahlen[3] = subset4/z4;
        }else{
            czahlen[3] = gzahlen.get(0)+ 4*abschnitt;
        }
        if(z5 != 0) {
            czahlen[4] = subset5/z5;
        }else{
            czahlen[4] = gzahlen.get(0)+ 5*abschnitt;
        }
        if(z6 != 0) {
            czahlen[5] = subset6/z6;
        }else{
            czahlen[5] = gzahlen.get(0)+ 6*abschnitt;
        }
        if(z7 != 0) {
            czahlen[6] = subset7/z7;
        }else{
            czahlen[6] = gzahlen.get(0)+ 7*abschnitt;
        }
        if(z8 != 0) {
            czahlen[7] = subset8/z8;
        }else{
            czahlen[7] = gzahlen.get(0)+ 8*abschnitt;
        }
        if(z9 != 0) {
            czahlen[8] = subset9/z9;
        }else{
            czahlen[8] = gzahlen.get(0)+ 9*abschnitt;
        }
        if(z10 != 0) {
            czahlen[9] = subset10/z10;
        }else{
            czahlen[9] = gzahlen.get(0)+ 10*abschnitt;
        }
        for(int j = 0; j<10; j++){
            System.out.print(czahlen[j]+", ");
        }
        System.out.println();
        int verlust = computeMinDistances();
        int gewinn = 25*gzahlen.size();
        int bilanz = gewinn-verlust;
        System.out.println("Bilanz: "+bilanz);
    }

    //Berechnet den Betrag den Al auszahlen muss
    static int computeMinDistances(){
        int distances = 0;
        for(int i = 0; i<gzahlen.size(); i++){
            distances = distances + getDistance(gzahlen.get(i));
        }
        return distances;
    }

    //findet den Abstand zu der nähsten von Als Zahlen
    static int getDistance(int gzahl){
        int min = 1000;
        for(int i = 0; i<10; i++){
            int d = Math.abs(czahlen[i]-gzahl);
            if(d<min){
                min = d;
            }
        }
        return min;

    }
}
