import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RectangleTest {
    Rectangle rec;

    @BeforeEach
    void setUp(){
        Vector point = new Vector(2.0,-2.0);
        double width = 5.0;
        double height = 3.0;

        rec = new Rectangle(point, width, height);
    }

    @Test
    void area() {
        assertEquals(rec.area(), 15.0, 0.01);
    }

    @Test
    void circumference() {
        assertEquals(rec.circumference(), 16.0,0.01);
    }

    @Test
    void center() {
        double[] actual = {rec.center().x, rec.center().y};
        double[] expected = {4.5, -0.5};
        assertArrayEquals(actual, expected, 0.01);
    }

    @Test
    void containsPoint() {
        assertTrue(rec.containsPoint(new Vector(3.01, -1.80)));
        assertFalse(rec.containsPoint(new Vector(6.40, 1.25)));
    }
}