/*
 * O cliente deve executar as operações com as matrizes e salvar os dados (recuperar e por fim excluir o arquivo)
 */

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

 public class Client {
    public static void main(String[] args) {
      String hostM = args[0];
      String hostDB = args[1];

      try {
         Registry registryMatrix = LocateRegistry.getRegistry(hostM,12344);
         Registry registryDB = LocateRegistry.getRegistry(hostDB,12345);

         IMatrix matrix_stub = (IMatrix) registryMatrix.lookup("matrix-server");
         IDatabase database_stub = (IDatabase) registryDB.lookup("db-server");
         double[][] a = matrix_stub.randfill(100, 100);
         double[][] b = matrix_stub.randfill(100, 100);
         double[][] c = matrix_stub.mult(a, b);

        database_stub.save(a, "a.txt");
        database_stub.save(b, "b.txt");
        double[][] na = database_stub.load("a.txt");
        double[][] nb = database_stub.load("b.txt");
        database_stub.remove("a.txt");
        database_stub.remove("b.txt");

      } catch (Exception ex) {
         ex.printStackTrace();
      }
   }

}