import java.util.ArrayList;
import java.util.Properties;

import org.jfree.data.category.CategoryDataset;
import org.jfree.data.category.DefaultCategoryDataset;


public class trackerModel {
	private static final String dbProperty = "DBName";
	private final String propertiesFile = "properties.txt";
	//private String dbFileName = "records.db";
	private Properties userProperties;
	
	private static final String chestExercises = "chest_exercises.txt";
	private static final String backExercises = "back_exercises.txt";
	private static final String legExercises = "leg_exercises.txt";
	private static final String shoulderExercises = "shoulder_exercises.txt";
	private static final String bicepExercises = "bicep_exercises.txt";
	private static final String tricepExercises = "tricep_exercises.txt";
	private static final String abExercises = "ab_exercises.txt";
	
	private boolean graphMax = false;
	private boolean graphVolume = false;
	
	private String [] muscleGroups = {"", "Chest", "Back", "Legs", "Shoulders", "Biceps", "Triceps", "Abs"};
	private String [] muscleExercises;
	
	private ArrayList <Integer> recordedWeights;
	private ArrayList <Integer> recordedReps;
	
	private ArrayList <databaseEntry> dbEntries;
	
	public trackerModel () {
		
	}
	
	public String getPropertiesFile () {
		return propertiesFile;
	}
	
	public Properties getUserProperties () {
		return userProperties;
	}
	
	public void setRecordedWeights (ArrayList <Integer> weights) {
		this.recordedWeights = weights;
	}
	
	public void setRecordedReps (ArrayList <Integer> reps ) {
		this.recordedReps = reps;
	}

	public void setProperties (Properties props) {
		this.userProperties = props;
	}
	
	public void setDBProperty (String dbName) {
		this.userProperties.remove(dbProperty);
		this.userProperties.put(dbProperty, dbName);
	}

	public void setDBEntries (ArrayList <databaseEntry> entries) {
		this.dbEntries = entries;
	}

	public ArrayList <Integer> getRecordedWeights () {
		return this.recordedWeights;
	}
	
	public ArrayList <Integer> getRecordedReps () {
		return this.recordedReps;
	}
	
	public String getChestExercises () {
		return chestExercises;
	}
	
	public String getBackExercises () {
		return backExercises;
	}
	
	public String getLegExercises () {
		return legExercises;
	}
	
	public String getShoulderExercises () {
		return shoulderExercises;
	}
	
	public String getBicepExercises () {
		return bicepExercises;
	}
	
	public String getTricepExercises () {
		return tricepExercises;
	}
	
	public String getAbExercises () {
		return abExercises;
	}

	public String [] getMuscleGroups () {
		return this.muscleGroups;
	}
	
	public String [] getMuscleExercises () {
		return this.muscleExercises;
	}
	
	public String [] getAllExercises () {
		return new String [] {chestExercises, backExercises, legExercises, bicepExercises, tricepExercises, shoulderExercises, abExercises};
	}
	
	public boolean getGraphMax () {
		return this.graphMax;
	}
	
	public boolean getGraphVolume () {
		return this.graphVolume;
	}
	
	public void graphMax () {
		graphMax = true;
		graphVolume = false;
	}
	
	public void graphVolume () {
		graphVolume = true;
		graphMax = false;
	}

	public void setMuscleExercises (String [] exercises) {
		this.muscleExercises = exercises;
	}
	
	public String getDBProperty () {
		return this.userProperties.getProperty(dbProperty);
	}
	
	public CategoryDataset getMaxDataset () {
		DefaultCategoryDataset maxSet = new DefaultCategoryDataset ();
		if (dbEntries.size() > 0) {
			for(int i = 0; i < dbEntries.size(); i++) {
				maxSet.addValue(dbEntries.get(i).getMax(), "Weight", trackerController.dateFormatter(dbEntries.get(i).getDate()));
			}
		}
		return maxSet;
	}
	
	public CategoryDataset getVolumeDataset () {
		DefaultCategoryDataset volumeSet = new DefaultCategoryDataset();
		
		if (dbEntries.size() > 0) {
			for(int i = 0; i < dbEntries.size(); i++) {
				volumeSet.addValue(dbEntries.get(i).getVolume(), "Weight", trackerController.dateFormatter(dbEntries.get(i).getDate()));
			}
		}
		return volumeSet;
	}
}
