import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;

class CircleTest {

    Circle circle;

    @BeforeEach
    void setUp(){
        circle = new Circle(new Vector(4.0,2.0), Math.sqrt(10/Math.PI));
    }

    @Test
    void area(){
        assertEquals(circle.area(), 10);
    }

    @Test
    void circumference() {
        circle = new Circle(new Vector(0,0), 1/Math.PI);
        assertEquals(circle.circumference(), 2);
    }

    @Test
    void center() {
        assertEquals(circle.center().toString(), new Vector(4.0,2.0).toString());
        assertEquals(circle.center(), circle.getCenter());
    }

    @Test
    void containsPoint() {
        assertTrue(circle.containsPoint(new Vector(4,3)));
        assertFalse(circle.containsPoint(new Vector(100,100)));
    }
}