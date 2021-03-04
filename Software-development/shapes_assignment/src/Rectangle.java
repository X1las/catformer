



public class Rectangle extends Shape {
    Vector bottom_left;
    double width;
    double height;

    public Rectangle(Vector bottom_left, double width, double height){
        this.bottom_left = bottom_left;
        this.width       = width;
        this.height      = height;
    }



    public double area(){
        double area = this.width * this.height;
        return area;
    }
    
    
    
    public double circumference(){
       double circumference = (2*height) + (2* width);
       return circumference;
            
    }

    public Vector center(){
        double centerX = bottom_left.x + width/2;
        double centerY = bottom_left.y + height/2;
        Vector center = new Vector(centerX, centerY);
        return center;
    }
    
    public boolean isInside(Vector v){
        if (v.x > bottom_left.x && v.x < (bottom_left.x + width) && v.y > bottom_left.y && v.y < (bottom_left.y + height)){
            return true;
        }
        return false;
    }

  
}
