import java.util.*;
import java.math.*;


public class Triangle extends Shape{
    private Vector pointA;
    private Vector pointB;
    private Vector pointC;

    public Triangle(Vector pointA, Vector pointB, Vector pointC){
        this.pointA = pointA;
        this.pointB = pointB;
        this.pointC = pointC;
    }
    public Triangle(double vecA_x, double vecA_y, double vecB_x, double vecB_y,double vecC_x, double vecC_y){
        this.pointA = new Vector(vecA_x,vecA_y);
        this.pointB = new Vector(vecB_x,vecB_y);
        this.pointC = new Vector(vecC_x, vecC_y);
    }


    // Getters
    public Vector getPointA(){
        return pointA;
    }
    public Vector getPointB() {
        return pointB;
    }
    public Vector getPointC() {
        return pointC;
    }
    
    // Setters
    public void setPointA(Vector pointA) {
        this.pointA = pointA;
    }
    public void setPointB(Vector pointB) {
        this.pointB = pointB;
    }
    public void setPointC(Vector pointC) {
        this.pointC = pointC;
    }


    // Returning the area using Heron's formula
    public double area(){
        // length of all sides of the triangle
        double sideBC = lengthOfSide(pointB,pointC);
        double sideAC = lengthOfSide(pointA,pointC);
        double sideAB = lengthOfSide(pointA,pointB);
        
        // semiperimeter = (|BC|+|AC|+|AB|)/2
        double semiperimeter = circumference() / 2;

        // Heron's formula: area = sqrt(semiperimeter*(semiperimeter-|BC|)(semiperimeter-|AC|)(semiperimeter -|AB|))
        double area = Math.sqrt(semiperimeter * (semiperimeter - sideBC) * (semiperimeter - sideAC) * (semiperimeter - sideAB));
        return area;
    }

    // Returning the circumference
    public double circumference(){
        Vector sideBC = pointB.sub(pointC);
        Vector sideAC = pointA.sub(pointC);
        Vector sideAB = pointA.sub(pointB);
        double result = (sideBC.length() + sideAC.length() + sideAB.length());
        return result;
    }

    // Returning the center of the triangle
    public Vector center(){
        Vector vec = centroid(); // The center can be defined in different ways, but we set the default center option as its centroid
        return vec;
    }

    public Vector centroid(){
        // formula for centroid: ((x1+x2+x3)/3,(y1+y2+y3)/3)
        double centroidX = (pointA.x + pointB.x + pointC.x) / 3;
        double centroidY = (pointA.y + pointB.y + pointC.y) / 3;
        Vector centroid = new Vector(centroidX, centroidY);
        return centroid;
    }


    // To check whether a point is inside the triangle. 
    // Mathematics are based on: https://mathworld.wolfram.com/TriangleInterior.html#:~:text=The%20simplest%20way%20to%20determine,it%20lies%20outside%20the%20triangle.
    public boolean containsPoint(Vector point){
        
        // expressing point v as a linear combination of one corner v0 and two adjacent sides, v1 and v2:
        // v = v0 + a*v1 + b*v2

        Vector v = point;
        Vector v0 = pointA;
        Vector v1 = pointC.sub(pointA);
        Vector v2 = pointB.sub(pointA);

        // solving for and computing the constants a and b
        double a =   (det(v, v2) - det(v0, v2)) / det(v1, v2);
        double b = - (det(v, v1) - det(v0, v1)) / det(v1, v2);
        
        // checking the conditions for point v lying inside the triangle
        if (a > 0 && b > 0 && a + b < 1){
            return true;
        }
        return false;
    }

    // Finds the length of the side between two vectors given. Used to find the area of the triangle. 
    private double lengthOfSide(Vector vec1, Vector vec2){
        double side_length = vec1.sub(vec2).length();
        return side_length;
    }

    // The determinant of a 2x2 matrix with column vectors vec1 and vec2, which is used when checking if a point is inside the triangle.
    private double det(Vector vec1, Vector vec2) {
        double determinant = (vec1.x * vec2.y) - (vec1.y * vec2.x);
        return determinant;
    }
}
