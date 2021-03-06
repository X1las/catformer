
public class Rectangle extends Shape {
    private Vector bottom_left;
    private double width;
    private double height;

    public Rectangle(Vector bottom_left, double width, double height){
        this.bottom_left = bottom_left;
        this.width       = width;
        this.height      = height;
    }

    public Rectangle(double bot_left_x, double bot_left_y,double width, double height){
        this.bottom_left = new Vector(bot_left_x,bot_left_y);
        this.width = width;
        this.height = height;
    }

    // Getters
    public Vector getBottom_left() {
        return bottom_left;
    }
    public double getWidth() {
        return width;
    }
    public double getHeight() {
        return height;
    }
    
    // Setters
    public void setBottom_left(Vector bottom_left) {
        this.bottom_left = bottom_left;
    }
    public void setWidth(double width) {
        this.width = width;
    }
    public void setHeight(double height) {
        this.height = height;
    }
    
    // Returning the area of the rectangle
    public double area(){
        double area = this.width * this.height;
        return area;
    }
    
    // Returning the circumference of the rectangle
    public double circumference(){
       double circumference = (2*height) + (2* width);
       return circumference;
    }

    // Returning the center of the rectangle
    public Vector center(){
        double centerX = bottom_left.x + width/2;
        double centerY = bottom_left.y + height/2;
        Vector center = new Vector(centerX, centerY);
        return center;
    }
    
    // To check whether a point is inside the rectangle
    public boolean containsPoint(Vector v){
        if (v.x > bottom_left.x && v.x < (bottom_left.x + width) && v.y > bottom_left.y && v.y < (bottom_left.y + height)){
            return true;
        }
        return false;
    }
}
