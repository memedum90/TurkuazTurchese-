
public class Result {
	
	public String name;
	int inDegree;
	int inDegreeF;
	int inDegreeN;
	int outDegree;
	int outDegreeF;
	int outDegreeN;
	int centrality;
	int betweenness;
	
	
	
	Result(String name){
		this.name = name;
	}
	
	int getInDegree(){
		return this.inDegree;
	}
	
	void setInDegree(int degree){
		this.inDegree = degree;
	}

}
