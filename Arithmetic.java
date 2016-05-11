import java.util.*;

public class Arithmetic
{

    public static int add(int i, int j) { return i + j; }
    public static float add(float i, float j) {return i + j; }
    public static float add(float i, int j) {return i + j; }
    public static float add(int i, float j) {return i + j; }

    public static int mult(int i, int j) {return i * j; }
    public static float mult(float i, float j) {return i * j; }
    public static float mult(float i, int j) {return i * j; }
    public static float mult(int i, float j) {return i * j; }

    public static int subract(int i, int j) {return i - j; }
    public static float subract(float i, float j) {return i - j; }
    public static float subract(float i, int j) {return i - j; }
    public static float subract(int i, float j) {return i - j; }

    public static int div(int i, int j) {return i / j; }
    public static float div(float i, float j) {return i / j; }
    public static float div(float i, int j) {return i / j; }
    public static float div(int i, float j) {return i / j; }

    public static void squares(String str) {

        ArrayList<String> items = new ArrayList<>();
        String temp = "";
        int index = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) != ',') {
                temp += str.charAt(i);
            }

            else {
                items.add(index, temp);
                index++;
                temp = "";
            }
        }

        items.stream()
                .forEach (e -> System.out.println(squareNum(e)));

    }

    public static String squareNum(String num) {
        float temp = Float.parseFloat(num);
        temp *= temp;
        return Float.toString(temp);
    }
}