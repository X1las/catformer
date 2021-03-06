import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RectangleTest {
    Rectangle rect_vector, rect_doubles;
    Rectangle[] rectangles;

    @BeforeEach
    void setUp(){
        Vector point = new Vector(2.0,-2.0);
        double width = 5.0;
        double height = 3.0;
        rect_vector = new Rectangle(point, width, height);
        rect_doubles = new Rectangle(2.0,-2.0,width,height);
        rectangles = new Rectangle[]{rect_vector, rect_doubles};
    }

    @Test
    void area() {
        for (Rectangle rectangle : rectangles) assertEquals(rectangle.area(), 15.0, 0.01);
    }

    @Test
    void circumference() {
        for (Rectangle rectangle : rectangles) assertEquals(rectangle.circumference(), 16.0,0.01);
    }

    @Test
    void center() {
        double[] expected = {4.5, -0.5};
        for (Rectangle rectangle : rectangles) {
            double[] actual = {rectangle.center().x, rectangle.center().y};
            assertArrayEquals(actual, expected, 0.01);
        }
    }

    @Test
    void containsPoint() {
        for (Rectangle rectangle : rectangles){
            assertTrue(rectangle.containsPoint(new Vector(3.01, -1.80)));
            assertFalse(rectangle.containsPoint(new Vector(6.40, 1.25)));
        }
    }
}