import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TriangleTest {
    Triangle tri;

    @BeforeEach
    void setUp(){
        Vector pointA = new Vector(2.50,2.87);
        Vector pointB = new Vector(4.17, 6.98);
        Vector pointC = new Vector(6.66, -2.02);

        tri = new Triangle(pointA, pointB, pointC);
    }

    @Test
    void area() {
        assertEquals(tri.area(), 12.63, 0.01);
    }

    @Test
    void circumference() {
        assertEquals(tri.circumference(), 20.19, 0.01);
    }

    @Test
    void center() {
        double[] actual = {tri.center().x, tri.center().y};
        double[] expected = {4.44, 2.61};
        assertArrayEquals(actual, expected, 0.01);
    }

    @Test
    void centroid() {
        double[] actual = {tri.centroid().x, tri.centroid().y};
        double[] expected = {4.44, 2.61};
        assertArrayEquals(actual, expected, 0.01);
    }

    @Test
    void containsPoint() {
        assertTrue(tri.containsPoint(new Vector(4,2)));
        assertFalse(tri.containsPoint(new Vector(6.16, 0.39)));
    }
}