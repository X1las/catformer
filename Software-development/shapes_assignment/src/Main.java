//import jdk.javadoc.internal.doclets.formats.html.SourceToHTMLConverter;




public class Main {

    public static void main(String[] args) {

        //Vector vec =  new Vector(4,2);

        Vector point_vec = new Vector(4,2);
        Circle circle = new Circle(point_vec,4);

        System.out.println(circle.area());


        Vector bot_left = new Vector(4,2);
        Rectangle rect1 = new Rectangle(bot_left, 10, 2);
        
        Point vec = new Point(4,2);
        Vector vec2 = new Vector(7,3);
        Vector vec3 = new Vector(5,6);

        Triangle tri1 = new Triangle(vec,vec2,vec3);
        //System.out.println(tri1.isInside(vec));

        
        Vector cent1 = (tri1.centroid());

        Vector vec_1 =  new Vector(11.0,2.0);
        Vector vec2_1 = new Vector(13.0,2.0);
        Vector vec3_1 = new Vector(12.0,4.0);

        Triangle tri2 = new Triangle(vec_1,vec2_1,vec3_1);
        
        System.out.println(tri2.getPointA());
        //System.out.println(tri2.isInside(new Point(12.0,2.0)));
        


    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
}
