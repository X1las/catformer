import java.util.*;
import java.math.*;


public class Triangle extends Shape{
    Vector pointA;
    Vector pointB;
    Vector pointC;

    public Triangle(Vector pointA, Vector pointB, Vector pointC){
        this.pointA = pointA;
        this.pointB = pointB;
        this.pointC = pointC;
    }

    private double lengthOfSide(Vector vec1, Vector vec2){
        double side_length = vec1.sub(vec2).length();
        return side_length;
    
    }

    // DONE
    public double area(){
        
        // length of all sides of the triangle
        double sideBC = lengthOfSide(pointB,pointC);
        double sideAC = lengthOfSide(pointA,pointC);
        double sideAB = lengthOfSide(pointA,pointB);
        
        // s = (a+b+c)/2
        double semiperimeter = circumference() / 2;
        
        //Heron's formula: area = sqrt(s*(s-a)(s-b)(s-c))
        double area = Math.sqrt(semiperimeter * (semiperimeter - sideBC * (semiperimeter - sideAC) * (semiperimeter - sideAB)));
        return area;
    }

    //DONE
    public double circumference(){
        Vector sideBC = pointB.sub(pointC);
        Vector sideAC = pointA.sub(pointC);
        Vector sideAB = pointA.sub(pointB);
        double result = (sideBC.length() + sideAC.length() + sideAB.length());
        return result;
    }

    public Vector center(){
        Vector vec = centroid();
        return vec;
    }

    public Vector centroid(){
        // ((x1+x2+x3)/3,(y1+y2+y3)/3)
        double centroidX = (pointA.x + pointB.x + pointC.x) / 3;
        double centroidY = (pointA.y + pointB.y + pointC.y) / 3;

        Vector centroid = new Vector(centroidX, centroidY);
        
        return centroid;
    }
    /*
    public boolean isInside(Vector point){
        // From: https://mathworld.wolfram.com/TriangleInterior.html#:~:text=The%20simplest%20way%20to%20determine,it%20lies%20outside%20the%20triangle.
        
        Vector v = point;
        Vector v0 = pointA;
        Vector v1 = pointC.sub(pointA);
        Vector v2 = pointB.sub(pointA);
    
        double a =   (det(v, v2) - det(v0, v2)) / det(v1, v2);
        double b = - (det(v, v1) - det(v0, v1)) / det(v1, v2);

        if (a >= 0 && b >= 0 && a + b <= 1){
            return true;
        }
        
        return false;
    }*/



    public boolean isInside(Vector point){
        // From: https://mathworld.wolfram.com/TriangleInterior.html#:~:text=The%20simplest%20way%20to%20determine,it%20lies%20outside%20the%20triangle.
        
        Vector v = point;
        Vector v0 = pointA;
        Vector v1 = pointC.sub(pointA);
        Vector v2 = pointB.sub(pointA);
    
        double a =   (det(v, v2) - det(v0, v2)) / det(v1, v2);
        double b = - (det(v, v1) - det(v0, v1)) / det(v1, v2);

        if (a == 0 && b == 0 && a + b < 1){
            return true;
        }
        
        return false;
    }


    private double det(Vector vec1, Vector vec2){
        double determinant = (vec1.x*vec2.y) - (vec1.y*vec2.x);
        return determinant;

    }
    
    
}
