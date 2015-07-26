import java.awt.event.ActionEvent;
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
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;


public class primaryWindow implements DefaultWindow{
	private static final String dbFileName = "records.db";
	
	private static final String chestExercises = "chest_exercises.txt";
	private static final String backExercises = "back_exercises.txt";
	private static final String legExercises = "leg_exercises.txt";
	private static final String shoulderExercises = "shoulder_exercises.txt";
	private static final String bicepExercises = "bicep_exercises.txt";
	private static final String tricepExercises = "tricep_exercises.txt";
	private static final String abExercises = "ab_exercises.txt";
	
	String [] muscleGroups = {"", "Chest", "Back", "Legs", "Shoulders", "Biceps", "Triceps", "Abs"};
	String [] muscleExercises;
	
	JFrame primaryFrame;
	JPanel primaryPanel;
	JPanel leftPanel;
	JPanel rightPanel;
	JScrollPane scrollPanel;
	JPanel muscleGroupPanel;
	JPanel exercisePanel;
	JPanel setsPanel;
	JPanel submitPanel;
	JPanel savePanel;
	
	JLabel muscleGroupLabel;
	JLabel exerciseLabel;
	JLabel setsLabel;
	
	JTextField setsTextField;
	
	JComboBox <String> muscleGroupMenu;
	JComboBox <String> exerciseMenu;
	JButton submitButton;
	JButton cancelButton;
	JButton finishButton;
	JButton saveButton;
	JButton graphButton;
	
	ArrayList <JPanel> multipleSetPanels;
	ArrayList <JTextField> repInputs;
	ArrayList <JTextField> weightInputs;
	
	ArrayList <Integer> recordedWeights;
	ArrayList <Integer> recordedReps;
	
	public primaryWindow () {
		primaryFrame = new JFrame ();
		primaryPanel = new JPanel ();
		leftPanel = new JPanel ();
		rightPanel = new JPanel ();
		muscleGroupPanel = new JPanel ();
		exercisePanel = new JPanel ();
		setsPanel = new JPanel ();
		submitPanel = new JPanel ();
		savePanel = new JPanel ();
		
		muscleGroupLabel = new JLabel ("Select Muscle Group:");
		exerciseLabel = new JLabel ("Select Exercise:");
		setsLabel = new JLabel ("Sets:");
		
		setsTextField = new JTextField ();
		setsTextField.setColumns(3);
		setsPanel.add(setsLabel);
		setsPanel.add(setsTextField);
		
		muscleGroupMenu = new JComboBox <String> (muscleGroups);
		muscleGroupMenu.setSelectedIndex(0);
		muscleGroupMenu.addActionListener(this);
		
		exerciseMenu = new JComboBox <String> ();
		exercisePanel.add(exerciseLabel);
		exercisePanel.add(exerciseMenu);
		
		muscleGroupPanel.add(muscleGroupLabel);
		muscleGroupPanel.add(muscleGroupMenu);
				
		submitButton = new JButton ("Submit");
		submitButton.addActionListener(this);
		cancelButton = new JButton ("Cancel");
		cancelButton.addActionListener(this);
		finishButton = new JButton ("Finish");
		finishButton.addActionListener(this);
		saveButton = new JButton ("Save");
		saveButton.addActionListener(this);
		graphButton = new JButton ("Graph");
		graphButton.addActionListener(this);
		
		setsPanel.add(setsLabel);
		setsPanel.add(setsTextField);
		
		submitPanel.setLayout(new BoxLayout(submitPanel, BoxLayout.LINE_AXIS));
		submitPanel.add(submitButton);
		//submitPanel.add(finishButton);
		submitPanel.add(cancelButton);
		
		leftPanel.setLayout(new BoxLayout(leftPanel, BoxLayout.PAGE_AXIS));
		leftPanel.add(muscleGroupPanel);
		leftPanel.add(exercisePanel);
		leftPanel.add(setsPanel);
		leftPanel.add(submitPanel);
		
		JPanel tempPanel = new JPanel ();
		JTextField tempWeight = new JTextField ();
		tempWeight.setColumns(3);
		JTextField tempRep = new JTextField ();
		tempRep.setColumns(3);
		
		JLabel repsLabel = new JLabel ("Reps");
		JLabel weightLabel = new JLabel ("Weight");
		
		tempPanel.add(weightLabel);
		tempPanel.add(tempWeight);
		tempPanel.add(repsLabel);
		tempPanel.add(tempRep);
		
		rightPanel.add(tempPanel);
				
		primaryPanel.setLayout(new BoxLayout(primaryPanel, BoxLayout.LINE_AXIS));
		primaryPanel.add(leftPanel);
		primaryPanel.add(Box.createHorizontalGlue());
		primaryPanel.add(rightPanel);
		
		primaryFrame.add(primaryPanel);
		primaryFrame.setSize(575, 200);
		primaryFrame.pack();
		primaryFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	private void setsWindow (int setsCount) {
		rightPanel.removeAll();
		rightPanel.setLayout(new BoxLayout(rightPanel, BoxLayout.PAGE_AXIS));
		
		multipleSetPanels = new ArrayList <JPanel> ();
		repInputs = new ArrayList <JTextField> ();
		weightInputs = new ArrayList <JTextField> ();
		
		for(int i = 0; i < setsCount; i++) {
			JPanel tempPanel = new JPanel ();
			JTextField tempWeight = new JTextField ();
			tempWeight.setColumns(3);
			weightInputs.add(tempWeight);
			JTextField tempRep = new JTextField ();
			tempRep.setColumns(3);
			repInputs.add(tempRep);
			
			JLabel repsLabel = new JLabel ("Reps");
			JLabel weightLabel = new JLabel ("Weight");
			
			tempPanel.add(weightLabel);
			tempPanel.add(tempWeight);
			tempPanel.add(repsLabel);
			tempPanel.add(tempRep);
			
			rightPanel.add(tempPanel);
		}

		scrollPanel = new JScrollPane (rightPanel);
		scrollPanel.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
		scrollPanel.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		
		savePanel = new JPanel ();
		savePanel.setLayout(new BoxLayout(savePanel, BoxLayout.LINE_AXIS));
		savePanel.add(saveButton);
		savePanel.add(graphButton);
		
		rightPanel.add(savePanel);
		
		primaryPanel.remove(rightPanel);
		primaryPanel.add(scrollPanel);
		primaryFrame.pack();
		primaryFrame.revalidate();
	}
	
	private void copyToArray (ArrayList <String> exercises) {
		muscleExercises = new String [exercises.size()];
		for (int i = 0; i < exercises.size(); i++) {
			muscleExercises [i] = exercises.get(i);
		}
	}
	
	private void loadExercises (int muscleGroup) {
		ArrayList <String> exercises = new ArrayList <String> ();
		BufferedReader exerciseStream = null;
		switch (muscleGroup) {
		case 1:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(chestExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		case 2:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(backExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		case 3:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(legExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		case 4:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(shoulderExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		case 5:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(bicepExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		case 6:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(tricepExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		case 7:
			try {
				exerciseStream = new BufferedReader (new FileReader(new File(abExercises)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
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
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		copyToArray (exercises);
	}

	private int oneRepMax (int weight, int reps) {
		double numerator = weight * 100;
		double denominator = 101.3 - (2.67123 * reps); 
		return (int) (numerator / denominator);
	}
	
	private void addEntry (int volume, int max, int totalSets, int totalReps, String exercise) {
		Date currentDate = new Date ();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd");
		String date = sdf.format(currentDate);
		String insertStatement = "INSERT INTO " + exercise + " (Date,Volume,Max,Sets,Reps) VALUES ( '" + date + "', ";
		insertStatement += volume + ", " + max + ", " + totalSets + ", " + totalReps + " );";
		
		System.out.println(insertStatement);
		Connection dbConnection;
		Statement insertion = null;
		try {
			dbConnection = DriverManager.getConnection("jdbc:sqlite:" + dbFileName);
			insertion = dbConnection.createStatement();
			insertion.executeUpdate(insertStatement);
			dbConnection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		//System.out.println(insertStatement);
	}
	
	private void captureData () {
		//recordedWeights = new ArrayList <Integer> ();
		//recordedReps = new ArrayList <Integer> ();
		
		int totalVolume = 0;
		int totalSets = 0;
		int totalReps = 0;
		int highest1RM = 0;
		
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
		addEntry (totalVolume, highest1RM, totalSets, totalReps, (String) exerciseMenu.getSelectedItem());
	}
	
	private void resetSetPanel () {
		primaryPanel.remove(scrollPanel);
		
		rightPanel = new JPanel ();
		
		JPanel tempPanel = new JPanel ();
		JTextField tempWeight = new JTextField ();
		tempWeight.setColumns(3);
		JTextField tempRep = new JTextField ();
		tempRep.setColumns(3);
		
		JLabel repsLabel = new JLabel ("Reps");
		JLabel weightLabel = new JLabel ("Weight");
		
		tempPanel.add(weightLabel);
		tempPanel.add(tempWeight);
		tempPanel.add(repsLabel);
		tempPanel.add(tempRep);
		
		rightPanel.add(tempPanel);
		primaryPanel.add(rightPanel);
		primaryFrame.pack();
		primaryFrame.revalidate();
	}
	
	private void clearInputs () {
		muscleGroupMenu.setSelectedIndex(0);
		exerciseMenu.setSelectedIndex(0);
		setsTextField.setText(" ");
		resetSetPanel();
		primaryFrame.revalidate();
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		if(e.getSource() == submitButton) {
			if (muscleGroupMenu.getSelectedIndex () != 0 && exerciseMenu.getSelectedIndex() != 0) {
				try {
					setsWindow (Integer.parseInt(setsTextField.getText()));
				} catch (NumberFormatException err) {
					System.out.println ("Please Enter a valid number");
				}
			}
			else {
				System.out.println("Please select a muscle group and exercise");
			}
		}
		else if (e.getSource() == finishButton) {
			
		}
		else if (e.getSource() == cancelButton) {
			
		}
		else if (e.getSource() == saveButton) {
			captureData ();
			clearInputs();
		}
		else if (e.getSource() == graphButton) {
			
		}
		else if (e.getSource() == muscleGroupMenu) {
			if (muscleGroupMenu.getSelectedIndex() != 0) {
				loadExercises (muscleGroupMenu.getSelectedIndex());
				DefaultComboBoxModel <String> model = new DefaultComboBoxModel <String> (muscleExercises);
				exerciseMenu.setModel(model);
			}
		}
	}
	
	public ArrayList <databaseEntry> queryDatabase (String exercise) {
		ArrayList <databaseEntry> entries = new ArrayList <databaseEntry> ();
		String queryStatement = "SELECT * from " + exercise + ";";
		Connection dbConnection;
		Statement query = null;
		try {
			dbConnection = DriverManager.getConnection("jdbc:sqlite:" + dbFileName);
			query = dbConnection.createStatement();
			ResultSet queryResults = query.executeQuery(queryStatement);
			while (queryResults.next()) {
				String date = queryResults.getString(0);
				int volume = queryResults.getInt("Volume");
				int max = queryResults.getInt("Max");
				int sets = queryResults.getInt("Sets");
				int reps = queryResults.getInt("Reps");
				
				entries.add(new databaseEntry(date, volume, max, sets, reps));
			}
			dbConnection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return entries;
	}

	@Override
	public void run() {
		primaryFrame.setVisible(true);
	}

	@Override
	public void setLocation(int x, int y) {
		primaryFrame.setLocation(x, y);
	}

	@Override
	public void closeWindow() {
		primaryFrame.setVisible(false);
	}

}
