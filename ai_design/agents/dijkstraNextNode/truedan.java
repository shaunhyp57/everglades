import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.io.*;

/*
  This class was developed by modifying an existing java class
  provided as part of UCF's COP4516 class to teach implementation
  of Dijkstra's algorithm. It was modified to print the next node
  to move to from each node to the target node. 

  Input is of the form
  
  c
  n e
  to from weight - e1
  to from weight - e2
  ...
  
  c: number of graphs to analyze
  n: number of nodes in graph
  e: number of directed edges in graph
  followed by each edge in the form of
          to from weight
  
  For example input, refer to everBoard.txt
*/

public class truedan {

  // Store graph here
  static ArrayList<Edge>[] g;
  static int n;

  public static void main(String[] args) throws Exception{

    Scanner in = new Scanner(System.in);
    int cases = in.nextInt();

    // Process each case.
    for (int co = 1; co <= cases; co++) {

      // Read the graph.
      n = in.nextInt();
      int m = in.nextInt();
      g = new ArrayList[n];
      for (int i = 0; i < n; i++)
        g[i] = new ArrayList<Edge>();

      // Form the edges.
      for (int i = 0; i < m; i++) {
        int a = in.nextInt() - 1;
        int b = in.nextInt() - 1;
        int w = in.nextInt();
        g[a].add(new Edge(b, w, 0));
        g[b].add(new Edge(a, w, 0));
      }
      
        for(int startNode = 0; startNode < n; startNode++)
        {
            // Run Dijkstra's
            int[] dist = dijkstras(startNode);
            int val = 0;

            for(int di: dist)
            {
                if(val == startNode)
                    System.out.print("-1, ");
                else
                    System.out.print((di  + 1) + ", ");
                
                val++;
            }
            System.out.println();
        }
    }

    in.close();
  }

  static int[] dijkstras(int s) {

  	// Set up Dijkstra's
    boolean[] v = new boolean[n];
    int[] d = new int[n];
    int[] past = new int[n];
    PriorityQueue<Edge> pq = new PriorityQueue<Edge>();
    pq.add(new Edge(s, 0, 0));

    // Run until nothing in the queue.
    while (!pq.isEmpty()) {

      // Pull the next estimate.
      Edge at = pq.poll();

      // Got to at before...
      if (v[at.e]) continue;

      // We've reached here.
      v[at.e] = true;
      d[at.e] = at.w;
      past[at.e] = at.p;

      // Update all vertices we can reach from here.
      for (Edge adj : g[at.e])
        pq.add(new Edge(adj.e, adj.w + at.w, at.e));
    }

    // This is the answer.
    return past;
  }

  // Class so we can use a Priority Queue for Dijkstra's.
  static class Edge implements Comparable<Edge> {
    int e, w, p;

    public Edge(int e, int w, int p) {
      this.e = e;
      this.w = w;
      this.p = p;
    }

    public int compareTo(Edge o) {
        if(w != o.w)
            return w - o.w;

        return o.e - e;
    }
  }
}
