import java.util.*;

public abstract class Shape {
    


    public abstract double area();
    
    public abstract double circumference();

    public abstract Vector center();
    
    public abstract boolean isInside(Vector point);

    public abstract double dist(Shape shape);


}

