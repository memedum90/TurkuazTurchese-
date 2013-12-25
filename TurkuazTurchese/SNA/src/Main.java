import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.util.*;

import fr.inria.acacia.corese.api.IDatatype;
import fr.inria.edelweiss.kgram.core.Mapping;
import fr.inria.edelweiss.kgram.core.Mappings;
import fr.inria.edelweiss.kgraph.core.Graph;
import fr.inria.edelweiss.kgraph.query.QueryProcess;
import fr.inria.edelweiss.kgtool.load.Load;
import fr.inria.edelweiss.kgtool.print.ResultFormat;

/**
 * @author stradivarius
 *
 */
public class Main {
	
	/**
	 * QUERIES
	 */
	/* General query to retrieve all the agents */
//	static String generalQuery = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
//		+ " SELECT ?x ?y WHERE {?x foaf:knows ?y}";
	static String generalQuery = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x ?f ?y WHERE {?x tto:hasRelationship ?r ."
		+ " ?r ns1:flame ?f ."
		+ " ?r tto:hasCorrespondant ?y"
		+ " }";
	
	/* This query calculates the inDegree of a node x. The number denotes the depth of the path search.
	 *  A node with a high inDegree is considered to be an authority, so a node with high power and consideration.
	 *  it uses the foaf:knows relation */
	static String inDegree = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
		+ " SELECT ?x (count(?y) as ?degree) WHERE{"
		+ " {?y $path ?x"
		+ "	filter(match($path, foaf:knows))"
		+ "	filter(pathLength($path) <= 10) }"
		+ "	} GROUP BY ?x";
	
	/* This query calculates the weighted inDegree of a node x. The depth of the path search is 1.
	 *  A node with a high inDegree is considered to be an authority, so a node with high power and consideration.
	 *  respectively, its variants N and F calculates only with non flames and flames respectively */
	static String inDegree1 = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x (sum(?w) as ?degree) WHERE{"
		+ " { ?y tto:hasCorrespondant ?x ."
		+ " ?y tto:value ?w }"
		+ "	} GROUP BY ?x";
	static String inDegree1F = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x (sum(?w) as ?degree) WHERE{"
		+ " { ?y tto:hasCorrespondant ?x ."
		+ " ?y ns1:flame \"flame\" ."
		+ " ?y tto:value ?w }"
		+ "	} GROUP BY ?x";
	static String inDegree1N = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x (sum(?w) as ?degree) WHERE{"
		+ " { ?y tto:hasCorrespondant ?x ."
		+ " ?y ns1:flame \"noflame\" ."
		+ " ?y tto:value ?w }"
		+ "	} GROUP BY ?x";
	
	/* This query calculates the outDegree of a node x. The number denotes the depth of the path search.
	 * A node with a high outDegree is considered to be a hub, so a node that is a good information diffuser. */
	static String outDegree = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
		+ " SELECT ?x (count(?y) as ?degree) WHERE{"
		+ " {?x $path ?y"
		+ "	filter(match($path, foaf:knows))"
		+ "	filter(pathLength($path) <= 10) }"
		+ "	} GROUP BY ?x";
	
	/* This query calculates the weighted outDegree of a node x. The depth of the path search is 1.
	 *  A node with a high outDegree is considered to be a hub, so a node that is a good information diffuser.
	 *  respectively, its variants N and F calculates only with non flames and flames respectively */
	static String outDegree1 = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x (sum(?w) as ?degree) WHERE{"
		+ " { ?x tto:hasRelationship ?y ."
		+ " ?y tto:hasCorrespondant ?s ."
		+ " ?y tto:value ?w }"
		+ "	} GROUP BY ?x";
	static String outDegree1F = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x (sum(?w) as ?degree) WHERE{"
		+ " { ?x tto:hasRelationship ?y ."
		+ " ?y tto:hasCorrespondant ?s ."
		+ " ?y ns1:flame \"flame\" ."
		+ " ?y tto:value ?w }"
		+ "	} GROUP BY ?x";
	static String outDegree1N = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ " SELECT ?x (sum(?w) as ?degree) WHERE{"
		+ " { ?x tto:hasRelationship ?y ."
		+ " ?y tto:hasCorrespondant ?s ."
		+ " ?y ns1:flame \"noflame\" ."
		+ " ?y tto:value ?w }"
		+ "	} GROUP BY ?x";
	
	/* The closeness centrality of a resource represents its capacity to join (and to be reached by) any resource in a network.
	 * The closeness centrality of a node is the inverse sum of its shortest distances to each other resource. */
	static String closeCentral = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
		+ "	SELECT ?x ?to (pathLength($path) as ?length) (sum(?length) as ?centrality) WHERE {"
		+ "	{?x $path ?to"
		+ " filter(match($path, foaf:knows, 's'))}"
		+ " } GROUP BY ?x";
	
	/* The betweenness centrality focuses on the capacity of a node to be an intermediary between any two other nodes.
	 * It is defined as the ratio between the total number of shortest paths and the number of shortest paths passing though that node */
	static String betweennessDen = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
		+ " SELECT ?from ?to (count($path) as ?nbPaths) WHERE{"
		+ " ?from $path ?to"
		+ "	filter(match($path, foaf:knows, 'sa'))"
		+ "	} GROUP BY ?from ?to";
	static String betweennessNum = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
		+ " SELECT ?from ?to ?b (count($path) as ?nbPaths) WHERE{"
		+ "	?from $path ?to"
		+ " GRAPH $path{?b foaf:knows ?j}"
		+ " filter(match($path, foaf:knows, 'sa'))"
		+ "	filter(?from != ?b)"
		+ " OPTIONAL { ?from (foaf:knows)::?p ?to }"
		+ "	filter(!bound(?p))"
		+ " } group by ?from ?to ?b";


	/* We use a simplified version of the betweenness and we check only how many conversations flames the user is involved in. */
	static String smplBtwn = "PREFIX tto: <http://www.fedemontori.eu/ns#>"
		+ " PREFIX ns1: <http://www.fedemontori.eu/>"
		+ "	SELECT ?x (count(?to) as ?btw) WHERE {"
		+ "	{?x tto:hasRelationship ?to }"
		+ " }";
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {

		Graph graph = Graph.create();
		
		Load ld = Load.create(graph);
		ld.load("social_graph.rdf");
		
		QueryProcess exec = QueryProcess.create(graph);
		

		
		try{
			//System.out.println(ResultFormat.create(exec.query(betweennessNum)));
			// Query for getting the general informations
			Mappings map = exec.query(generalQuery);
			Map<String, List<String>> MapfGeneral = new HashMap<>();
			for (Mapping m : map){
				List<String> empty;
				if (!MapfGeneral.containsKey(((IDatatype) m.getValue("?x")).toString())){
					empty = new ArrayList<String>();
				} else {
					empty = MapfGeneral.get(((IDatatype) m.getValue("?x")).toString());
					MapfGeneral.remove(((IDatatype) m.getValue("?x")).toString());
				}
				empty.add(((IDatatype) m.getValue("?y")).toString());
				MapfGeneral.put(((IDatatype) m.getValue("?x")).toString(), empty);
			}
			// Query for General indegree with depth 10
			map = exec.query(inDegree);
			Map<String, String> MapfinD10 = new HashMap<>();
			for (Mapping m : map){
				MapfinD10.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?degree")).toString());
			}
			// Query for Flame indegree with depth 1
			map = exec.query(inDegree1F);
			Map<String, String> MapfinDF1 = new HashMap<>();
			for (Mapping m : map){
				MapfinDF1.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?degree")).toString());
			}
			// Query for Nonflame indegree with depth 1
			map = exec.query(inDegree1N);
			Map<String, String> MapfinDN1 = new HashMap<>();
			for (Mapping m : map){
				MapfinDN1.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?degree")).toString());
			}
			// Query for General outdegree with depth 10
			map = exec.query(outDegree);
			Map<String, String> MapfoutD10 = new HashMap<>();
			for (Mapping m : map){
				MapfoutD10.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?degree")).toString());
			}
			// Query for Flame outdegree with depth 1
			map = exec.query(outDegree1F);
			Map<String, String> MapfoutDF1 = new HashMap<>();
			for (Mapping m : map){
				MapfoutDF1.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?degree")).toString());
			}
			// Query for Nonflame outdegree with depth 1
			map = exec.query(outDegree1N);
			Map<String, String> MapfoutDN1 = new HashMap<>();
			for (Mapping m : map){
				MapfoutDN1.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?degree")).toString());
			}
			// Query for Closeness Centrality
			map = exec.query(closeCentral);
			Map<String, String> MapfClsCnt = new HashMap<>();
			for (Mapping m : map){
				MapfClsCnt.put(((IDatatype) m.getValue("?x")).toString(), ((IDatatype) m.getValue("?centrality")).toString());
			}
			// Query for Global Betweenness
			map = exec.query(betweennessDen);
			Mappings mapN = exec.query(betweennessNum);
			Map<String[], String> MapfBtwnD = new HashMap<>();
			Map<String[], String> MapfBtwnN = new HashMap<>();
			Map<String, String> MapfBtwn = new HashMap<>();
			for (Mapping m : map){
				String couple[] = new String[2];
				couple[0] = ((IDatatype) m.getValue("?from")).toString();
				couple[1] = ((IDatatype) m.getValue("?to")).toString();
				MapfBtwnD.put(couple, ((IDatatype) m.getValue("?nbPaths")).toString());		
			}
			for (Mapping m : mapN){
				String triplet[] = new String[3];
				
				if (m.getValue("?b") != null){
					triplet[0] = ((IDatatype) m.getValue("?from")).toString();
					triplet[1] = ((IDatatype) m.getValue("?to")).toString();
					triplet[2] = ((IDatatype) m.getValue("?b")).toString();
					MapfBtwnN.put(triplet, ((IDatatype) m.getValue("?nbPaths")).toString());
				}

			}
			for (String[] Triple : MapfBtwnN.keySet()){
				int sum = 0;
				String couple[] = new String[2];
				couple[0] = Triple[0];
				couple[1] = Triple[1];
				if (MapfBtwn.containsKey(Triple[2])){
					sum += Integer.parseInt(MapfBtwn.get(Triple[2]));
					MapfBtwn.remove(Triple[2]);					
				}
				sum += Integer.parseInt(MapfBtwnD.get(couple));
				MapfBtwn.put(Triple[2], Integer.toString(sum));
			}
			
			//Map<String, Result> FinalMap = new HashMap<>();
			for (String key : MapfGeneral.keySet()) {
				//Result temp = new Result(key);
				System.out.println("User " + key);
				System.out.println("    - has conversations with:");
				for (String guy : MapfGeneral.get(key)){
					System.out.println("        - " + guy);
				}
				System.out.println("    - inDegree with depth 10: " + MapfinD10.get(key));
				System.out.println("    - inDegree (Flaming, weighted) with depth 1: " + MapfinDF1.get(key));
				System.out.println("    - inDegree (NonFlaming, weighted) with depth 1: " + MapfinDN1.get(key));
				System.out.println("    - outDegree with depth 10: " + MapfoutD10.get(key));
				System.out.println("    - outDegree (Flaming, weighted) with depth 1: " + MapfoutDF1.get(key));
				System.out.println("    - outDegree (NonFlaming, weighted) with depth 1: " + MapfoutDN1.get(key));
				System.out.println("    - Closeness Centrality: " + MapfClsCnt.get(key));
				System.out.println("    - in-Betweenness: " + MapfBtwn.get(key));
			}

			
			
//				   dt.intValue();
//				   dt.doubleValue();
//				   dt.getLabel();
//				   dt.getDatatypeURI();
//				   dt.getLang();
//				   dt.isURI();
//				   dt.isLiteral();
//				   dt.isBlank();
//				   System.out.println(dt.getLabel());
//				}   
			
//			ResultFormat fGeneral = ResultFormat.create(exec.query(generalQuery));
//			ResultFormat finD10 = ResultFormat.create(exec.query(inDegree));
//			ResultFormat finDF1 = ResultFormat.create(exec.query(inDegree1F));
//			ResultFormat finDN1 = ResultFormat.create(exec.query(inDegree1N));
//			ResultFormat foutD10 = ResultFormat.create(exec.query(outDegree));
//			ResultFormat foutDF1 = ResultFormat.create(exec.query(outDegree1F));
//			ResultFormat foutDN1 = ResultFormat.create(exec.query(outDegree1N));
//			ResultFormat fClsCnt = ResultFormat.create(exec.query(closeCentral));
//			ResultFormat fBtwnD = ResultFormat.create(exec.query(betweennessDen));
//			ResultFormat fBtwnN = ResultFormat.create(exec.query(betweennessNum));
//			ResultFormat fSBtwn = ResultFormat.create(exec.query(smplBtwn));
//			System.out.println(finD10);

			
			
			
			
			
			
			
			
		} catch(Exception e){
			e.printStackTrace();
		}
		
		


	}

}
