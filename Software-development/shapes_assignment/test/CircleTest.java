import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;

class CircleTest {

    Circle circle;

    @BeforeEach
    void setUp(){
        circle = new Circle(new Vector(4.0,2.0), 3);
    }

    @Test
    void area(){
        assertEquals(circle.area(), 28.27, 0.01);
    }

    @Test
    void circumference() {
        assertEquals(circle.circumference(), 18.85, 0.01);
    }

    @Test
    void center() {
        double[] actual = {circle.center().x, circle.center().y};
        double[] expected = {4.0, 2.0};
        assertArrayEquals(actual, expected, 0.01);
    }

    @Test
    void containsPoint() {
        assertTrue(circle.containsPoint( new Vector(5.92,3.38)));
        assertFalse(circle.containsPoint(new Vector(0.90,1.44)));
    }
}