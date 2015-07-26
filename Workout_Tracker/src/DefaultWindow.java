import java.awt.event.ActionListener;


public interface DefaultWindow extends ActionListener {

	public static final int DEFAULT_WINDOW_WIDTH = 650;
	public static final int DEFAULT_WINDOW_HEIGHT = 250;
	public static final int DEFAULT_ROW_HEIGHT = 50;
	public static final int DEFAULT_SETS_WIDTH = 200;
	public static final int DEFAULT_COLUMN_WIDTH = 3;
	
	public void run();
	public void setLocation(int x, int y);
	public void closeWindow();
}
