
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


/*
 * O servidor deve oferecer:
 * - Operações com a base de dados (implementando IDatabase)
  */

public class ServerDatabase implements IDatabase{
  public ServerDatabase(){};

  @Override
  public void save(double[][] a, String filename) throws RemoteException{
    try(PrintWriter escrita = new PrintWriter(new File(filename));){
      for(int i = 0; i < a.length; i++) {
        for(int j = 0; j < a[i].length; j++){
          escrita.print(a[i][j] + ",");
        }
      escrita.println();
      }
    } catch (IOException e) {
      throw new RemoteException("Erro ao salvar!!!", e);
    }

  }

  @Override
  public double[][] load(String filename) throws RemoteException{
    double[][] matriz = null;

    try(FileReader leitorR = new FileReader(filename); BufferedReader leitorB = new BufferedReader(leitorR);){

      List<double[]> colunas = new ArrayList<>();
      String linha = null;
      
      while((linha = leitorB.readLine()) != null){
        String[] valor = linha.split(",");
        double[] coluna = Arrays.stream(valor).mapToDouble(Double::parseDouble).toArray();
        colunas.add(coluna);
      }
      matriz = colunas.toArray(new double[colunas.size()][]);
    } catch (IOException e) {
      throw new RemoteException("Erro ao recuperar a matriz!!!", e);
    }

    return matriz;
  }

  @Override
  public void remove(String filename) throws RemoteException{

    try {
      File file = new File(filename);

      if(file.exists()){
        file.delete();
      }
    } catch (SecurityException e) {
      throw new RemoteException("Erro ao deletar o arquivo!!!", e);
    }
  }
    
  public static void main(String[] args){
    try
    {
      ServerDatabase server = new ServerDatabase();
      IDatabase stub = (IDatabase)UnicastRemoteObject.exportObject(server, 0);
      Registry reg = LocateRegistry.createRegistry(12345);
      reg.bind("db-server", stub);
      System.out.println("banco funcionando...");
    }
    catch (Exception e)
    {
      e.printStackTrace();
    }
  }

}
