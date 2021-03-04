//import jdk.javadoc.internal.doclets.formats.html.SourceToHTMLConverter;




public class Main {

    public static void main(String[] args) {

        Vector vec =  new Vector(4,2);
        Vector vec2 = new Vector(7,3);
        Vector vec3 = new Vector(5,6);

        Triangle tri1 = new Triangle(vec,vec2,vec3);

        Vector cent1 = (tri1.centroid());

        Vector vec_1 =  new Vector(11,2);
        Vector vec2_1 = new Vector(13,2);
        Vector vec3_1 = new Vector(12,4);

        Triangle tri2 = new Triangle(vec_1,vec2_1,vec3_1);
        
        System.out.println(tri2.dist(tri1));


    }
    
    
}
