/*
 * O servidor deve oferecer:
 * - Operações com matriz (implementando a interface IMatrix);
  */

public class ServerMatrix implements IMatrix {
    public double[][] sum(double[][] a, double[][] b) {
        if (a.length != b.length || a[0].length != b[0].length) {
            return null;
        }
        double[][] c = new double[a.length][a[0].length];
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a[0].length; j++) {
                c[i][j] = a[i][j] + b[i][j];
            }
        }
        return c;
    }

    public double[][] mult(double[][] a, double[][] b) {
        if (a[0].length != b.length) {
            return null;
        }
        double[][] c = new double[a.length][b[0].length];
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < b[0].length; j++) {
                c[i][j] = 0;
                for (int k = 0; k < a[0].length; k++) {
                    c[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return c;
    }

    public double[][] randfill(int rows, int cols) {
        double[][] a = new double[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                a[i][j] = Math.random();
            }
        }
        return a;
    }
}
