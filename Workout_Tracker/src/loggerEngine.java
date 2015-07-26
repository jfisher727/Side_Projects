import java.awt.GraphicsEnvironment;
import java.awt.Rectangle;


public class loggerEngine {
	
	public static void main (String [] args) {
		try {
			Class.forName("org.sqlite.JDBC");
			trackerModel model = new trackerModel ();
			trackerView view = new trackerView (model);
			trackerController controller = new trackerController (model, view);
			Rectangle rec = GraphicsEnvironment.getLocalGraphicsEnvironment().getMaximumWindowBounds();
			view.setLocation((int)((rec.getWidth()/2) - (DefaultWindow.DEFAULT_WINDOW_WIDTH/2)),
					(int)((rec.getHeight()/2) - (DefaultWindow.DEFAULT_WINDOW_HEIGHT/2)));
			controller.run();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
