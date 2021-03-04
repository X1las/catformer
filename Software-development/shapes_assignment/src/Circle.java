import java.util.*;


public class Circle extends Shape {
    Vector center;
    double radius;

    public Circle(Vector center, double radius){
        this.center = center;
        this.radius = radius;
    }
    

    public double area(){
        double area = Math.PI * (Math.pow(radius,2));
        return area;
    }
    
    public double circumference(){
        double circumference = 2 * Math.PI * radius;
        return circumference;
    }

    public Vector center(){
        return center;
    }
    
    public  boolean isInside(Vector v){
        Vector dist = v.sub(center);
        double dist_length = dist.length();
        if (dist_length < radius){
            return true;
        }
        return false;
    }

  

}
