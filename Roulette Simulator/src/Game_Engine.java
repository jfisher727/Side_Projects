import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;


public class Game_Engine {
	private static final String board_description = "Slot_descriptions.txt";
	private static final int SIMULATED_SPINS = 1000;
	
	private static ArrayList <Roulette_Slot> roulette_wheel;
	private static ArrayList <Roulette_Slot> winning_spins;
	
	
	public static void load_board () {
		roulette_wheel = new ArrayList <Roulette_Slot> ();
		try {
			Scanner board_reader = new Scanner (new File (board_description));
			while(board_reader.hasNextLine()) {
				String entire_line = board_reader.nextLine();
				String [] arguments = entire_line.split(" ", 2);
				roulette_wheel.add(new Roulette_Slot(arguments[1], Integer.valueOf(arguments[0])));
			}
			board_reader.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void simulate () {
		winning_spins = new ArrayList <Roulette_Slot> ();
		for (int i = 0; i < SIMULATED_SPINS; i++) {
			int random_slot = (int) ((((int)(Math.random() * 100)) /** System.currentTimeMillis()*/) % roulette_wheel.size());
			//System.out.println ("Slot: " + random_slot);
			//System.out.println (roulette_wheel.get(random_slot).toString());
			winning_spins.add(roulette_wheel.get(random_slot));
			/*
			try {
				Thread.sleep(10);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			*/
		}
	}
	
	public static void main (String [] args) {
		load_board ();
		simulate();
		Generate_Statistics stats = new Generate_Statistics (winning_spins);
		stats.generate_stats();
	}
}
