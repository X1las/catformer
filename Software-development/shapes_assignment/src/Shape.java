import java.util.*;

public abstract class Shape {
    


    public abstract double area();
    
    public abstract double circumference();

    public abstract Vector center();
    
    public abstract boolean isInside(Vector point);

    
    public double dist(Shape shape){
        Vector v = this.center().sub(shape.center());
        double result = v.length();
        return result;
    }   

}

