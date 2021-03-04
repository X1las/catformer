import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;

class CircleTest {

    Circle circle;

    @BeforeEach
    void setUp(){
        circle = new Circle(new Vector(4,2), Math.sqrt(10/Math.PI));
    }

    @Test
    void area(){
        assertEquals(circle.area(), 10);
    }

    @Test
    void circumference() {
    }

    @Test
    void center() {
    }

    @Test
    void containsPoint() {
    }
}