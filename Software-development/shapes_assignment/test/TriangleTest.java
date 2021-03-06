import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TriangleTest {
    Triangle tri_vec, tri_doubles;
    Triangle[] triangles;

    @BeforeEach
    void setUp(){
        double pointA_x = 2.50, pointA_y = 2.87;
        double pointB_x = 4.17, pointB_y = 6.98;
        double pointC_x = 6.66, pointC_y = -2.02;
        Vector pointA = new Vector(pointA_x, pointA_y);
        Vector pointB = new Vector(pointB_x, pointB_y);
        Vector pointC = new Vector(pointC_x, pointC_y);
        tri_vec = new Triangle(pointA, pointB, pointC);
        tri_doubles = new Triangle(pointA_x, pointA_y, pointB_x, pointB_y, pointC_x, pointC_y);
        triangles = new Triangle[]{tri_vec, tri_doubles};

    }

    @Test
    void area() {
        for (Triangle triangle : triangles) assertEquals(triangle.area(), 12.63, 0.01);
    }

    @Test
    void circumference() {
        for (Triangle triangle : triangles) assertEquals(triangle.circumference(), 20.19, 0.01);
    }

    @Test
    void center() {
        double[] expected = {4.44, 2.61};
        for (Triangle triangle : triangles){
            double[] actual = {triangle.center().x, triangle.center().y};
            assertArrayEquals(actual, expected, 0.01);
        }
    }

    @Test
    void centroid() {
        double[] expected = {4.44, 2.61};
        for (Triangle triangle : triangles){
            double[] actual = {triangle.centroid().x, triangle.centroid().y};
            assertArrayEquals(actual, expected, 0.01);
        }
    }

    @Test
    void containsPoint() {
        for (Triangle triangle : triangles){
            assertTrue(triangle.containsPoint(new Vector(4,2)));
            assertFalse(triangle.containsPoint(new Vector(6.16, 0.39)));
        }


    }
}