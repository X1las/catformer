import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;

class CircleTest {

    Circle circle_vec, circle_doubles;
    Circle[] circles;

    @BeforeEach
    void setUp(){
        double point_x = 4.0, point_y = 2.0;
        double radius = 3;
        circle_vec = new Circle(new Vector(point_x,point_y), radius);
        circle_doubles = new Circle(point_x, point_y, radius);
        circles = new Circle[]{circle_doubles, circle_vec};
    }

    @Test
    void area(){
        for (Circle circle : circles) assertEquals(circle.area(), 28.27, 0.01);
    }

    @Test
    void circumference() {
        for (Circle circle : circles) assertEquals(circle.circumference(), 18.85, 0.01);
    }

    @Test
    void center() {
        double[] expected = {4.0, 2.0};
        for (Circle circle : circles){
            double[] actual = {circle.center().x, circle.center().y};
            assertArrayEquals(actual, expected, 0.01);
        }


    }

    @Test
    void containsPoint() {
        for (Circle circle : circles){
            assertTrue(circle.containsPoint( new Vector(5.92,3.38)));
            assertFalse(circle.containsPoint(new Vector(0.90,1.44)));
        }
    }
}