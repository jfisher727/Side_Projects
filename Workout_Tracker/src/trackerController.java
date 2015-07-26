import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.Properties;

import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JTextField;

import org.jfree.data.category.DefaultCategoryDataset;


public class trackerController implements ActionListener{
	
	private trackerModel model;
	private trackerView view;
	
	public trackerController (trackerModel model, trackerView view) {
		this.model = model;
		this.view = view;
		loadProperties();
	}
	
	public void loadProperties () {
		Properties defaultProperties = new Properties ();
		try {
			FileInputStream propLoad = new FileInputStream (this.model.getPropertiesFile());
			defaultProperties.load(propLoad);
			propLoad.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.model.setProperties(defaultProperties);
	}
	
	public void saveProperties () {
		try {
			File propsFile = new File (model.getPropertiesFile());
			OutputStream propStream = new FileOutputStream (propsFile);
			model.getUserProperties().store(propStream, "--- User selected database ---");
			propStream.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static String [] copyToArray (ArrayList <String> list) {
		String [] stringlist = new String [list.size()];
		for (int i = 0; i < list.size(); i++) {
			stringlist [i] = list.get(i);
		}
		return stringlist;
		//model.setMuscleExercises(muscleExercises);
	}
	
	private void loadExercises (int muscleGroup) {
		ArrayList <String> exercises = new ArrayList <String> ();
		BufferedReader exerciseStream = null;
		switch (muscleGroup) {
		case 1:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getChestExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		case 2:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getBackExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		case 3:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getLegExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		case 4:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getShoulderExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		case 5:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getBicepExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		case 6:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getTricepExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		case 7:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(model.getAbExercises())));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			break;
		default:
			System.err.println("No exercises loaded");
			break;
		}
		String line = null;
		try {
			while ((line = exerciseStream.readLine()) != null) {
				exercises.add(line);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		String [] exerciseList = copyToArray (exercises);
		model.setMuscleExercises(exerciseList);
	}
	
	private int oneRepMax (int weight, int reps) {
		double numerator = weight * 100;
		double denominator = 101.3 - (2.67123 * reps); 
		return (int) (numerator / denominator);
	}
	
	private void captureData () {
		//recordedWeights = new ArrayList <Integer> ();
		//recordedReps = new ArrayList <Integer> ();
		
		int totalVolume = 0;
		int totalSets = 0;
		int totalReps = 0;
		int highest1RM = 0;
		ArrayList <JTextField> repInputs = view.getRepInputs();
		ArrayList <JTextField> weightInputs = view.getWeightInputs();
		
		Date selectedDate = this.view.getSelectedDate();
		
		for (int i = 0; i < repInputs.size(); i++) {
			int currentReps = Integer.valueOf(repInputs.get(i).getText());
			int currentWeight = Integer.valueOf(weightInputs.get(i).getText());
			
			int current1RM = oneRepMax (currentWeight, currentReps);
			int currentVolume = currentReps * currentWeight;
			if (current1RM > highest1RM) {
				highest1RM = current1RM;
			}
			totalVolume += currentVolume;
			totalReps += currentReps;
			totalSets += 1;
		}
		System.out.println(highest1RM);
		addEntry (selectedDate, totalVolume, highest1RM, totalSets, totalReps, (String) view.getExerciseMenu().getSelectedItem());
	}
	
	private void addEntry (Date date, int volume, int max, int totalSets, int totalReps, String exercise) {
		DatabaseHandler.addEntry(model.getDBProperty(), new databaseEntry(date, volume, max, totalSets, totalReps), exercise);
	}
	
	public ArrayList <String> captureAllExercises () {
		ArrayList <String> exercises = new ArrayList <String> ();
		String [] groups = this.model.getAllExercises();
		for (int i = 0; i < groups.length; i++) {
			BufferedReader exerciseStream = null;
			String line = null;
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(groups[i])));
				while ((line = exerciseStream.readLine()) != null) {
					if (!line.equals("")) {
						exercises.add(line);
					}
				}
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		Collections.sort(exercises, String.CASE_INSENSITIVE_ORDER);
		return exercises;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		if(e.getSource() == view.getSubmitButton()) {
			Date selectedDate = this.view.getSelectedDate();
			if (view.getGroupMenu().getSelectedIndex () != 0 && view.getExerciseMenu().getSelectedIndex() != 0 && selectedDate != null) {
				try {
					view.setsWindow (Integer.parseInt(view.getSetsTextField().getText()));
				} catch (NumberFormatException err) {
					//System.out.println ("Please Enter a valid number");
					view.generateErrorWindow("Please enter a valid number");
				}
			}
			else {
				//System.out.println("Please select a muscle group and exercise");
				view.generateErrorWindow("Please select a muscle group, exercise, and date.");
			}
		}
		else if (e.getSource() == view.getCancelButton()) {
			this.view.clearInputs ();
		}
		else if (e.getSource() == view.getRecordButton()) {
			captureData ();
			view.clearInputs();
		}
		else if (e.getSource() == view.getSelectButton()) {
			this.view.hideSelectFrame();
			String exercise = (String) this.view.getAllExerciseMenu().getSelectedItem();
			String query = "SELECT * FROM " + exercise;
			ArrayList <databaseEntry> storedRecords = DatabaseHandler.queryDB(model.getDBProperty(), query);
			if (this.model.getGraphMax()) {
				DefaultCategoryDataset maxSet = new DefaultCategoryDataset ();
				for (int i = 0; i < storedRecords.size(); i++) {
					maxSet.addValue(storedRecords.get(i).getMax(), "1-RM", trackerController.dateFormatter(storedRecords.get(i).getDate()));
				}
				this.view.generateMaxGraph(maxSet);
			}
			else {
				DefaultCategoryDataset maxSet = new DefaultCategoryDataset ();
				for (int i = 0; i < storedRecords.size(); i++) {
					maxSet.addValue(storedRecords.get(i).getVolume(), "Volume", trackerController.dateFormatter(storedRecords.get(i).getDate()));
				}
				this.view.generateVolumeGraph(maxSet);
			}
			
		}
		else if (e.getSource() == view.getGroupMenu()) {
			JComboBox <String> exerciseMenu = view.getGroupMenu();
			if (exerciseMenu.getSelectedIndex() != 0) {
				loadExercises (exerciseMenu.getSelectedIndex());
				DefaultComboBoxModel <String> comboModel = new DefaultComboBoxModel <String> (model.getMuscleExercises());
				view.getExerciseMenu().setModel(comboModel);
				view.revalidateWindow();
			}
		}
		else if (e.getSource() == view.getExitItem()) {
			//closes the window
			view.closeWindow();
		}
		else if (e.getSource() == view.getSaveItem()) {
			//writes the user inputs to the database
		}
		else if (e.getSource() == view.getNewDBItem()) {
			//popup window to prompt the user for a name of the new DB they want the
			//data to be stored to. generates a new DB file
			File selectedFile = view.generateNewFileSelect();
			if (selectedFile != null) {
				model.setDBProperty(selectedFile.getAbsolutePath());
				saveProperties();
				DatabaseHandler.generateNewDB(selectedFile.getAbsolutePath(), model.getAllExercises());
			}
		}
		else if (e.getSource() == view.getLoadItem()) {
			File selectedFile = view.generateFileChooser();
			if (selectedFile != null) {
				model.setDBProperty(selectedFile.getAbsolutePath());
				saveProperties();
			}
		}
		else if (e.getSource() == view.getGraphMaxItem()) {
			//generate graph of max over time for the selected exercise
			this.model.graphMax();
			this.view.generateExerciseSelect(captureAllExercises());
		}
		else if (e.getSource() == view.getGraphVolItem()) {
			//generate graph of volume over time for the selected exercise
			this.model.graphVolume();
			this.view.generateExerciseSelect(captureAllExercises());
		}
	}

	public void setActionListeners () {
		this.view.setActionListeners (this);
	}
	
	public void run () {
		setActionListeners ();
		view.run();
	}
	
	public static String dateFormatter (Date d) {
		DateFormat df = new SimpleDateFormat ("MM/dd/yyyy");
		return df.format(d);
	}
}
