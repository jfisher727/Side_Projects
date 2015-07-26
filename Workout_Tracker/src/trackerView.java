import java.awt.event.ActionListener;
import java.io.File;
import java.util.ArrayList;
import java.util.Date;
import java.util.Properties;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;

import org.jdatepicker.impl.JDatePanelImpl;
import org.jdatepicker.impl.JDatePickerImpl;
import org.jdatepicker.impl.UtilDateModel;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;


public class trackerView {
	private JFrame primaryFrame;
	private JFrame selectFrame;
	private JPanel primaryPanel;
	private JPanel topPanel;
	private JPanel leftPanel;
	private JPanel rightPanel;
	private JScrollPane scrollPanel;
	private JPanel datePanel;
	private JPanel muscleGroupPanel;
	private JPanel exercisePanel;
	private JPanel setsPanel;
	private JPanel submitPanel;
	
	private JMenuBar menuBar;
	private JMenu fileMenu;
	private JMenuItem newDBItem;
	private JMenuItem loadItem;
	private JMenuItem saveItem;
	private JMenuItem exitItem;
	private JMenu graphMenu;
	private JMenuItem graphMaxItem;
	private JMenuItem graphVolItem;
	
	private JLabel dateLabel;
	private JLabel muscleGroupLabel;
	private JLabel exerciseLabel;
	private JLabel setsLabel;
	
	private JTextField setsTextField;
	private JFileChooser dbSelector;
	private JDatePickerImpl datePicker;
	
	private JComboBox <String> muscleGroupMenu;
	private JComboBox <String> exerciseMenu;
	private JComboBox <String> allExerciseMenu;
	private JButton submitButton;
	private JButton cancelButton;
	private JButton recordButton;
	private JButton selectButton;
	
	private ArrayList <JTextField> repInputs;
	private ArrayList <JTextField> weightInputs;
	
	private trackerModel model;
	
	public trackerView (trackerModel model) {
		this.model = model;
		
		primaryFrame = new JFrame ();
		primaryPanel = new JPanel ();
		topPanel = new JPanel ();
		leftPanel = new JPanel ();
		rightPanel = new JPanel ();
		datePanel = new JPanel ();
		muscleGroupPanel = new JPanel ();
		exercisePanel = new JPanel ();
		setsPanel = new JPanel ();
		submitPanel = new JPanel ();
		
		menuBar = new JMenuBar();
		fileMenu = new JMenu ("File");
		newDBItem = new JMenuItem ("New");
		loadItem = new JMenuItem ("Load Dataset");
		saveItem = new JMenuItem ("Save Dataset");
		exitItem = new JMenuItem ("Exit");
		
		fileMenu.add(newDBItem);
		fileMenu.add(loadItem);
		fileMenu.add(saveItem);
		fileMenu.add(exitItem);
		
		graphMenu = new JMenu ("Graph");
		graphMaxItem = new JMenuItem ("Graph 1RM");
		graphVolItem = new JMenuItem ("Graph Volume");
		
		graphMenu.add(graphMaxItem);
		graphMenu.add(graphVolItem);
		
		menuBar.add(fileMenu);
		menuBar.add(graphMenu);
		
		dateLabel = new JLabel ("Select Date:");
		muscleGroupLabel = new JLabel ("Select Muscle Group:");
		exerciseLabel = new JLabel ("Select Exercise:");
		setsLabel = new JLabel ("Sets:");
		
		setsTextField = new JTextField ();
		setsTextField.setColumns(DefaultWindow.DEFAULT_COLUMN_WIDTH);
		setsPanel.add(setsLabel);
		setsPanel.add(setsTextField);
		
		UtilDateModel dateModel = new UtilDateModel();
		Properties props = new Properties ();
		props.put("text.today", "Today");
		props.put("text.month", "Month");
		props.put("text.year", "Year");
		JDatePanelImpl datePanelImpl = new JDatePanelImpl(dateModel, props);
		datePicker = new JDatePickerImpl(datePanelImpl, new DateLabelFormatter());
		
		datePanel.add(dateLabel);
		datePanel.add(datePicker);
		
		muscleGroupMenu = new JComboBox <String> (this.model.getMuscleGroups());
		muscleGroupMenu.setSelectedIndex(0);
		//muscleGroupMenu.addActionListener(this);
		
		exerciseMenu = new JComboBox <String> ();
		exercisePanel.add(exerciseLabel);
		exercisePanel.add(exerciseMenu);
		
		muscleGroupPanel.add(muscleGroupLabel);
		muscleGroupPanel.add(muscleGroupMenu);
				
		submitButton = new JButton ("Submit");
		cancelButton = new JButton ("Cancel");
		recordButton = new JButton ("Record");
		selectButton = new JButton ("Select");
		
		setsPanel.add(setsLabel);
		setsPanel.add(setsTextField);
		
		submitPanel.setLayout(new BoxLayout(submitPanel, BoxLayout.LINE_AXIS));
		submitPanel.add(submitButton);
		//submitPanel.add(finishButton);
		submitPanel.add(recordButton);
		submitPanel.add(cancelButton);
		
		leftPanel.setLayout(new BoxLayout(leftPanel, BoxLayout.PAGE_AXIS));
		leftPanel.add(datePanel);
		leftPanel.add(muscleGroupPanel);
		leftPanel.add(exercisePanel);
		leftPanel.add(setsPanel);
		//leftPanel.add(submitPanel);
		
		JPanel tempPanel = new JPanel ();
		JTextField tempWeight = new JTextField ();
		tempWeight.setColumns(DefaultWindow.DEFAULT_COLUMN_WIDTH);
		JTextField tempRep = new JTextField ();
		tempRep.setColumns(DefaultWindow.DEFAULT_COLUMN_WIDTH);
		
		JLabel repsLabel = new JLabel ("Reps");
		JLabel weightLabel = new JLabel ("Weight");
		
		tempPanel.add(weightLabel);
		tempPanel.add(tempWeight);
		tempPanel.add(repsLabel);
		tempPanel.add(tempRep);
		
		rightPanel.add(tempPanel);
		
		topPanel.setLayout(new BoxLayout(topPanel, BoxLayout.LINE_AXIS));
		topPanel.add(leftPanel);
		topPanel.add(Box.createHorizontalGlue());
		topPanel.add(rightPanel);
				
		primaryPanel.setLayout(new BoxLayout(primaryPanel, BoxLayout.PAGE_AXIS));
		primaryPanel.add(topPanel);
		primaryPanel.add(submitPanel);
		
		primaryFrame.add(primaryPanel);
		primaryFrame.setJMenuBar(menuBar);
		primaryFrame.setSize(DefaultWindow.DEFAULT_WINDOW_WIDTH, DefaultWindow.DEFAULT_WINDOW_HEIGHT);
		//primaryFrame.setSize(800, 200);
		primaryFrame.setResizable(false);
		//primaryFrame.pack();
		primaryFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	public void setsWindow (int setsCount) {
		if(scrollPanel != null && scrollPanel.getParent().equals(topPanel)) {
			topPanel.remove(scrollPanel);
		}
		rightPanel.removeAll();
		rightPanel.setLayout(new BoxLayout(rightPanel, BoxLayout.PAGE_AXIS));
		
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
		
		topPanel.remove(rightPanel);
		topPanel.add(scrollPanel);
		primaryFrame.revalidate();
	}
	
	private void resetSetPanel () {
		if (scrollPanel != null && scrollPanel.getParent().equals(topPanel)) {
			topPanel.remove(scrollPanel);
			scrollPanel = null;
		}
		else {
			topPanel.remove(rightPanel);
		}
		
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
		topPanel.add(rightPanel);
		//primaryFrame.pack();
		primaryFrame.revalidate();
	}
	
	public void clearInputs () {
		muscleGroupMenu.setSelectedIndex(0);
		if(exerciseMenu.getItemCount() >= 1) {
			exerciseMenu.setSelectedIndex(0);
		}
		setsTextField.setText("");
		resetSetPanel();
		primaryFrame.revalidate();
	}
	
	public void run() {
		primaryFrame.setVisible(true);
	}

	public void setLocation(int x, int y) {
		primaryFrame.setLocation(x, y);
	}

	public void closeWindow() {
		primaryFrame.setVisible(false);
		primaryFrame.dispose();
	}
	
	public void revalidateWindow () {
		primaryFrame.revalidate();
	}

	public void generateErrorWindow (String message) {
		JOptionPane.showMessageDialog(new JFrame(), message, "Error", JOptionPane.ERROR_MESSAGE);
	}
	
	public void setActionListeners (ActionListener a) {
		setCancelAL(a);
		setRecordAL(a);
		setGroupMenuAL(a);
		setSaveAL(a);
		setSubmitAL(a);
		setSelectAL (a);
		setExitAL(a);
		setNewDBAL(a);
		setLoadAL(a);
		setGraphMaxAL(a);
		setGraphVolAL(a);
	}

	public void setSelectAL (ActionListener a) {
		selectButton.addActionListener(a);
	}

	public void setSubmitAL (ActionListener a) {
		submitButton.addActionListener(a);
	}
	
	public void setCancelAL (ActionListener a) {
		cancelButton.addActionListener(a);
	}
	
	public void setRecordAL (ActionListener a) {
		this.recordButton.addActionListener(a);
	}

	public void setGroupMenuAL (ActionListener a) {
		muscleGroupMenu.addActionListener(a);
	}

	public void setNewDBAL (ActionListener a) {
		this.newDBItem.addActionListener(a);
	}
	
	public void setLoadAL (ActionListener a) {
		this.loadItem.addActionListener(a);
	}
	
	public void setSaveAL (ActionListener a) {
		this.saveItem.addActionListener(a);
	}
	
	public void setExitAL (ActionListener a) {
		this.exitItem.addActionListener(a);
	}

	public void setGraphMaxAL (ActionListener a) {
		this.graphMaxItem.addActionListener(a);
	}
	
	public void setGraphVolAL (ActionListener a) {
		this.graphVolItem.addActionListener(a);
	}
	
	public JButton getSubmitButton () {
		return this.submitButton;
	}
	
	public JButton getCancelButton () {
		return this.cancelButton;
	}
	
	public JButton getRecordButton () {
		return this.recordButton;
	}
	
	public JButton getSelectButton () {
		return this.selectButton;
	}

	public JComboBox <String> getGroupMenu () {
		return this.muscleGroupMenu;
	}
	
	public JComboBox <String> getExerciseMenu () {
		return this.exerciseMenu;
	}

	public JComboBox <String> getAllExerciseMenu () {
		return this.allExerciseMenu;
	}
	
	public JTextField getSetsTextField () {
		return this.setsTextField;
	}
	
	public ArrayList <JTextField> getRepInputs () {
		return this.repInputs;
	}
	
	public ArrayList <JTextField> getWeightInputs () {
		return this.weightInputs;
	}
	
	public JMenuItem getNewDBItem () {
		return this.newDBItem;
	}
	
	public JMenuItem getLoadItem () {
		return this.loadItem;
	}
	
	public JMenuItem getExitItem () {
		return this.exitItem;
	}
	
	public JMenuItem getSaveItem () {
		return this.saveItem;
	}
	
	public JMenuItem getGraphMaxItem () {
		return this.graphMaxItem;
	}
	
	public JMenuItem getGraphVolItem () {
		return this.graphVolItem;
	}
	
	public JFrame getJFrame () {
		return new JFrame ();
	}
	
	public Date getSelectedDate () {
		Date date;
		if (datePicker.getModel().getValue() != null) {
			date = (Date) datePicker.getModel().getValue();
		}
		else {
			date = new Date ();
		}
		return date;
		/*
		DateFormat df = new SimpleDateFormat ("MM/dd/yyyy");
		return df.format(date);
		*/
	}
	
	public File generateFileChooser () {
		dbSelector = new JFileChooser ();
		dbSelector.setFileSelectionMode(JFileChooser.FILES_ONLY);
		int returnValue = dbSelector.showOpenDialog(new JFrame());
		if (returnValue == JFileChooser.APPROVE_OPTION) {
            return dbSelector.getSelectedFile();
        }
		return null;
	}
	
	public File generateNewFileSelect () {
		dbSelector = new JFileChooser ();
		dbSelector.setFileSelectionMode(JFileChooser.FILES_ONLY);
		int returnValue = dbSelector.showSaveDialog(new JFrame());
		if (returnValue == JFileChooser.APPROVE_OPTION) {
            return dbSelector.getSelectedFile();
        }
		return null;
	}
	
	public void generateExerciseSelect (ArrayList <String> exercises) {
		selectFrame = new JFrame ();
		JPanel defaultPanel = new JPanel ();
		JPanel selectPanel = new JPanel ();
		JPanel buttonPanel = new JPanel ();
		
		String [] allExercises = trackerController.copyToArray(exercises);
		allExerciseMenu = new JComboBox <String> (allExercises);
		
		selectPanel.add(allExerciseMenu);
		buttonPanel.add(selectButton);
		
		defaultPanel.setLayout(new BoxLayout(defaultPanel, BoxLayout.PAGE_AXIS));
		defaultPanel.add(selectPanel);
		defaultPanel.add(buttonPanel);
		selectFrame.add(defaultPanel);
		selectFrame.pack();
		selectFrame.setLocation(primaryFrame.getLocation());
		selectFrame.setVisible(true);
	}
	
	public void hideSelectFrame () {
		selectFrame.setVisible(false);
	}

	public void generateMaxGraph (DefaultCategoryDataset graphData) {
		JFreeChart lineChart = ChartFactory.createLineChart(
		         "1-RM vs Date",
		         "Date","1-RM",
		         graphData,
		         PlotOrientation.VERTICAL,
		         true,true,false);
		         
		      ChartPanel chartPanel = new ChartPanel( lineChart );
		      chartPanel.setPreferredSize( new java.awt.Dimension( 560 , 367 ) );
		      JFrame graphFrame = new JFrame ();
		      graphFrame.add(chartPanel);
		      graphFrame.pack();
		      graphFrame.setLocation(primaryFrame.getLocation());
		      graphFrame.setVisible(true);
	}
	
	public void generateVolumeGraph (DefaultCategoryDataset graphData) {
		JFreeChart lineChart = ChartFactory.createLineChart(
		         "Volume vs Date",
		         "Date","Volume",
		         graphData,
		         PlotOrientation.VERTICAL,
		         true,true,false);
		         
		      ChartPanel chartPanel = new ChartPanel( lineChart );
		      chartPanel.setPreferredSize( new java.awt.Dimension( 560 , 367 ) );
		      JFrame graphFrame = new JFrame ();
		      graphFrame.add(chartPanel);
		      graphFrame.pack();
		      graphFrame.setLocation(primaryFrame.getLocation());
		      graphFrame.setVisible(true);
	}
}
