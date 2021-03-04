

import java.math.*;


public class Vector {
    double x;
    double y;

    public Vector(double x, double y){
        this.x = x;
        this.y = y;
    }        

    public Vector(){
        this.x = 0;
        this.y = 0;
    }

    public double length(){
        double len; 
        len = Math.sqrt(Math.pow(x,2) + Math.pow(y,2));
        return len;        
    }

    public Vector add(Vector other_vec){
        Vector new_vector = new Vector();
        new_vector.x = this.x + other_vec.x;
        new_vector.y = this.y + other_vec.y;
        return new_vector;
    
    }

    public Vector sub(Vector other_vec){
        Vector new_vector = new Vector();
        new_vector.x = this.x - other_vec.x;
        new_vector.y = this.y - other_vec.y;
        return new_vector;
    
    }
    
    public void print(){
        System.out.print("(");
        System.out.print(this.x);
        System.out.print(",");
        System.out.print(this.y);
        System.out.println(")");
    }

    public String toString(){
        String str = ("(" + this.x + "," + this.y + ")" );
        return str;
    }

}
