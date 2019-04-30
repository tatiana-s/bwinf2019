import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;

public class Superstar {

    static int n; //Gruppengroeße
    static HashMap<String, Integer> mitglieder; //ordnet Teilnehmern Nummern zu
    static String[] names; //Teilnehmernamen
    static int[][] matrix; //Adjazenzmatrix
    static int fragen; //Anzahl der benoetigten Fragen

    public static void main(String[] args) throws IOException {
        buildMatrix("superstar1.txt"); //hier filename veraendern
        findSuperstar();
    }

    //führt Verfahren aus
    public static void findSuperstar(){
        fragen = 0;
        int x = 0;
        int y = 0;
        while(x<n && y<n){
            if(x != y){
                if(XfollowsY(x, y)){
                    x++;
                }else{
                    y++;
                }
            }else{
                y++;
            }
        }
        if(x == n-1){
            System.out.println("Es gibt keinen Superstar in dieser Gruppe");
        }else{
            if(checkSuperstar(x)){
                System.out.println("Der Superstar ist "+names[x]);
            }else{
                System.out.println("Es gibt keinen Superstar in dieser Gruppe");
            }
        }
        System.out.println("Gefunden in "+fragen+" Fragen (maximale Anzahl waere "+(4*n-4)+")");
    }

    //Kontrolliert ob gefundener moeglicher Superstar wirklich Superstar ist
    public static boolean checkSuperstar(int x){
        boolean s = true;
        for(int i = 0; i<n; i++){
            if(i != x){
                s = XfollowsY(i, x);
            }
        }
        if(!s){
            return s;
        }else{
            for(int i = 0; i<n; i++){
                if(i != x){
                    if(XfollowsY(x, i)){
                        s = false;
                    }
                }
            }
            return s;
        }
    }

    //frägt Position G[x][y] ab und gibt die dazugehoerige Frage aus
    public static boolean XfollowsY(int x, int y){
        fragen++;
        System.out.print("Frage "+fragen+": Folgt "+names[x]+" "+names[y]+"? ");
        boolean antwort = (matrix[x][y]==1);
        if(antwort){
            System.out.println("ja");
        }else{
            System.out.println("nein");
        }
        return antwort;
    }

    //erstellt Adjazenzmatrix (und weitere Listen) aus Eingabe
    public static void buildMatrix(String fn) throws IOException {
        mitglieder = new HashMap<>();
        String filename = fn;
        String currentDirectory;
        File file = new File(filename);
        currentDirectory = file.getAbsolutePath();
        final BufferedReader in = new BufferedReader(new FileReader(currentDirectory));
        String name = "";
        String line = in.readLine();
        names = line.split(" ");
        n = names.length;
        for(int i = 0; i<names.length; i++){
            mitglieder.put(names[i], i);
        }
        String[] connection;
        matrix = new int[n][n];
        while((line = in.readLine()) != null){
            connection = line.split(" ");
            matrix[mitglieder.get(connection[0])][mitglieder.get(connection[1])] = 1;
        }
        printMatrix();

    }

    //Hilfsmethode zur Veranschaulichung der Matrix
    public static void printMatrix(){
        for(int i = 0; i<n; i++){
            for(int j = 0; j<n; j++){
                System.out.print(matrix[i][j]+" ");
            }
            System.out.println();
        }
    }
}
