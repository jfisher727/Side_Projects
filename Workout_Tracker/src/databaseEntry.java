import java.util.Date;


public class databaseEntry {
	private Date date;
	private int volume;
	private int max;
	private int sets;
	private int reps;
	
	public databaseEntry (Date date, int volume, int max, int sets, int reps) {
		this.date = date;
		this.volume = volume;
		this.max = max;
		this.sets = sets;
		this.reps = reps;
	}
	
	public Date getDate () {
		return this.date;
	}
	
	public String dateToString () {
		return this.date.toString();
	}
	
	public int getVolume () {
		return this.volume;
	}
	
	public int getMax () {
		return this.max;
	}
	
	public int getSets () {
		return this.sets;
	}
	
	public int getReps () {
		return this.reps;
	}

}
