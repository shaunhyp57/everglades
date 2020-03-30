import java.io.*;
import java.util.*;

public class DFS_BFS
{

	public static void main(String[] args)
	{
		new DFS_BFS(); // I like doing things this way...
	}
	
	int N; // number of vertices in the graph
	boolean[][] G; // the graph as an adjacency matrix
				   // G[i][j] is true if there is an edge from i to j
	
	DFS_BFS()
	{
		setupGraph();		
		System.out.println("------------------------------");
		System.out.println();
		
		// perform a DFS on the graph
		DFS();
		System.out.println();
		System.out.println("------------------------------");
		System.out.println();
		
		// perform a BFS on the graph
		BFS();
		System.out.println();
		System.out.println("------------------------------");
		System.out.println();
		System.out.println("All done - have a good day!");
	}
	
	// initial setup of the graph
	void setupGraph()
	{
		// set up a graph with 8 vertices + 3 components that looks like:
		/*
			0 --- 1        5---6
			| \    \       |  / 
			|  \    \      | /
			2   3----4     7
		*/
		N=11;
		G=new boolean[N][N];
		// notice that for each edge G[i][j] == G[j][i]
		// this means that the graph is undirected
		G[0][1]=G[1][0]=true; G[0][3]=G[3][0]=true; G[1][2]=G[2][1]=true;
		G[2][3]=G[3][2]=true; G[1][4]=G[4][1]=true; G[3][6]=G[6][3]=true;
        G[5][2]=G[2][5]=true; G[6][8]=G[8][6]=true; G[2][4]=G[4][2]=true;
        G[6][2]=G[2][6]=true; G[6][9]=G[9][6]=true; G[7][4]=G[4][7]=true;
        G[5][8]=G[8][5]=true; G[7][8]=G[8][7]=true; G[8][4]=G[4][8]=true;
        G[7][10]=G[10][7]=true; G[9][10]=G[10][9]=true; G[2][4]=G[4][2]=true;
        
	}
	
	// perform a DFS on the graph G
	void DFS()
	{
		
		// do the DFS from each node not already visited
		for (int i=0; i<N; ++i){
			for(int j = 0; j < N; j++){
                boolean[] V=new boolean[N];
			    System.out.printf("DFS for component %d starting at node %d%n",numComponets,i);
                DFS(i, V, j);
            }
        }
    }
	
	// perform a DFS starting at node at (works recursively)
	void DFS(int at, boolean[] V, int tar)
	{
		System.out.printf("At node %d in the DFS%n",at);
		
		// mark that we are visiting this node
		V[at]=true;
		
		// recursively visit every node connected yet to be visited
		for (int i=0; i<N; ++i)
			if (G[at][i] && !V[i])
			{
				System.out.printf("Going to node %d...",i);
				DFS(i,V);
			}
		System.out.printf("Done processing node %d%n", at);
	}
	
	// perform a BFS on the graph G 
	void BFS()
	{
		// a visited array to mark which vertices have been visited in BFS
		boolean[] V=new boolean[N]; 
		
		int numComponets=0; // the number of components in the graph
		
		// do the BFS from each node not already visited
		for (int i=0; i<N; ++i)
			if (!V[i])
			{
				++numComponets;
				System.out.printf("BFS for component %d starting at node %d%n",numComponets,i);
				
				BFS(i,V);
			}
		System.out.println();
		System.out.printf("Finished BFS - found %d components.%n", numComponets);
	}
	
	// perform a BFS starting at node start
	void BFS(int start, boolean[] V)
	{
		Queue<Integer> Q=new LinkedList<Integer>(); // A queue to process nodes
		
		// start with only the start node in the queue and mark it as visited
		Q.offer(start);
		V[start]=true;
				
		// continue searching the graph while still nodes in the queue
		while (!Q.isEmpty())
		{
			int at=Q.poll(); // get the head of the queue
			System.out.printf("At node %d in the BFS%n",at);
			
			// add any unseen nodes to the queue to process, then mark them as  
			// visited so they don't get re-added
			for (int i=0; i<N; ++i)
				if (G[at][i] && !V[i])
				{
					Q.offer(i);
					V[i]=true;
					System.out.printf("Adding node %d to the queue in the BFS%n", i);
				}
			System.out.printf("Done processing node %d%n", at);
		}
		System.out.printf("Finished with the BFS from start node %d%n", start);
	}
}