import java.util.*;

public abstract class Shape {

    // Method that will return the area of shape
    public abstract double area();
    
    // Method that will return the circumference of the shape
    public abstract double circumference();

    // Method that will return the center of the shape.
    public abstract Vector center();
    
    // Method that checks whether a point is inside the shape (does not include very outer points of the shape)
    public abstract boolean containsPoint(Vector point);

    // Uses the centers of any two shapes to calculate the distance between their centers. 
    public double dist(Shape shape){
        Vector v = this.center().sub(shape.center());
        return v.length();
    }

}

