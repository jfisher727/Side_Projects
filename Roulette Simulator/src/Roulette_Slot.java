
public class Roulette_Slot {
	
	String color;
	int value;
	
	public Roulette_Slot () {
		//default constructor
		this.color = null;
		this.value = -1;
	}
	
	public Roulette_Slot (String color, int value) {
		this.color = color;
		this.value = value;
	}
	
	public String toString () {
		if (value == 37) {
			return color + " 00";
		}
		return color + " " + value;
	}

}
