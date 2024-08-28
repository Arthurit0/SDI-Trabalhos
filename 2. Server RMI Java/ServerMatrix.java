
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.Random;

/*
 * O servidor deve oferecer:
 * - Operações com matriz (implementando a interface IMatrix);
  */

public class ServerMatrix implements IMatrix{
  public ServerMatrix() throws RemoteException {
    super();
  }
    
  @Override
  public double[][] sum(double[][] a, double[][] b) throws RemoteException{
    if (a.length != b.length || a[0].length != b[0]. length){
      throw new IllegalArgumentException("Matrizes precisam ser de mesma dimensões!!");
    }

    int linhas = a.length;
    int colunas = a[0].length;
    double[][] result = new double[linhas][colunas];

    for (int i = 0; i < linhas; i++) {
      for (int j = 0; j < colunas; j++) {
        result[i][j] = a[i][j] + b[i][j];
      }
    }

    return result;
  }

  @Override
  public double[][] mult(double[][] a, double[][] b) throws RemoteException{
    int colunaA = a.length;
    int colunaB = b.length;
    int linhaA = a[0].length;
    int linhaB = b[0].length;
    double result[][]= new double[colunaA][linhaB];

    if (colunaA != colunaB) {
        throw new IllegalArgumentException("O numero de colunas de A e B tem que ser iguais!!!");
    }

    for (int i = 0; i < colunaA; i++) {
      for (int j = 0; j < linhaB; j++) {
        result[i][j] = 0;
        for (int k = 0; k < linhaA; k++) {
            result[i][j] += a[i][k] * b[i][k];
        }
      }
    }

    return result;
  }

  @Override
  public double[][] randfill(int rows, int cols) throws RemoteException{
    double[][] matrix = new double[rows][cols];
    Random random = new Random();

    for (int i = 0; i < rows; i++) {
      for (int j = 0; j < cols ; j++) {
          matrix[i][j] = random.nextDouble();
      }
    }

    return matrix;
  }

  public static void main(String[] args) throws Exception{

    try 
    {
      ServerMatrix server = new ServerMatrix();
      IMatrix stub = (IMatrix)UnicastRemoteObject.exportObject(server, 0);
      Registry reg = LocateRegistry.createRegistry(12344);
      reg.bind("matrix-server", stub);
      System.out.println("Server funcionando...");
    } 
    catch (Exception e) 
    {
      e.printStackTrace();
    }
  }

}
