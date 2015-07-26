import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;


public class DatabaseHandler {
	
	public static void addEntry (String dbFile, databaseEntry entry, String exercise) {
		Date date = entry.getDate();
		String insertStatement = "INSERT INTO " + exercise + " (Date,Volume,Max,Sets,Reps) VALUES ( '" + trackerController.dateFormatter(date) + "', ";
		insertStatement += entry.getVolume() + ", " + entry.getMax() + ", " + entry.getSets() + ", " + entry.getReps() + " );";
		
		System.out.println(insertStatement);
		Connection dbConnection;
		Statement insertion = null;
		try {
			dbConnection = DriverManager.getConnection("jdbc:sqlite:" + dbFile);
			insertion = dbConnection.createStatement();
			insertion.executeUpdate(insertStatement);
			dbConnection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		//System.out.println(insertStatement);
	}
	
	public static ArrayList <databaseEntry> queryDB (String dbFile, String query) {
		ArrayList <databaseEntry> entries = new ArrayList <databaseEntry> ();
		Connection dbConnection;
		Statement queryStatement = null;
		try {
			dbConnection = DriverManager.getConnection("jdbc:sqlite:" + dbFile);
			queryStatement = dbConnection.createStatement();
			ResultSet queryResults = queryStatement.executeQuery(query);
			while (queryResults.next()) {
				String dateString = queryResults.getString("Date");
				DateFormat df = new SimpleDateFormat ("MM/dd/yyyy");
				Date date;
				try {
					date = df.parse(dateString);
					int volume = queryResults.getInt("Volume");
					int max = queryResults.getInt("Max");
					int sets = queryResults.getInt("Sets");
					int reps = queryResults.getInt("Reps");
					
					entries.add(new databaseEntry(date, volume, max, sets, reps));
				} catch (ParseException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			dbConnection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		Collections.sort(entries, new Comparator<databaseEntry>() {

			@Override
			public int compare(databaseEntry o1, databaseEntry o2) {
				return o1.getDate().compareTo(o2.getDate());
			}
			
		});
		//sort entries based on date, to make sure they're in correct order
		return entries;
	}

	public static void generateTable (String dbFile, String exercise) {
		String createStatement = "CREATE TABLE '" + exercise + "' (" +
								" 'Date' TEXT NOT NULL," +
								" 'Volume' INTEGER NOT NULL DEFAULT 0," +
								" 'Max' INTEGER NOT NULL DEFAULT 0," +
								" 'Sets' INTEGER NOT NULL DEFAULT 0," +
								" 'Reps' INTEGER NOT NULL DEFAULT 0 )";
		
		Connection dbConnection;
		Statement insertion = null;
		//System.out.println(createStatement);
		try {
			dbConnection = DriverManager.getConnection("jdbc:sqlite:" + dbFile);
			insertion = dbConnection.createStatement();
			insertion.executeUpdate(createStatement);
			dbConnection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public static void generateNewDB (String dbFile, String [] exerciseFiles) {
		//generate the appropriate DB table 
		ArrayList <String> exercises = new ArrayList <String> ();
		BufferedReader exerciseStream = null;
		for (int i = 0; i < exerciseFiles.length; i++) {
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(exerciseFiles[i])));
				String line = null;
				while ((line = exerciseStream.readLine()) != null) {
					exercises.add(line);
				}
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
			for (String exercise: exercises) {
				if(!exercise.equals("")) {
					generateTable(dbFile, exercise);
				}
			}
			exercises.clear();
		}
	}
}
