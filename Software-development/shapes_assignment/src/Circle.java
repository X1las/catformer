import java.util.*;


public class Circle extends Shape {
    private Vector center;
    private double radius;

    public Circle(Vector center, double radius){
        this.center = center;
        this.radius = radius;
    }

    public Circle(double center_x, double center_y, double radius){
        this.center = new Vector(center_x, center_y);
        this.radius = radius;
    }

    // getters
    public Vector getCenter() {
        return center;
    }
    public double getRadius() {
        return radius;
    }
    // setters
    public void setCenter(Vector center) {
        this.center = center;
    }
    public void setRadius(double radius) {
        this.radius = radius;
    }
    
    // Returning the area of the circle
    public double area(){
        double area = Math.PI * (Math.pow(radius,2));
        return area;
    }

    // Returning the circumference of the circle
    public double circumference(){
        double circumference = 2 * Math.PI * radius;
        return circumference;
    }
    // Returning the center of the circle (technically does the same as the getCenter())
     public Vector center(){
        return center;
    }

    // To check whether a point is inside the circle by checking if the point is closer to the center than the outer ring around it
    public  boolean containsPoint(Vector v){
        Vector dist = v.sub(center);
        double dist_length = dist.length();
        if (dist_length < radius){
            return true;
        }
        return false;
    }

  

}
