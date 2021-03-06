

import java.math.*;


public class Vector {
    public double x;
    public double y;

    public Vector(double x, double y){
        this.x = x;
        this.y = y;
    }        

    public Vector(){
        this.x = 0;
        this.y = 0;
    }

    // Returns the length of the vector
    public double length(){
        double len = Math.sqrt(Math.pow(x,2) + Math.pow(y,2));
        return len;        
    }

    // Returns new vectors by adding two vectors
    public Vector add(Vector other_vec){
        Vector new_vector = new Vector();
        new_vector.x = this.x + other_vec.x;
        new_vector.y = this.y + other_vec.y;
        return new_vector;
    }

    // Returns new vectors by subtracting two vectors
    public Vector sub(Vector other_vec){
        Vector new_vector = new Vector();
        new_vector.x = this.x - other_vec.x;
        new_vector.y = this.y - other_vec.y;
        return new_vector;
    
    }
    
    // Directly prints the vector
    public void print(){
        System.out.print(this.toString());
    }

    // Gives a string version of the vector for printing especially. Distinguished from print() above, since this allows for concatenation.
    public String toString(){
        String str = ("(" + this.x + "," + this.y + ")" );
        return str;
    }
}



