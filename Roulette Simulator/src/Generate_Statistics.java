import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Scanner;


public class Generate_Statistics {
	private static final String stat_storage = "statistics.txt";
	private ArrayList <Roulette_Slot> winning_spins;
	private int spins = 0;
	private int green_spins = 0;
	private int red_spins = 0;
	private int black_spins = 0;
	private int zero_spins = 0;
	private int double_zero = 0;
	private int first_twelve = 0;
	private int second_twelve = 0;
	private int third_twelve = 0;
	private int even_spins = 0;
	private int odd_spins = 0;
	private int one_to_eighteen = 0;
	private int nineteen_to_thirtysix = 0;
	private int first_column = 0;
	private int second_column = 0;
	private int third_column = 0;
	private double [] times_won = new double [38];
	private double [] win_percents = new double [52];
	
	public Generate_Statistics (ArrayList<Roulette_Slot> winning_spins) {
		this.winning_spins = winning_spins;
	}
	
	private void capture_color (String color) {
		if (color.equalsIgnoreCase("black")) {
			this.black_spins++;
		}
		else if (color.equalsIgnoreCase("red")) {
			this.red_spins++;
		}
		else {
			this.green_spins++;
		}
	}
	
	private void capture_value (int value) {
		times_won [value] += 1;
		if (value == 0) {
			this.zero_spins++;
		}
		else if (value == 37) {
			this.double_zero++;
		}
		else {
			//check for even odd
			if (value % 2 == 0) {
				this.even_spins++;
			}
			else {
				this.odd_spins++;
			}
			
			//check for groups of 12
			if (value >= 1 && value <= 12) {
				this.first_twelve++;
			}
			else if (value >= 13 && value <= 24) {
				this.second_twelve++;
			}
			else {
				this.third_twelve++;
			}
			
			//check for groups of 18
			if (value >= 1 && value <= 18) {
				this.one_to_eighteen++;
			}
			else {
				this.nineteen_to_thirtysix++;
			}
			
			//check for columns
			if (value % 3 == 1) {
				this.first_column++;
			}
			else if (value % 3 == 2) {
				this.second_column++;
			}
			else {
				this.third_column++;
			}
		}
	}

	private static double round(double value, int places) {
	    if (places < 0) throw new IllegalArgumentException();

	    BigDecimal bd = new BigDecimal(value);
	    bd = bd.setScale(places, RoundingMode.HALF_UP);
	    return bd.doubleValue();
	}
	
	private void print_board (FileWriter writer) {
		try {
			writer.write("         -------------------------------------------------------------------------------------------------------------\n\r");
			writer.write(" --------|        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|   0    |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("| (" + win_percents[14]  + ")  |--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|--------|        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|   00   |--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|\n\r");
			writer.write("| (" + win_percents[51]  + ")  |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("|        |        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write(" --------|        |        |        |        |        |        |        |        |        |        |        |        |\n\r");
			writer.write("         -------------------------------------------------------------------------------------------------------------\n\r");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private void write_to_file () {
		try {
			FileWriter stats_writer = new FileWriter (new File(stat_storage));
			stats_writer.write ("Total spins: " + this.spins);
			stats_writer.write ("Black spins: " + this.black_spins + ", percent: " + win_percents[0] + "%\n\r");
			stats_writer.write ("Red spins: " + this.red_spins + ", percent: " + win_percents[1] + "%\n\r");
			stats_writer.write ("Even spins: " + this.even_spins + ", percent: " + win_percents[2] + "%\n\r");
			stats_writer.write ("Odd spins: " + this.odd_spins + ", percent: " + win_percents[3] + "%\n\r");
			stats_writer.write ("Zero spins: " + this.zero_spins + ", percent: " + win_percents[4] + "%\n\r");
			stats_writer.write ("Double Zero spins: " + this.double_zero + ", percent: " + win_percents[5] + "%\n\r");
			stats_writer.write ("1-12 spins: " + this.first_twelve + ", percent: " + win_percents[6] + "%\n\r");
			stats_writer.write ("13-24 spins: " + this.second_twelve + ", percent: " + win_percents[7] + "%\n\r");
			stats_writer.write ("25-36 spins: " + this.third_twelve + ", percent: " + win_percents[8] + "%\n\r");
			stats_writer.write ("1-18 spins: " + this.one_to_eighteen + ", percent: " + win_percents[9] + "%\n\r");
			stats_writer.write ("19-36 spins: " + this.nineteen_to_thirtysix + ", percent: " + win_percents[10] + "%\n\r");
			stats_writer.write ("First column: " + this.first_column + ", percent: " + win_percents[11] + "%\n\r");
			stats_writer.write ("Second column: " + this.second_column + ", percent: " + win_percents[12] + "%\n\r");
			stats_writer.write ("Third column: " + this.third_column + ", percent: " + win_percents[13] + "%\n\r");
			
			print_board (stats_writer);
			stats_writer.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private void generate_percents () {
		win_percents [0] = round ((double)this.black_spins/this.spins * 100, 3);
		win_percents [1] = round ((double)this.red_spins/this.spins * 100, 3);
		win_percents [2] = round ((double)this.even_spins/this.spins * 100, 3);
		win_percents [3] = round ((double)this.odd_spins/this.spins * 100, 3);
		win_percents [4] = round ((double)this.zero_spins/this.spins * 100, 3);
		win_percents [5] = round ((double)this.double_zero/this.spins * 100, 3);
		win_percents [6] = round ((double)this.first_twelve/this.spins * 100, 3);
		win_percents [7] = round ((double)this.second_twelve/this.spins * 100, 3);
		win_percents [8] = round ((double)this.third_twelve/this.spins * 100, 3);
		win_percents [9] = round ((double)this.one_to_eighteen/this.spins * 100, 3);
		win_percents [10] = round ((double)this.nineteen_to_thirtysix/this.spins * 100, 3);
		win_percents [11] = round ((double)this.first_column/this.spins * 100, 3);
		win_percents [12] = round ((double)this.second_column/this.spins * 100, 3);
		win_percents [13] = round ((double)this.third_column/this.spins * 100, 3);
		
		int x = 0;
		for (int i = 14; i < win_percents.length; i++) {
			win_percents[i] = round((double)times_won[x] / this.spins * 100, 3);
			x++;
		}
	}
	
	private void print_stats () {
		generate_percents ();
		System.out.println ("Total spins: " + this.spins);
		System.out.println ("Black spins: " + this.black_spins + ", percent: " + win_percents[0] + "%\n\r");
		System.out.println ("Red spins: " + this.red_spins + ", percent: " + win_percents[1] + "%\n\r");
		System.out.println ("Even spins: " + this.even_spins + ", percent: " + win_percents[2] + "%\n\r");
		System.out.println ("Odd spins: " + this.odd_spins + ", percent: " + win_percents[3] + "%\n\r");
		System.out.println ("Zero spins: " + this.zero_spins + ", percent: " + win_percents[4] + "%\n\r");
		System.out.println ("Double Zero spins: " + this.double_zero + ", percent: " + win_percents[5] + "%\n\r");
		System.out.println ("1-12 spins: " + this.first_twelve + ", percent: " + win_percents[6] + "%\n\r");
		System.out.println ("13-24 spins: " + this.second_twelve + ", percent: " + win_percents[7] + "%\n\r");
		System.out.println ("25-36 spins: " + this.third_twelve + ", percent: " + win_percents[8] + "%\n\r");
		System.out.println ("1-18 spins: " + this.one_to_eighteen + ", percent: " + win_percents[9] + "%\n\r");
		System.out.println ("19-36 spins: " + this.nineteen_to_thirtysix + ", percent: " + win_percents[10] + "%\n\r");
		System.out.println ("First column: " + this.first_column + ", percent: " + win_percents[11] + "%\n\r");
		System.out.println ("Second column: " + this.second_column + ", percent: " + win_percents[12] + "%\n\r");
		System.out.println ("Third column: " + this.third_column + ", percent: " + win_percents[13] + "%\n\r");
		System.out.println();
		
		/*System.out.println("Do you want the breakdown for each number? (y/n)" );
		Scanner input = new Scanner (System.in);
		if (input.nextLine().equals("y")) {
			for (int i = 0; i < times_won.length; i++) {
				double win_percent = times_won[i]/this.spins * 100;
				System.out.println("Percent " + i + " was spun: " + round(win_percent, 3) + "%");
			}
		}
		*/
		//System.out.println("Do you want to write the results to file? (y/n)");
		//if (input.nextLine().equals("y")) {
			write_to_file();
		//}
		//input.close();
	}
	
	public void generate_stats () {
		this.spins = winning_spins.size();
		for (Roulette_Slot spin: winning_spins) {
			capture_color(spin.color);
			capture_value(spin.value);
		}
		
		print_stats();
	}
}
